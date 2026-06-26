#!/usr/bin/env bash
set -euo pipefail

WIL_RUNNER_SAFE_CWD="${WIL_RUNNER_SAFE_CWD:-$PWD}"

REPO_URL="${REPO_URL:-git@github.com:EdLWEISS186/dac-dual-node-cgnat-setup.git}"
BRANCH="${BRANCH:-main}"
TMP_PARENT="${TMP_PARENT:-/tmp}"

PRIMARY_RPC="${PRIMARY_RPC:-http://127.0.0.1:8546}"
FALLBACK_RPC="${FALLBACK_RPC:-http://192.168.100.7:8545}"
MAX_BLOCKS="${MAX_BLOCKS:-50000}"
BALANCE_ENRICH_LIMIT="${BALANCE_ENRICH_LIMIT:-1000}"
SLEEP_SECONDS="${SLEEP_SECONDS:-180}"
PUSH_TO_GITHUB="${PUSH_TO_GITHUB:-1}"
RUN_ONCE="${RUN_ONCE:-0}"

# Phase-aware runtime presets.
# Backfill/catch-up stay conservative and device-safe.
# Incremental switches to small, frequent micro-sync cycles.
WIL_PHASE_AWARE_PRESET="${WIL_PHASE_AWARE_PRESET:-1}"

BACKFILL_MAX_BLOCKS="${BACKFILL_MAX_BLOCKS:-50000}"
BACKFILL_ADAPTIVE_CHUNK_SIZE="${BACKFILL_ADAPTIVE_CHUNK_SIZE:-5000}"
BACKFILL_SLEEP_SECONDS="${BACKFILL_SLEEP_SECONDS:-180}"

CATCHUP_MAX_BLOCKS="${CATCHUP_MAX_BLOCKS:-50000}"
CATCHUP_ADAPTIVE_CHUNK_SIZE="${CATCHUP_ADAPTIVE_CHUNK_SIZE:-5000}"
CATCHUP_SLEEP_SECONDS="${CATCHUP_SLEEP_SECONDS:-180}"

INCREMENTAL_SLEEP_SECONDS="${INCREMENTAL_SLEEP_SECONDS:-60}"
INCREMENTAL_MAX_BLOCKS_NORMAL="${INCREMENTAL_MAX_BLOCKS_NORMAL:-10}"
INCREMENTAL_CHUNK_SIZE_NORMAL="${INCREMENTAL_CHUNK_SIZE_NORMAL:-10}"
INCREMENTAL_MAX_BLOCKS_LAG_100="${INCREMENTAL_MAX_BLOCKS_LAG_100:-25}"
INCREMENTAL_CHUNK_SIZE_LAG_100="${INCREMENTAL_CHUNK_SIZE_LAG_100:-25}"
INCREMENTAL_MAX_BLOCKS_LAG_500="${INCREMENTAL_MAX_BLOCKS_LAG_500:-100}"
INCREMENTAL_CHUNK_SIZE_LAG_500="${INCREMENTAL_CHUNK_SIZE_LAG_500:-100}"
INCREMENTAL_MAX_BLOCKS_LAG_HIGH="${INCREMENTAL_MAX_BLOCKS_LAG_HIGH:-500}"
INCREMENTAL_CHUNK_SIZE_LAG_HIGH="${INCREMENTAL_CHUNK_SIZE_LAG_HIGH:-100}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SQLITE_HEALTH_GUARD="$SCRIPT_DIR/sqlite_health_guard.py"
ADAPTIVE_CHUNK_GUARD="$SCRIPT_DIR/adaptive_chunk_guard.py"
ADAPTIVE_RUNTIME_DIR="${ADAPTIVE_RUNTIME_DIR:-$HOME/wil-v3-worker-logs/adaptive-runtime}"
ADAPTIVE_ACTIVE_RUNTIME_DIR=""
ACTIVE_WORKDIR=""

ensure_safe_cwd() {
  cd "$WIL_RUNNER_SAFE_CWD" 2>/dev/null || cd "$HOME" 2>/dev/null || cd /
}
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


cleanup_active_workdir() {
  local dir="${ACTIVE_WORKDIR:-}"

  if [ -z "$dir" ]; then
    return 0
  fi

  case "$dir" in
    /tmp/wil-v3-rank-run.*)
      if [ -d "$dir" ]; then
        ensure_safe_cwd
        rm -rf -- "$dir"
        echo "[INFO] Cleaned temp workdir: $dir"
      fi
      ACTIVE_WORKDIR=""
      ;;
    *)
      echo "[WARN] Refusing to clean unexpected temp workdir: $dir"
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

trap 'cleanup_adaptive_runtime_dir || true; cleanup_active_workdir || true' EXIT


EXTERNAL_STATE_DIR="${EXTERNAL_STATE_DIR:-$HOME/wil-v3-rank-state}"
EXTERNAL_SQLITE_FILE="${EXTERNAL_SQLITE_FILE:-$EXTERNAL_STATE_DIR/wil-v3-rank-state.sqlite}"
EXTERNAL_BACKUP_DIR="${EXTERNAL_BACKUP_DIR:-$EXTERNAL_STATE_DIR/backups}"
BACKUP_EXTERNAL_STATE_EVERY_RUN="${BACKUP_EXTERNAL_STATE_EVERY_RUN:-0}"

load_wil_sync_snapshot_env() {
  local preset_file
  preset_file="$(mktemp)"

  python3 - "$EXTERNAL_SQLITE_FILE" "$PRIMARY_RPC" > "$preset_file" <<'WIL_PHASE_SNAPSHOT_PY'
import json
import sqlite3
import sys
import urllib.request

sqlite_path = sys.argv[1]
rpc_url = sys.argv[2]

def shell_quote(value):
    text = "" if value is None else str(value)
    return "'" + text.replace("'", "'\"'\"'") + "'"

def load_checkpoint(path):
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True, timeout=10)
    rows = conn.execute("SELECT key, value_json FROM checkpoint").fetchall()
    conn.close()

    out = {}
    for key, value in rows:
        try:
            out[key] = json.loads(value)
        except Exception:
            out[key] = value
    return out

def rpc_latest_block(url):
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": [],
        "id": 1,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=8) as resp:
        return int(json.loads(resp.read().decode("utf-8"))["result"], 16)

try:
    cp = load_checkpoint(sqlite_path)
except Exception as exc:
    cp = {}
    print(f"WIL_PHASE_PRESET_ERROR={shell_quote('sqlite:' + str(exc))}")

phase = cp.get("sync_phase") or "HISTORICAL_BACKFILL_IN_PROGRESS"
latest_block = None

try:
    latest_block = rpc_latest_block(rpc_url)
except Exception as exc:
    print(f"WIL_PHASE_RPC_ERROR={shell_quote(str(exc))}")

incremental_next = cp.get("incremental_next_block")
catch_up_next = cp.get("catch_up_next_block")
backfill_next = cp.get("local_rpc_backfill_next_block")

lag = 0
if str(phase).upper() == "INCREMENTAL" and latest_block is not None and incremental_next is not None:
    try:
        lag = max(0, int(latest_block) - int(incremental_next) + 1)
    except Exception:
        lag = 0

print(f"WIL_PHASE_SYNC_PHASE={shell_quote(phase)}")
print(f"WIL_PHASE_CHAIN_LATEST_BLOCK={shell_quote(latest_block)}")
print(f"WIL_PHASE_BACKFILL_NEXT_BLOCK={shell_quote(backfill_next)}")
print(f"WIL_PHASE_CATCH_UP_NEXT_BLOCK={shell_quote(catch_up_next)}")
print(f"WIL_PHASE_INCREMENTAL_NEXT_BLOCK={shell_quote(incremental_next)}")
print(f"WIL_PHASE_INCREMENTAL_LAG_BLOCKS={shell_quote(lag)}")
WIL_PHASE_SNAPSHOT_PY

  # shellcheck disable=SC1090
  . "$preset_file"
  rm -f "$preset_file"
}

resolve_phase_aware_preset() {
  if [ "$WIL_PHASE_AWARE_PRESET" != "1" ]; then
    echo "[INFO] Phase-aware preset disabled | MAX_BLOCKS=$MAX_BLOCKS | ADAPTIVE_CHUNK_SIZE=$ADAPTIVE_CHUNK_SIZE | SLEEP_SECONDS=$SLEEP_SECONDS"
    return 0
  fi

  load_wil_sync_snapshot_env

  local phase
  phase="${WIL_PHASE_SYNC_PHASE:-HISTORICAL_BACKFILL_IN_PROGRESS}"

  case "$phase" in
    INCREMENTAL)
      local lag
      lag="${WIL_PHASE_INCREMENTAL_LAG_BLOCKS:-0}"

      if [ "$lag" -le 20 ]; then
        MAX_BLOCKS="$INCREMENTAL_MAX_BLOCKS_NORMAL"
        ADAPTIVE_CHUNK_SIZE="$INCREMENTAL_CHUNK_SIZE_NORMAL"
      elif [ "$lag" -le 100 ]; then
        MAX_BLOCKS="$INCREMENTAL_MAX_BLOCKS_LAG_100"
        ADAPTIVE_CHUNK_SIZE="$INCREMENTAL_CHUNK_SIZE_LAG_100"
      elif [ "$lag" -le 500 ]; then
        MAX_BLOCKS="$INCREMENTAL_MAX_BLOCKS_LAG_500"
        ADAPTIVE_CHUNK_SIZE="$INCREMENTAL_CHUNK_SIZE_LAG_500"
      else
        MAX_BLOCKS="$INCREMENTAL_MAX_BLOCKS_LAG_HIGH"
        ADAPTIVE_CHUNK_SIZE="$INCREMENTAL_CHUNK_SIZE_LAG_HIGH"
      fi

      SLEEP_SECONDS="$INCREMENTAL_SLEEP_SECONDS"
      ;;

    POST_BACKFILL_CATCH_UP)
      MAX_BLOCKS="$CATCHUP_MAX_BLOCKS"
      ADAPTIVE_CHUNK_SIZE="$CATCHUP_ADAPTIVE_CHUNK_SIZE"
      SLEEP_SECONDS="$CATCHUP_SLEEP_SECONDS"
      ;;

    *)
      MAX_BLOCKS="$BACKFILL_MAX_BLOCKS"
      ADAPTIVE_CHUNK_SIZE="$BACKFILL_ADAPTIVE_CHUNK_SIZE"
      SLEEP_SECONDS="$BACKFILL_SLEEP_SECONDS"
      ;;
  esac

  echo "[INFO] Phase-aware preset | phase=${phase} | latest=${WIL_PHASE_CHAIN_LATEST_BLOCK:-unknown} | backfill_next=${WIL_PHASE_BACKFILL_NEXT_BLOCK:-unknown} | catch_up_next=${WIL_PHASE_CATCH_UP_NEXT_BLOCK:-unknown} | incremental_next=${WIL_PHASE_INCREMENTAL_NEXT_BLOCK:-unknown} | lag_blocks=${WIL_PHASE_INCREMENTAL_LAG_BLOCKS:-0} | MAX_BLOCKS=$MAX_BLOCKS | ADAPTIVE_CHUNK_SIZE=$ADAPTIVE_CHUNK_SIZE | SLEEP_SECONDS=$SLEEP_SECONDS"
}

run_once() {
  local workdir
  workdir="$(mktemp -d "$TMP_PARENT/wil-v3-rank-run.XXXXXX")"
  local repo="$workdir/repo"

  cleanup() {
    ensure_safe_cwd
    rm -rf "$workdir"
  }
  ACTIVE_WORKDIR="$workdir"
  # RETURN trap disabled for adaptive multi-chunk mode; cleanup is explicit.

  echo "[INFO] Temporary workdir: $workdir"
  echo "[INFO] Cloning repo..."
  local clone_ok=0
  for clone_attempt in 1 2 3; do
    echo "[INFO] Clone attempt ${clone_attempt}/3"
    rm -rf "$repo"

    if git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$repo"; then
      clone_ok=1
      break
    fi

    echo "[WARN] Git clone failed on attempt ${clone_attempt}; retrying after 10s..."
    sleep 10
  done

  if [ "$clone_ok" != "1" ]; then
    echo "[WARN] Git clone failed after retries; skipping this cycle and keeping runner alive."
    cleanup_active_workdir || true
    return 0
  fi

  cd "$repo"

  local base="DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3"
  local worker="$base/rank-data-engine/scripts/local_rpc_rank_data_worker.py"
  local lightweight_generator="$base/rank-data-engine/scripts/generate_lightweight_public_rank_status.py"
  local public_status="$base/rank-data-engine/data/public-run-status.json"
  local worker_abs="$repo/$worker"
  local public_status_abs="$repo/$public_status"

  mkdir -p "$base/rank-data-engine/data" "$base/data" "$EXTERNAL_STATE_DIR" "$EXTERNAL_BACKUP_DIR"

    if [ ! -f "$EXTERNAL_SQLITE_FILE" ]; then
      echo "[INFO] SQLite rank state not found; bootstrapping fresh v3.7.0 rebuild DB: $EXTERNAL_SQLITE_FILE"
      PYTHONPATH="$(dirname "$worker_abs")" python3 - "$EXTERNAL_SQLITE_FILE" <<'WIL_V3_7_BOOTSTRAP_SQLITE'
import sys
from pathlib import Path
from sqlite_rank_state import SQLiteRankState

state = SQLiteRankState(Path(sys.argv[1]))
state.close()
print("[OK] Bootstrapped fresh SQLite rank state")
WIL_V3_7_BOOTSTRAP_SQLITE
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
        cleanup_adaptive_runtime_dir || true
        cleanup_active_workdir || true
        exit "$WORKER_RC"
      fi

      mem_available_kb="$(awk '/MemAvailable:/ {print $2}' /proc/meminfo 2>/dev/null || echo 0)"
      mem_available_kb="${mem_available_kb:-0}"

      swap_used_kb="$(awk '/SwapTotal:/ {t=$2} /SwapFree:/ {f=$2} END {print t-f}' /proc/meminfo 2>/dev/null || echo 0)"
      swap_used_kb="${swap_used_kb:-0}"

      load1="$(awk '{print $1}' /proc/loadavg 2>/dev/null || echo 0)"
      load1="${load1:-0}"

      cpu_cores="$(nproc 2>/dev/null || echo 1)"
      cpu_cores="${cpu_cores:-1}"

      vmstat_sample="$(vmstat 1 2 2>/dev/null | tail -1 || true)"
      cpu_idle_pct="$(printf '%s\n' "$vmstat_sample" | awk '{print $15}')"
      cpu_idle_pct="${cpu_idle_pct:-100}"
      io_wait_pct="$(printf '%s\n' "$vmstat_sample" | awk '{print $16}')"
      io_wait_pct="${io_wait_pct:-0}"

      python3 "$ADAPTIVE_CHUNK_GUARD" \
        --status "$public_status_abs" \
        --elapsed-seconds "$chunk_elapsed" \
        --wal-growth-bytes "$wal_growth_bytes" \
        --free-kb "$free_after_kb" \
        --mem-available-kb "$mem_available_kb" \
        --swap-used-kb "$swap_used_kb" \
        --worker-mem-kb "$worker_mem_kb" \
        --load1 "$load1" \
        --cpu-cores "$cpu_cores" \
        --cpu-idle-pct "$cpu_idle_pct" \
        --io-wait-pct "$io_wait_pct" \
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

  echo "[INFO] WIL v3.7.0 worker result"
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

echo "[INFO] WIL v3.7.0 SQLite Rank State Worker | Parity-Safe Rebuild"
echo "[INFO] primary=$PRIMARY_RPC"
echo "[INFO] fallback=$FALLBACK_RPC"
echo "[INFO] max_blocks=$MAX_BLOCKS"
echo "[INFO] balance_enrich_limit=$BALANCE_ENRICH_LIMIT"
echo "[INFO] sleep_seconds=$SLEEP_SECONDS"
echo "[INFO] push_to_github=$PUSH_TO_GITHUB"
echo "[INFO] run_once=$RUN_ONCE"
echo "[INFO] sqlite_state_file=$EXTERNAL_SQLITE_FILE"

while true; do
  ensure_safe_cwd
  echo
  echo "============================================================"
  echo "[INFO] Run started at $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "============================================================"

  resolve_phase_aware_preset
  run_once

  echo "[INFO] Run finished at $(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  if [ "$RUN_ONCE" = "1" ]; then
    echo "[INFO] RUN_ONCE=1, exiting."
    exit 0
  fi

  echo "[INFO] Sleeping ${SLEEP_SECONDS}s..."
  echo "[INFO] Clean adaptive runtime before sleep"
  cleanup_adaptive_runtime_dir || true

  echo "[INFO] Clean temp workdir before sleep"
  cleanup_active_workdir || true

  sleep "$SLEEP_SECONDS"
done
