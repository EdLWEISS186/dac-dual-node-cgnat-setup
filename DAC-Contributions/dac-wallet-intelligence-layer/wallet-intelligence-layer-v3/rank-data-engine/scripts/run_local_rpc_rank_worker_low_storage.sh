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

EXTERNAL_STATE_DIR="${EXTERNAL_STATE_DIR:-$HOME/wil-v3-rank-state}"
EXTERNAL_STATE_FILE="${EXTERNAL_STATE_FILE:-$EXTERNAL_STATE_DIR/latest-state.json}"
EXTERNAL_BACKUP_DIR="${EXTERNAL_BACKUP_DIR:-$EXTERNAL_STATE_DIR/backups}"
BACKUP_EXTERNAL_STATE_EVERY_RUN="${BACKUP_EXTERNAL_STATE_EVERY_RUN:-0}"

run_once() {
  local workdir
  workdir="$(mktemp -d "$TMP_PARENT/wil-v3-rank-run.XXXXXX")"

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
  local generator="$base/scripts/generate_rank_from_engine_data.py"
  local repo_state="$base/rank-data-engine/data/latest.json"

  mkdir -p "$base/rank-data-engine/data" "$base/data" "$EXTERNAL_STATE_DIR" "$EXTERNAL_BACKUP_DIR"

  if [ ! -f "$EXTERNAL_STATE_FILE" ]; then
    echo "[ERROR] External state file not found: $EXTERNAL_STATE_FILE"
    echo "[ERROR] Restore ~/wil-v3-rank-state/latest-state.json before running v3.2.0 worker."
    exit 1
  fi

  echo "[INFO] Restoring heavy state from external local storage"
  cp "$EXTERNAL_STATE_FILE" "$repo_state"

  echo "[INFO] Running local RPC worker"
  /usr/bin/time -f "[TIME] elapsed=%E cpu=%P mem_kb=%M" \
    python3 "$worker" \
      --primary-rpc "$PRIMARY_RPC" \
      --fallback-rpc "$FALLBACK_RPC" \
      --max-blocks "$MAX_BLOCKS" \
      --balance-enrich-limit "$BALANCE_ENRICH_LIMIT" \
      --no-snapshot-archive

  python3 -m json.tool "$repo_state" >/dev/null

  echo "[INFO] Saving heavy state back to external local storage"
  cp "$repo_state" "$EXTERNAL_STATE_FILE"

  if [ "$BACKUP_EXTERNAL_STATE_EVERY_RUN" = "1" ]; then
    cp "$EXTERNAL_STATE_FILE" "$EXTERNAL_BACKUP_DIR/latest-state-$(date -u +"%Y-%m-%dT%H-%M-%SZ").json"
  fi

  echo "[INFO] Generating public rank summary/index"
  python3 "$generator"

  echo "[INFO] Replacing GitHub latest.json with small public manifest"
  python3 <<'PY'
import json
from pathlib import Path
from datetime import datetime, timezone

base = Path("DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3")
state_path = base / "rank-data-engine/data/latest.json"
summary_path = base / "data/wallet-rank-summary.json"
manifest_path = state_path

state = json.loads(state_path.read_text())
checkpoint = state.get("checkpoint", {})
counters = state.get("counters", {})
summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}

manifest = {
    "schema": "WIL_V3_PUBLIC_RANK_MANIFEST",
    "version": "v3.2.0",
    "project": "Wallet Intelligence Layer v3.2.0",
    "engine": "rank-data-engine",
    "network": state.get("network", "DAC Testnet"),
    "chain_id": state.get("chain_id", 21894),
    "status": "EXTERNALIZED_STATE_BACKFILL_IN_PROGRESS",
    "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    "externalized_state": True,
    "heavy_state_storage": "LOCAL_EXTERNAL_STATE_WITH_OPTIONAL_GOOGLE_DRIVE_BACKUP",
    "heavy_state_local_path": "~/wil-v3-rank-state/latest-state.json",
    "github_storage_role": "PUBLIC_MANIFEST_ONLY",
    "rank_lookup_enabled": False,
    "rank_shards_published": False,
    "snapshot_archive_written": state.get("snapshot_archive_written", False),
    "latest_snapshot": "externalized-local-state",
    "sync_status": {
        "phase": checkpoint.get("sync_phase"),
        "historical_backfill_complete": checkpoint.get("historical_backfill_complete") is True,
        "catch_up_status": checkpoint.get("catch_up_status"),
        "historical_backfill_anchor_block": checkpoint.get("historical_backfill_anchor_block"),
        "last_synced_block": checkpoint.get("last_synced_block"),
        "local_rpc_backfill_next_block": checkpoint.get("local_rpc_backfill_next_block"),
        "catch_up_next_block": checkpoint.get("catch_up_next_block"),
        "incremental_next_block": checkpoint.get("incremental_next_block"),
        "local_rpc_latest_block_at_sync": checkpoint.get("local_rpc_latest_block_at_sync"),
        "last_sync_at": checkpoint.get("last_sync_at"),
    },
    "counters": {
        "total_indexed_wallets": counters.get("total_indexed_wallets"),
        "total_processed_transactions": counters.get("total_processed_transactions"),
        "native_balance_snapshots": counters.get("native_balance_snapshots"),
        "last_sync_processed_blocks": counters.get("last_sync_processed_blocks"),
        "last_sync_processed_transactions": counters.get("last_sync_processed_transactions"),
        "last_sync_wallets_changed": counters.get("last_sync_wallets_changed"),
    },
    "public_summary": {
        "path": "data/wallet-rank-summary.json",
        "status": summary.get("status"),
        "has_valid_rank_index": summary.get("has_valid_rank_index"),
        "total_ranked_wallets": summary.get("total_ranked_wallets"),
    },
    "note": "GitHub no longer stores monolithic rank state. Heavy rank state is externalized for v3.2.0."
}

manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
PY

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

echo "[INFO] WIL v3.2.0 Externalized Rank State Worker"
echo "[INFO] primary=$PRIMARY_RPC"
echo "[INFO] fallback=$FALLBACK_RPC"
echo "[INFO] max_blocks=$MAX_BLOCKS"
echo "[INFO] balance_enrich_limit=$BALANCE_ENRICH_LIMIT"
echo "[INFO] sleep_seconds=$SLEEP_SECONDS"
echo "[INFO] push_to_github=$PUSH_TO_GITHUB"
echo "[INFO] run_once=$RUN_ONCE"
echo "[INFO] external_state_file=$EXTERNAL_STATE_FILE"

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
  sleep "$SLEEP_SECONDS"
done
