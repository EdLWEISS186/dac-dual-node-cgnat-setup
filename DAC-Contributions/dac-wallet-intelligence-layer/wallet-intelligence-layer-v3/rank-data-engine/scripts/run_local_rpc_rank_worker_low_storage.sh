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

run_once() {
  local workdir
  workdir="$(mktemp -d "$TMP_PARENT/wil-v3-rank-run.XXXXXX")"

  cleanup() {
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

  echo "[INFO] Running local RPC worker"
  /usr/bin/time -f "[TIME] elapsed=%E cpu=%P mem_kb=%M" \
    python3 "$worker" \
      --primary-rpc "$PRIMARY_RPC" \
      --fallback-rpc "$FALLBACK_RPC" \
      --max-blocks "$MAX_BLOCKS" \
      --balance-enrich-limit "$BALANCE_ENRICH_LIMIT" \
      --no-snapshot-archive

  echo "[INFO] Generating rank output"
  python3 "$generator"

  python3 -m json.tool "$base/rank-data-engine/data/latest.json" >/dev/null
  python3 -m json.tool "$base/data/wallet-rank-summary.json" >/dev/null
  python3 -m json.tool "$base/data/wallet-rank-index.json" >/dev/null

  python3 <<'PY'
import json
from pathlib import Path

base = Path("DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3")
latest = json.loads((base / "rank-data-engine/data/latest.json").read_text())
summary = json.loads((base / "data/wallet-rank-summary.json").read_text())

print("[STATUS] last_sync:", latest["checkpoint"].get("last_sync_at"))
print("[STATUS] last_synced_block:", latest["checkpoint"].get("last_synced_block"))
print("[STATUS] next_block:", latest["checkpoint"].get("local_rpc_backfill_next_block"))
print("[STATUS] processed_tx:", latest["counters"].get("total_processed_transactions"))
print("[STATUS] indexed_wallets:", latest["counters"].get("total_indexed_wallets"))
print("[STATUS] native_balance_snapshots:", latest["counters"].get("native_balance_snapshots"))
print("[STATUS] ranked_wallets:", summary.get("total_ranked_wallets"))
print("[STATUS] latest_snapshot:", latest.get("latest_snapshot"))
print("[STATUS] snapshot_archive_written:", latest.get("snapshot_archive_written"))
PY

  git add -f "$base/rank-data-engine/data/latest.json"
  git add -f "$base/data/wallet-rank-summary.json"
  git add -f "$base/data/wallet-rank-index.json"
  git add -f "$base/data/rank-shards/"*.json

  if git diff --cached --quiet; then
    echo "[INFO] No WIL v3 rank data changes to commit."
  else
    git config user.name "JERUZZALEM Local Rank Worker"
    git config user.email "suryaawalaka@gmail.com"

    git commit -m "chore: sync WIL v3 local RPC rank data"

    if [ "$PUSH_TO_GITHUB" = "1" ]; then
      git push origin "$BRANCH"
    else
      echo "[INFO] PUSH_TO_GITHUB=0, commit kept only inside temp folder."
    fi
  fi

  echo "[INFO] Temporary workdir removed after this run."
}

echo "[INFO] WIL v3 Low-Local-Storage Worker"
echo "[INFO] primary=$PRIMARY_RPC"
echo "[INFO] fallback=$FALLBACK_RPC"
echo "[INFO] max_blocks=$MAX_BLOCKS"
echo "[INFO] balance_enrich_limit=$BALANCE_ENRICH_LIMIT"
echo "[INFO] sleep_seconds=$SLEEP_SECONDS"
echo "[INFO] push_to_github=$PUSH_TO_GITHUB"
echo "[INFO] run_once=$RUN_ONCE"

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
