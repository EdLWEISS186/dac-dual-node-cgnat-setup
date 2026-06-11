#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd
)"

BUILDER="${BUILDER:-$SCRIPT_DIR/generate_rank_from_sqlite.py}"

STATE_DB="${STATE_DB:-$HOME/wil-v3-rank-state/wil-v3-rank-state.sqlite}"
REPO_URL="${REPO_URL:-https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup.git}"
DATA_BRANCH="${DATA_BRANCH:-wil-v3-rank-data}"

WORK_ROOT="${WORK_ROOT:-$HOME/wil-v3-rank-state/rank-snapshot-publisher}"
BUILDER_WORK_ROOT="${BUILDER_WORK_ROOT:-$HOME/wil-v3-rank-state/rank-publisher-work}"
LOCK_FILE="${LOCK_FILE:-$HOME/wil-v3-rank-state/rank-snapshot-publisher.lock}"

PUSH_TO_GITHUB="${PUSH_TO_GITHUB:-1}"
ALLOW_INCOMPLETE="${ALLOW_INCOMPLETE:-0}"
LIMIT="${LIMIT:-}"
KEEP_WORK="${KEEP_WORK:-0}"
BATCH_SIZE="${BATCH_SIZE:-1000}"

STAMP="$(date -u +"%Y-%m-%dT%H-%M-%SZ")"
RUN_DIR="$WORK_ROOT/run-$STAMP-$$"
OUTPUT_DIR="$RUN_DIR/output"
SNAPSHOT_REPO="$RUN_DIR/snapshot-repo"

mkdir -p \
  "$WORK_ROOT" \
  "$BUILDER_WORK_ROOT" \
  "$(dirname "$LOCK_FILE")"

exec 9>"$LOCK_FILE"

if ! flock -n 9; then
  echo "[INFO] Another WIL rank snapshot publisher is running."
  exit 0
fi

cleanup() {
  if [ "$KEEP_WORK" = "1" ]; then
    echo "[INFO] Keeping publisher work directory: $RUN_DIR"
  else
    rm -rf "$RUN_DIR"
  fi
}

trap cleanup EXIT

for command_name in \
  python3 \
  git \
  flock
do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "[ERROR] Required command not found: $command_name"
    exit 1
  fi
done

if [ ! -f "$BUILDER" ]; then
  echo "[ERROR] SQLite rank publisher not found: $BUILDER"
  exit 1
fi

if [ ! -f "$STATE_DB" ]; then
  echo "[ERROR] SQLite rank state not found: $STATE_DB"
  exit 1
fi

case "$PUSH_TO_GITHUB" in
  0|1) ;;
  *)
    echo "[ERROR] PUSH_TO_GITHUB must be 0 or 1"
    exit 1
    ;;
esac

case "$ALLOW_INCOMPLETE" in
  0|1) ;;
  *)
    echo "[ERROR] ALLOW_INCOMPLETE must be 0 or 1"
    exit 1
    ;;
esac

if [ -n "$LIMIT" ] && ! [[ "$LIMIT" =~ ^[1-9][0-9]*$ ]]; then
  echo "[ERROR] LIMIT must be empty or a positive integer"
  exit 1
fi

if [ "$PUSH_TO_GITHUB" = "1" ]; then
  if [ "$ALLOW_INCOMPLETE" = "1" ]; then
    echo "[ERROR] Incomplete rank snapshots cannot be pushed."
    exit 1
  fi

  if [ -n "$LIMIT" ]; then
    echo "[ERROR] Limited rank snapshots cannot be pushed."
    exit 1
  fi
fi

mkdir -p "$OUTPUT_DIR"

echo "[INFO] WIL v3.3.0 compact rank snapshot publisher"
echo "[INFO] state_db=$STATE_DB"
echo "[INFO] data_branch=$DATA_BRANCH"
echo "[INFO] push_to_github=$PUSH_TO_GITHUB"
echo "[INFO] allow_incomplete=$ALLOW_INCOMPLETE"
echo "[INFO] limit=${LIMIT:-none}"
echo "[INFO] run_dir=$RUN_DIR"

builder_arguments=(
  --state-db "$STATE_DB"
  --output-dir "$OUTPUT_DIR"
  --work-root "$BUILDER_WORK_ROOT"
  --batch-size "$BATCH_SIZE"
)

if [ "$ALLOW_INCOMPLETE" = "1" ]; then
  builder_arguments+=(--allow-incomplete)
fi

if [ -n "$LIMIT" ]; then
  builder_arguments+=(--limit "$LIMIT")
fi

echo
echo "[INFO] Building compact global rank snapshot"

/usr/bin/time \
  -f "[TIME] rank_build_elapsed=%E cpu=%P mem_kb=%M" \
  python3 "$BUILDER" "${builder_arguments[@]}"

SUMMARY="$OUTPUT_DIR/wallet-rank-summary.json"
INDEX="$OUTPUT_DIR/wallet-rank-index.json"
SHARDS_DIR="$OUTPUT_DIR/rank-shards"

echo
echo "[INFO] Validating generated snapshot"

python3 - \
  "$SUMMARY" \
  "$INDEX" \
  "$SHARDS_DIR" \
  "$PUSH_TO_GITHUB" <<'PY'
import json
import sys
from pathlib import Path

summary_path = Path(sys.argv[1])
index_path = Path(sys.argv[2])
shards_dir = Path(sys.argv[3])
push_enabled = sys.argv[4] == "1"

for required in [summary_path, index_path]:
    if not required.is_file() or required.stat().st_size == 0:
        raise SystemExit(
            f"Required rank artifact missing or empty: {required}"
        )

if not shards_dir.is_dir():
    raise SystemExit(
        f"Rank shard directory missing: {shards_dir}"
    )

summary = json.loads(
    summary_path.read_text(encoding="utf-8")
)

index = json.loads(
    index_path.read_text(encoding="utf-8")
)

if summary.get("version") != "v3.3.0":
    raise SystemExit("Unexpected summary version")

if summary.get("state_backend") != "SQLITE":
    raise SystemExit("Summary is not SQLite-backed")

expected_small_metric_order = [
    "native_funds",
    "estimated_current_stake",
    "transactions",
    "native_volume",
    "gas_used",
    "nft_holdings",
    "collection_diversity",
    "reputation_score",
    "low_sybil_risk",
]

expected_metric_order = (
    expected_small_metric_order
    + ["official_inception_nfts"]
)

expected_composite_metric_order = [
    "native_funds",
    "transactions",
    "gas_used",
    "native_volume",
    "nft_holdings",
    "collection_diversity",
    "reputation_score",
    "low_sybil_risk",
]

expected_rank_order = (
    expected_metric_order
    + ["overall_rank"]
)

if (
    summary.get("compact_record_schema")
    != "WIL_V3_COMPACT_ARRAY_V2"
):
    raise SystemExit(
        "Unexpected summary compact record schema"
    )

if index.get("mode") != "SHARDED_COMPACT_V2":
    raise SystemExit("Unexpected rank index mode")

if (
    index.get("record_schema")
    != "WIL_V3_COMPACT_ARRAY_V2"
):
    raise SystemExit("Unexpected compact record schema")

if (
    summary.get("small_metric_order")
    != expected_small_metric_order
):
    raise SystemExit(
        "Unexpected summary small metric order"
    )

if (
    index.get("small_metric_order")
    != expected_small_metric_order
):
    raise SystemExit(
        "Unexpected index small metric order"
    )

if (
    index.get("metric_order")
    != expected_metric_order
):
    raise SystemExit(
        "Unexpected complete metric order"
    )

if (
    summary.get("composite_ranking_variables")
    != expected_composite_metric_order
):
    raise SystemExit(
        "Unexpected summary composite metric order"
    )

if (
    index.get("composite_metric_order")
    != expected_composite_metric_order
):
    raise SystemExit(
        "Unexpected index composite metric order"
    )

if (
    index.get("official_signal_key")
    != "official_inception_nfts"
):
    raise SystemExit(
        "Official Rank Signal key is missing"
    )

if (
    index.get("rank_order")
    != expected_rank_order
):
    raise SystemExit(
        "Unexpected comparative rank order"
    )

official_rank_tiers = {
    int(minimum): label
    for minimum, label
    in (index.get("official_rank_tiers") or [])
}

expected_official_rank_tiers = {
    0: "NONE",
    1: "CADET",
    2: "COMMANDO",
    3: "SEAL",
    4: "SHADOW UNIT",
    5: "VANGUARD",
    6: "SENTINEL",
    7: "SOVEREIGN",
    8: "WARRIOR",
    9: "ARCHITECT",
    10: "INTERCEPTOR",
    11: "PHANTOM",
    12: "CIPHER",
    13: "CROWN",
}

if (
    official_rank_tiers
    != expected_official_rank_tiers
):
    raise SystemExit(
        "Unexpected Official Rank Signal tiers"
    )

shard_files = sorted(shards_dir.glob("*.json"))

expected_shards = int(
    summary.get("rank_shards", {}).get("shard_count")
    or 0
)

if not shard_files:
    raise SystemExit("No rank shards generated")

if len(shard_files) != expected_shards:
    raise SystemExit(
        "Generated shard count mismatch: "
        f"{len(shard_files)} != {expected_shards}"
    )

for shard_file in shard_files:
    if shard_file.stat().st_size == 0:
        raise SystemExit(
            f"Empty rank shard: {shard_file}"
        )

if push_enabled:
    if summary.get("has_valid_rank_index") is not True:
        raise SystemExit(
            "Production push requires a valid rank summary"
        )

    if index.get("has_valid_rank_index") is not True:
        raise SystemExit(
            "Production push requires a valid rank index"
        )

total_bytes = sum(
    shard_file.stat().st_size
    for shard_file in shard_files
)

print("[OK] rank snapshot structure valid")
print("[OK] compact schema valid")
print(f"[OK] shard_count={len(shard_files)}")
print(
    "[OK] total_ranked_wallets="
    f"{summary.get('total_ranked_wallets')}"
)
print(f"[OK] shard_bytes={total_bytes}")
print(
    "[OK] valid_public_index="
    f"{summary.get('has_valid_rank_index')}"
)
PY

echo
echo "[INFO] Creating single-commit snapshot repository"

git init -q -b "$DATA_BRANCH" "$SNAPSHOT_REPO"

mkdir -p "$SNAPSHOT_REPO/data"

cp "$SUMMARY" \
  "$SNAPSHOT_REPO/data/wallet-rank-summary.json"

cp "$INDEX" \
  "$SNAPSHOT_REPO/data/wallet-rank-index.json"

cp -a "$SHARDS_DIR" \
  "$SNAPSHOT_REPO/data/rank-shards"

touch "$SNAPSHOT_REPO/.nojekyll"

python3 - \
  "$SUMMARY" \
  "$INDEX" \
  "$SNAPSHOT_REPO/snapshot-manifest.json" \
  "$DATA_BRANCH" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

summary_path = Path(sys.argv[1])
index_path = Path(sys.argv[2])
manifest_path = Path(sys.argv[3])
branch = sys.argv[4]

summary = json.loads(
    summary_path.read_text(encoding="utf-8")
)

index = json.loads(
    index_path.read_text(encoding="utf-8")
)

manifest = {
    "schema": "WIL_V3_RANK_SNAPSHOT_MANIFEST",
    "version": "v3.3.0",
    "branch": branch,
    "created_at": datetime.now(
        timezone.utc
    ).replace(microsecond=0).isoformat(),
    "state_backend": "SQLITE",
    "record_schema": index.get("record_schema"),
    "index_mode": index.get("mode"),
    "generated_at": summary.get("generated_at"),
    "has_valid_rank_index": (
        summary.get("has_valid_rank_index")
    ),
    "total_ranked_wallets": (
        summary.get("total_ranked_wallets")
    ),
    "total_processed_transactions": (
        summary.get("total_processed_transactions")
    ),
    "shard_count": (
        summary.get("rank_shards", {}).get(
            "shard_count"
        )
    ),
    "paths": {
        "summary": "data/wallet-rank-summary.json",
        "index": "data/wallet-rank-index.json",
        "shards": "data/rank-shards",
    },
}

manifest_path.write_text(
    json.dumps(
        manifest,
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

print("[OK] snapshot manifest created")
PY

cat > "$SNAPSHOT_REPO/README.md" <<'EOF'
# WIL v3.3.0 Rank Data Snapshot

This branch contains the current compact public Wallet Intelligence Layer
rank snapshot.

Generated artifacts:

- `data/wallet-rank-summary.json`
- `data/wallet-rank-index.json`
- `data/rank-shards/*.json`
- `snapshot-manifest.json`

The heavy SQLite state is not stored in this branch.
EOF

git -C "$SNAPSHOT_REPO" \
  config user.name \
  "JERUZZALEM WIL Rank Publisher"

git -C "$SNAPSHOT_REPO" \
  config user.email \
  "suryaawalaka@gmail.com"

git -C "$SNAPSHOT_REPO" add .

git -C "$SNAPSHOT_REPO" commit -q \
  -m "publish: WIL v3.3.0 compact rank snapshot $STAMP"

SNAPSHOT_COMMIT="$(
  git -C "$SNAPSHOT_REPO" rev-parse HEAD
)"

echo "[OK] snapshot_commit=$SNAPSHOT_COMMIT"

if [ "$PUSH_TO_GITHUB" = "1" ]; then
  echo
  echo "[INFO] Force-publishing single snapshot commit"

  git -C "$SNAPSHOT_REPO" \
    remote add origin "$REPO_URL"

  git -C "$SNAPSHOT_REPO" \
    push --force origin \
    "HEAD:refs/heads/$DATA_BRANCH"

  echo "[OK] snapshot branch published: $DATA_BRANCH"
else
  echo
  echo "[INFO] PUSH_TO_GITHUB=0; snapshot branch was not pushed"
fi

echo
echo "[INFO] Snapshot repository files"

find "$SNAPSHOT_REPO" \
  -maxdepth 3 \
  -type f \
  ! -path '*/.git/*' \
  -printf '%s %p\n' \
  | sort -n \
  | tail -20

echo
echo "[OK] WIL v3.3.0 compact rank snapshot publisher complete"
