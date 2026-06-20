#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup.git}"
BRANCH="${BRANCH:-main}"
TMP_PARENT="${TMP_PARENT:-/tmp}"

PRIMARY_RPC="${PRIMARY_RPC:-http://127.0.0.1:8546}"
FALLBACK_RPC="${FALLBACK_RPC:-http://192.168.100.7:8545}"
MAX_BLOCKS="${MAX_BLOCKS:-100}"
BALANCE_ENRICH_LIMIT="${BALANCE_ENRICH_LIMIT:-700}"
SLEEP_SECONDS="${SLEEP_SECONDS:-600}"
PUSH_TO_GITHUB="${PUSH_TO_GITHUB:-1}"
RUN_ONCE="${RUN_ONCE:-0}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQLITE_HEALTH_GUARD="$SCRIPT_DIR/sqlite_health_guard.py"
ADAPTIVE_CHUNK_GUARD="$SCRIPT_DIR/adaptive_chunk_guard.py"
ADAPTIVE_RUNTIME_DIR="${ADAPTIVE_RUNTIME_DIR:-$HOME/wil-v3-worker-logs/adaptive-runtime}"
ADAPTIVE_ACTIVE_RUNTIME_DIR=""
ADAPTIVE_CHUNK_MODE="${ADAPTIVE_CHUNK_MODE:-1}"
ADAPTIVE_CHUNK_SIZE="${ADAPTIVE_CHUNK_SIZE:-5000}"
ADAPTIVE_MAX_CHUNK_SECONDS="${ADAPTIVE_MAX_CHUNK_SECONDS:-180}"
ADAPTIVE_MAX_CHUNK_TX="${ADAPTIVE_MAX_CHUNK_TX:-5000}"
ADAPTIVE_MAX_CHUNK_WALLET_ROWS="${ADAPTIVE_MAX_CHUNK_WALLET_ROWS:-1000}"
ADAPTIVE_MAX_CHUNK_STAKING_ROWS="${ADAPTIVE_MAX_CHUNK_STAKING_ROWS:-500}"
ADAPTIVE_MAX_CHUNK_WAL_GROWTH_BYTES="${ADAPTIVE_MAX_CHUNK_WAL_GROWTH_BYTES:-536870912}"
ADAPTIVE_MIN_FREE_KB="${ADAPTIVE_MIN_FREE_KB:-26214400}"
ADAPTIVE_MIN_MEM_AVAILABLE_KB="${ADAPTIVE_MIN_MEM_AVAILABLE_KB:-1048576}"
ADAPTIVE_MAX_SWAP_USED_KB="${ADAPTIVE_MAX_SWAP_USED_KB:-1048576}"
ADAPTIVE_MAX_WORKER_MEM_KB="${ADAPTIVE_MAX_WORKER_MEM_KB:-768000}"
ADAPTIVE_MAX_LOAD_FACTOR_X100="${ADAPTIVE_MAX_LOAD_FACTOR_X100:-150}"
ADAPTIVE_MIN_CPU_IDLE_PCT="${ADAPTIVE_MIN_CPU_IDLE_PCT:-15}"
ADAPTIVE_MAX_IO_WAIT_PCT="${ADAPTIVE_MAX_IO_WAIT_PCT:-20}"


cleanup_adaptive_runtime_dir() {
  local dir="${ADAPTIVE_ACTIVE_RUNTIME_DIR:-}"

  if [ -z "$dir" ]; then
    return 0
  fi

  case "$dir" in
    "$ADAPTIVE_RUNTIME_DIR"/wil-v3-rank-run.*)
      if [ -d "$dir" ]; then
        rm -rf -- "$dir"
        echo "[INFO] Cleaned adaptive runtime dir: $dir"
      fi
      ADAPTIVE_ACTIVE_RUNTIME_DIR=""
      ;;
    *)
      echo "[WARN] Refusing to clean unexpected adaptive runtime dir: $dir"
      ;;
  esac
}

cleanup_stale_adaptive_runtime_dirs() {
  mkdir -p "$ADAPTIVE_RUNTIME_DIR"

  find "$ADAPTIVE_RUNTIME_DIR" \
    -mindepth 1 \
    -maxdepth 1 \
    -type d \
    -name "wil-v3-rank-run.*" \
    -mmin +120 \
    -print \
    -exec rm -rf {} + \
    2>/dev/null || true
}

trap 'cleanup_adaptive_runtime_dir || true' EXIT


EXTERNAL_STATE_DIR="${EXTERNAL_STATE_DIR:-$HOME/wil-v3-rank-state}"
EXTERNAL_SQLITE_FILE="${EXTERNAL_SQLITE_FILE:-$EXTERNAL_STATE_DIR/wil-v3-rank-state.sqlite}"
EXTERNAL_BACKUP_DIR="${EXTERNAL_BACKUP_DIR:-$EXTERNAL_STATE_DIR/backups}"
BACKUP_EXTERNAL_STATE_EVERY_RUN="${BACKUP_EXTERNAL_STATE_EVERY_RUN:-0}"

run_once() {
  local workdir
  workdir="$(mktemp -d "$TMP_PARENT/wil-v3-rank-run.XXXXXX")"
  local repo="$workdir/repo"

  cleanup() {
    cd "$HOME" 2>/dev/null || true
    rm -rf "$workdir"
  }
  trap cleanup RETURN

  echo "[INFO] Temporary workdir: $workdir"
  echo "[INFO] Cloning repo..."
  git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$workdir/repo"

  cd "$workdir/repo"

  local base="DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3"
  local worker="$base/rank-data-engine/scripts/local_rpc_rank_data_worker.py"
  local lightweight_generator="$base/rank-data-engine/scripts/generate_lightweight_public_rank_status.py"
  local public_status="$base/rank-data-engine/data/public-run-status.json"
  local worker_abs="$repo/$worker"
  local public_status_abs="$repo/$public_status"

  mkdir -p "$base/rank-data-engine/data" "$base/data" "$EXTERNAL_STATE_DIR" "$EXTERNAL_BACKUP_DIR"

  if [ ! -f "$EXTERNAL_SQLITE_FILE" ]; then
    echo "[ERROR] SQLite rank state not found: $EXTERNAL_SQLITE_FILE"
    echo "[ERROR] Restore or migrate wil-v3-rank-state.sqlite before running the worker."
    exit 1
  fi

  echo "[INFO] Checking external SQLite rank state"
  if [ "${WIL_V3_FULL_SQLITE_QUICK_CHECK:-0}" = "1" ]; then
    echo "[INFO] Running full SQLite health guard because WIL_V3_FULL_SQLITE_QUICK_CHECK=1"
    timeout 1800s python3 "$SQLITE_HEALTH_GUARD" --sqlite-state "$EXTERNAL_SQLITE_FILE" --mode full
    HEALTH_RC=$?
  else
    echo "[INFO] Running lightweight SQLite health guard"
    timeout 60s python3 "$SQLITE_HEALTH_GUARD" --sqlite-state "$EXTERNAL_SQLITE_FILE" --mode lightweight
    HEALTH_RC=$?
  fi

  if [ "$HEALTH_RC" -ne 0 ]; then
    echo "[ERROR] SQLite preflight health guard failed: exit=$HEALTH_RC"
    timeout 1800s python3 "$SQLITE_HEALTH_GUARD" --sqlite-state "$EXTERNAL_SQLITE_FILE" --mode diagnose --force-full || true
    exit "$HEALTH_RC"
  fi

  echo "[INFO] Using external SQLite rank state directly"

  echo "[INFO] Running local RPC worker"

  get_mem_available_kb() { awk '/MemAvailable:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0; }
  get_swap_used_kb() { awk '/SwapTotal:/ {t=$2} /SwapFree:/ {f=$2} END {print t-f}' /proc/meminfo 2>/dev/null || echo 0; }
  get_load1() { awk '{print $1}' /proc/loadavg 2>/dev/null || echo 0; }
  get_cpu_cores() { nproc 2>/dev/null || echo 1; }
  get_cpu_idle_pct() { vmstat 1 2 2>/dev/null | tail -1 | awk '{print $15}' || echo 100; }
  get_io_wait_pct() { vmstat 1 2 2>/dev/null | tail -1 | awk '{print $16}' || echo 0; }

  if [ "$ADAPTIVE_CHUNK_MODE" = "1" ] && [ "$MAX_BLOCKS" -gt "$ADAPTIVE_CHUNK_SIZE" ]; then
    echo "[INFO] Adaptive chunk checkpoint mode enabled"
    echo "[INFO] adaptive_target_blocks=$MAX_BLOCKS"
    echo "[INFO] adaptive_chunk_size=$ADAPTIVE_CHUNK_SIZE"
    echo "[INFO] adaptive_max_chunk_seconds=$ADAPTIVE_MAX_CHUNK_SECONDS"
    echo "[INFO] adaptive_max_chunk_tx=$ADAPTIVE_MAX_CHUNK_TX"
    echo "[INFO] adaptive_max_chunk_wallet_rows=$ADAPTIVE_MAX_CHUNK_WALLET_ROWS"
    echo "[INFO] adaptive_max_chunk_staking_rows=$ADAPTIVE_MAX_CHUNK_STAKING_ROWS"
    echo "[INFO] adaptive_max_chunk_wal_growth_bytes=$ADAPTIVE_MAX_CHUNK_WAL_GROWTH_BYTES"
    echo "[INFO] adaptive_min_free_kb=$ADAPTIVE_MIN_FREE_KB"
    echo "[INFO] adaptive_min_mem_available_kb=$ADAPTIVE_MIN_MEM_AVAILABLE_KB"
    echo "[INFO] adaptive_max_swap_used_kb=$ADAPTIVE_MAX_SWAP_USED_KB"
    echo "[INFO] adaptive_max_worker_mem_kb=$ADAPTIVE_MAX_WORKER_MEM_KB"
    echo "[INFO] adaptive_max_load_factor_x100=$ADAPTIVE_MAX_LOAD_FACTOR_X100"
    echo "[INFO] adaptive_min_cpu_idle_pct=$ADAPTIVE_MIN_CPU_IDLE_PCT"
    echo "[INFO] adaptive_max_io_wait_pct=$ADAPTIVE_MAX_IO_WAIT_PCT"

    mkdir -p "$ADAPTIVE_RUNTIME_DIR"
    cleanup_stale_adaptive_runtime_dirs || true

    adaptive_run_id="$(basename "$workdir")"
    adaptive_cycle_runtime_dir="$ADAPTIVE_RUNTIME_DIR/$adaptive_run_id"
    ADAPTIVE_ACTIVE_RUNTIME_DIR="$adaptive_cycle_runtime_dir"

    rm -rf -- "$adaptive_cycle_runtime_dir"
    mkdir -p "$adaptive_cycle_runtime_dir"

    adaptive_done_blocks=0
    adaptive_chunk_index=0

    while [ "$adaptive_done_blocks" -lt "$MAX_BLOCKS" ]; do
      adaptive_remaining=$((MAX_BLOCKS - adaptive_done_blocks))
      adaptive_this_chunk="$ADAPTIVE_CHUNK_SIZE"
      if [ "$adaptive_remaining" -lt "$adaptive_this_chunk" ]; then
        adaptive_this_chunk="$adaptive_remaining"
      fi

      adaptive_chunk_index=$((adaptive_chunk_index + 1))
      echo "[INFO] Adaptive chunk $adaptive_chunk_index started | target_blocks=$adaptive_this_chunk | completed_before=$adaptive_done_blocks"

      free_before_kb="$(df -Pk "$EXTERNAL_STATE_DIR" | awk 'NR==2 {print $4}')"
      wal_before_bytes="$(stat -c %s "$EXTERNAL_SQLITE_FILE-wal" 2>/dev/null || echo 0)"
      chunk_time_file="$adaptive_cycle_runtime_dir/adaptive-chunk-$adaptive_chunk_index.time"
      decision_file="$adaptive_cycle_runtime_dir/adaptive-chunk-$adaptive_chunk_index.env"
      rm -f "$chunk_time_file" "$decision_file"
      chunk_start_ts="$(date +%s)"

      set +e
      /usr/bin/time -o "$chunk_time_file" -f "[TIME] elapsed=%E cpu=%P mem_kb=%M" \
          python3 "$worker_abs" \
          --primary-rpc "$PRIMARY_RPC" \
          --fallback-rpc "$FALLBACK_RPC" \
          --sqlite-state "$EXTERNAL_SQLITE_FILE" \
          --max-blocks "$adaptive_this_chunk" \
          --balance-enrich-limit "$BALANCE_ENRICH_LIMIT" \
          --no-snapshot-archive
      WORKER_RC=$?
      set -e

      cat "$chunk_time_file" 2>/dev/null || true
      worker_mem_kb="$(awk -F'mem_kb=' '/mem_kb=/ {print $2}' "$chunk_time_file" 2>/dev/null | awk '{print $1}' | tail -1)"
      worker_mem_kb="${worker_mem_kb:-0}"

      chunk_end_ts="$(date +%s)"
      chunk_elapsed=$((chunk_end_ts - chunk_start_ts))
      free_after_kb="$(df -Pk "$EXTERNAL_STATE_DIR" | awk 'NR==2 {print $4}')"
      wal_after_bytes="$(stat -c %s "$EXTERNAL_SQLITE_FILE-wal" 2>/dev/null || echo 0)"
      wal_growth_bytes=$((wal_after_bytes - wal_before_bytes))
      if [ "$wal_growth_bytes" -lt 0 ]; then
        wal_growth_bytes=0
      fi

      if [ "$WORKER_RC" -ne 0 ]; then
        echo "[ERROR] Local RPC worker failed in adaptive chunk $adaptive_chunk_index: exit=$WORKER_RC"
        echo "[INFO] Running SQLite failure diagnostic"
        timeout 1800s python3 "$SQLITE_HEALTH_GUARD" --sqlite-state "$EXTERNAL_SQLITE_FILE" --mode diagnose --force-full || true
        exit "$WORKER_RC"
      fi

      python3 "$ADAPTIVE_CHUNK_GUARD" \
        --status "$public_status_abs" \
        --elapsed-seconds "$chunk_elapsed" \
        --wal-growth-bytes "$wal_growth_bytes" \
        --free-kb "$free_after_kb" \
        --mem-available-kb "$(get_mem_available_kb)" \
        --swap-used-kb "$(get_swap_used_kb)" \
        --worker-mem-kb "$worker_mem_kb" \
        --load1 "$(get_load1)" \
        --cpu-cores "$(get_cpu_cores)" \
        --cpu-idle-pct "$(get_cpu_idle_pct)" \
        --io-wait-pct "$(get_io_wait_pct)" \
        --max-chunk-seconds "$ADAPTIVE_MAX_CHUNK_SECONDS" \
        --max-chunk-tx "$ADAPTIVE_MAX_CHUNK_TX" \
        --max-wallet-rows "$ADAPTIVE_MAX_CHUNK_WALLET_ROWS" \
        --max-staking-rows "$ADAPTIVE_MAX_CHUNK_STAKING_ROWS" \
        --max-wal-growth-bytes "$ADAPTIVE_MAX_CHUNK_WAL_GROWTH_BYTES" \
        --min-free-kb "$ADAPTIVE_MIN_FREE_KB" \
        --min-mem-available-kb "$ADAPTIVE_MIN_MEM_AVAILABLE_KB" \
        --max-swap-used-kb "$ADAPTIVE_MAX_SWAP_USED_KB" \
        --max-worker-mem-kb "$ADAPTIVE_MAX_WORKER_MEM_KB" \
        --max-load-factor-x100 "$ADAPTIVE_MAX_LOAD_FACTOR_X100" \
        --min-cpu-idle-pct "$ADAPTIVE_MIN_CPU_IDLE_PCT" \
        --max-io-wait-pct "$ADAPTIVE_MAX_IO_WAIT_PCT" \
        > "$decision_file"

      sed 's/^/[ADAPTIVE_DECISION] /' "$decision_file"
      . "$decision_file"

      adaptive_done_blocks=$((adaptive_done_blocks + ADAPTIVE_CHUNK_PROCESSED_BLOCKS))

      echo "[ADAPTIVE] chunk=$adaptive_chunk_index blocks=$ADAPTIVE_CHUNK_PROCESSED_BLOCKS tx=$ADAPTIVE_CHUNK_PROCESSED_TX wallet_rows=$ADAPTIVE_CHUNK_WALLET_ROWS staking_rows=$ADAPTIVE_CHUNK_STAKING_ROWS elapsed_seconds=$ADAPTIVE_CHUNK_ELAPSED_SECONDS worker_mem_kb=$ADAPTIVE_WORKER_MEM_KB wal_growth_bytes=$ADAPTIVE_CHUNK_WAL_GROWTH_BYTES free_kb=$ADAPTIVE_FREE_KB mem_available_kb=$ADAPTIVE_MEM_AVAILABLE_KB swap_used_kb=$ADAPTIVE_SWAP_USED_KB load1=$ADAPTIVE_LOAD1 load_threshold=$ADAPTIVE_LOAD_THRESHOLD cpu_idle_pct=$ADAPTIVE_CPU_IDLE_PCT io_wait_pct=$ADAPTIVE_IO_WAIT_PCT stop_reason=$ADAPTIVE_CHUNK_WORKER_STOP_REASON decision=$ADAPTIVE_SHOULD_CONTINUE reason=$ADAPTIVE_STOP_REASON total_blocks=$adaptive_done_blocks"

      if [ "$ADAPTIVE_SHOULD_CONTINUE" != "1" ]; then
        echo "[WARN] Adaptive guard stopping cycle early: $ADAPTIVE_STOP_REASON"
        break
      fi
    done

    echo "[INFO] Adaptive cycle completed | target_blocks=$MAX_BLOCKS | actual_blocks=$adaptive_done_blocks"
  else
    echo "[INFO] Adaptive chunk checkpoint mode disabled or not needed"
    set +e
    /usr/bin/time -f "[TIME] elapsed=%E cpu=%P mem_kb=%M" \
        python3 "$worker_abs" \
        --primary-rpc "$PRIMARY_RPC" \
        --fallback-rpc "$FALLBACK_RPC" \
        --sqlite-state "$EXTERNAL_SQLITE_FILE" \
        --max-blocks "$MAX_BLOCKS" \
        --balance-enrich-limit "$BALANCE_ENRICH_LIMIT" \
        --no-snapshot-archive
    WORKER_RC=$?
    set -e

    if [ "$WORKER_RC" -ne 0 ]; then
      echo "[ERROR] Local RPC worker failed: exit=$WORKER_RC"
      echo "[INFO] Running SQLite failure diagnostic"
      timeout 1800s python3 "$SQLITE_HEALTH_GUARD" --sqlite-state "$EXTERNAL_SQLITE_FILE" --mode diagnose --force-full || true
      exit "$WORKER_RC"
    fi
  fi

  if [ "$BACKUP_EXTERNAL_STATE_EVERY_RUN" = "1" ]; then
    backup_file="$EXTERNAL_BACKUP_DIR/wil-v3-rank-state-$(date -u +"%Y-%m-%dT%H-%M-%SZ").sqlite"

    echo "[INFO] Creating consistent per-run SQLite backup"
    rm -f "$backup_file"

    python3 -c 'import sqlite3,sys; src=sqlite3.connect(sys.argv[1]); dst=sqlite3.connect(sys.argv[2]); src.backup(dst); dst.commit(); dst.close(); src.close()' "$EXTERNAL_SQLITE_FILE" "$backup_file"

    python3 -c 'import sqlite3,sys; db=sqlite3.connect(sys.argv[1]); result=db.execute("PRAGMA integrity_check").fetchone()[0]; db.close(); raise SystemExit(0 if result == "ok" else f"SQLite backup integrity_check failed: {result}")' "$backup_file"
  fi

  python3 -m json.tool "$public_status" >/dev/null

  echo "[INFO] WIL v3.6.0 worker result"
  python3 - "$public_status" <<'STATUS_PY'
import json
import sys

status = json.load(open(sys.argv[1], encoding="utf-8"))
sync = status.get("sync_status", {}) or {}
last = status.get("last_run", {}) or {}

print("[STATUS] project:", status.get("project"))
print("[STATUS] version:", status.get("version"))
print("[STATUS] note:", status.get("note"))
print("[STATUS] phase:", sync.get("phase"))
print("[STATUS] historical_backfill_complete:", sync.get("historical_backfill_complete"))
print("[STATUS] last_synced_block:", sync.get("last_synced_block"))
print("[STATUS] local_rpc_backfill_next_block:", sync.get("local_rpc_backfill_next_block"))
print("[STATUS] catch_up_next_block:", sync.get("catch_up_next_block"))
print("[STATUS] catch_up_status:", sync.get("catch_up_status"))
print("[STATUS] local_rpc_latest_block_at_sync:", sync.get("local_rpc_latest_block_at_sync"))

for key in [
    "mode",
    "direction",
    "start_block",
    "end_block",
    "processed_blocks",
    "processed_transactions",
    "processed_staking_events",
    "staking_wallets_changed",
    "wallet_rows_written",
    "staking_rows_written",
    "stop_reason",
]:
    print(f"[STATUS] last_run.{key}:", last.get(key))

STATUS_PY

  echo "[INFO] Generating lightweight public sync artifacts"
  python3 "$lightweight_generator" --status-file "$public_status"

  publish_ready="$(
    python3 -c 'import json,sys; s=json.load(open(sys.argv[1], encoding="utf-8")); x=s.get("sync_status", {}); print("1" if x.get("phase") == "INCREMENTAL" and x.get("historical_backfill_complete") is True and x.get("catch_up_status") in ("CAUGHT_UP", None) else "0")' "$public_status"
  )"

  if [ "$publish_ready" = "1" ]; then
    echo "[INFO] Publish-ready incremental state detected."
    echo "[INFO] Full global rank publishing is handled by the dedicated SQLite snapshot publisher."
  fi

  python3 -m json.tool "$base/rank-data-engine/data/latest.json" >/dev/null
  python3 -m json.tool "$base/data/wallet-rank-summary.json" >/dev/null
  python3 -m json.tool "$base/data/wallet-rank-index.json" >/dev/null

  python3 <<'PY'
import json
from pathlib import Path

base = Path("DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3")
manifest = json.loads((base / "rank-data-engine/data/latest.json").read_text())
summary = json.loads((base / "data/wallet-rank-summary.json").read_text())

sync = manifest.get("sync_status", {})
counters = manifest.get("counters", {})

print("[STATUS] manifest_status:", manifest.get("status"))
print("[STATUS] sync_phase:", sync.get("phase"))
print("[STATUS] last_synced_block:", sync.get("last_synced_block"))
print("[STATUS] next_block:", sync.get("local_rpc_backfill_next_block"))
print("[STATUS] processed_tx:", counters.get("total_processed_transactions"))
print("[STATUS] indexed_wallets:", counters.get("total_indexed_wallets"))
print("[STATUS] native_balance_snapshots:", counters.get("native_balance_snapshots"))
print("[STATUS] rank_lookup_enabled:", manifest.get("rank_lookup_enabled"))
print("[STATUS] rank_shards_published:", manifest.get("rank_shards_published"))
print("[STATUS] summary_status:", summary.get("status"))
print("[STATUS] summary_ranked_wallets:", summary.get("total_ranked_wallets"))
PY

  manifest_file="$base/rank-data-engine/data/latest.json"
  summary_file="$base/data/wallet-rank-summary.json"
  index_file="$base/data/wallet-rank-index.json"
  shards_dir="$base/data/rank-shards"

  git add -f "$manifest_file"
  git add -f "$summary_file"
  git add -f "$index_file"
  git rm -r --cached --ignore-unmatch --sparse "$shards_dir" >/dev/null 2>&1 || true

  if git diff --cached --quiet; then
    echo "[INFO] No WIL v3 public manifest changes to commit."
  else
    git config user.name "JERUZZALEM Local Rank Worker"
    git config user.email "suryaawalaka@gmail.com"

    if [ "$PUSH_TO_GITHUB" = "1" ]; then
      publish_tmp="$(mktemp -d)"

      cp "$manifest_file" "$publish_tmp/latest.json"
      cp "$summary_file" "$publish_tmp/wallet-rank-summary.json"
      cp "$index_file" "$publish_tmp/wallet-rank-index.json"

      publish_ok=0

      for publish_attempt in 1 2 3; do
        echo "[INFO] Publish attempt $publish_attempt/3: refreshing temp clone from origin/$BRANCH"

        git fetch origin "$BRANCH"
        git reset --hard "origin/$BRANCH"

        mkdir -p "$(dirname "$manifest_file")"
        mkdir -p "$(dirname "$summary_file")"
        mkdir -p "$(dirname "$index_file")"

        cp "$publish_tmp/latest.json" "$manifest_file"
        cp "$publish_tmp/wallet-rank-summary.json" "$summary_file"
        cp "$publish_tmp/wallet-rank-index.json" "$index_file"

        git add -f "$manifest_file"
        git add -f "$summary_file"
        git add -f "$index_file"
        git rm -r --cached --ignore-unmatch --sparse "$shards_dir" >/dev/null 2>&1 || true

        if git diff --cached --quiet; then
          echo "[INFO] No WIL v3 public manifest changes after refresh."
          publish_ok=1
          break
        fi

        git commit -m "chore: sync WIL v3 public rank manifest"

        if git push origin "$BRANCH"; then
          publish_ok=1
          break
        fi

        echo "[WARN] GitHub push rejected or failed on attempt $publish_attempt. Retrying after refresh..."
        sleep 5
      done

      rm -rf "$publish_tmp"

      if [ "$publish_ok" != "1" ]; then
        echo "[WARN] GitHub publish failed after retries. Heavy state was saved locally; worker will continue."
      fi
    else
      git commit -m "chore: sync WIL v3 public rank manifest"
      echo "[INFO] PUSH_TO_GITHUB=0, commit kept only inside temp folder."
    fi
  fi

  echo "[INFO] Temporary workdir removed after this run."
}

echo "[INFO] WIL v3.6.0 SQLite Rank State Worker | Back to Normal - standard stake/rank worker"
echo "[INFO] primary=$PRIMARY_RPC"
echo "[INFO] fallback=$FALLBACK_RPC"
echo "[INFO] max_blocks=$MAX_BLOCKS"
echo "[INFO] balance_enrich_limit=$BALANCE_ENRICH_LIMIT"
echo "[INFO] sleep_seconds=$SLEEP_SECONDS"
echo "[INFO] push_to_github=$PUSH_TO_GITHUB"
echo "[INFO] run_once=$RUN_ONCE"
echo "[INFO] sqlite_state_file=$EXTERNAL_SQLITE_FILE"

while true; do
  echo
  echo "============================================================"
  echo "[INFO] Run started at $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "============================================================"

  run_once

  echo "[INFO] Run finished at $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  if [ "$RUN_ONCE" = "1" ]; then
    echo "[INFO] RUN_ONCE=1, exiting."
    exit 0
  fi

  echo "[INFO] Sleeping ${SLEEP_SECONDS}s..."
  echo "[INFO] Clean adaptive runtime before sleep"
  cleanup_adaptive_runtime_dir || true

  sleep "$SLEEP_SECONDS"
done
