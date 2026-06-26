#!/usr/bin/env bash
set -euo pipefail

STATE_DB="${STATE_DB:-$HOME/wil-v3-rank-state/wil-v3-rank-state.sqlite}"
WORK_DIR="${WORK_DIR:-$HOME/wil-v3-rank-state/gdrive-upload-work}"
PRIMARY_REMOTE_NAME="${PRIMARY_REMOTE_NAME:-gdrive_wil_a}"
SECONDARY_REMOTE_NAME="${SECONDARY_REMOTE_NAME:-gdrive_wil_b}"
BASE_FOLDER="${BASE_FOLDER:-WIL-v3-rank-state}"
ROLLOVER_USED_PERCENT="${ROLLOVER_USED_PERCENT:-90}"
KEEP_LOCAL_DAYS="${KEEP_LOCAL_DAYS:-3}"
UPLOAD_ENABLED="${UPLOAD_ENABLED:-1}"
LOCK_FILE="${LOCK_FILE:-$HOME/wil-v3-rank-state/gdrive-backup.lock}"

mkdir -p "$WORK_DIR" "$(dirname "$LOCK_FILE")"

exec 9>"$LOCK_FILE"

if ! flock -n 9; then
  echo "[INFO] Another WIL SQLite GDrive backup is already running."
  exit 0
fi

STAMP="$(date -u +"%Y-%m-%dT%H-%M-%SZ")"
SNAPSHOT="$WORK_DIR/wil-v3-rank-state-$STAMP.sqlite"
COMPRESSED="$SNAPSHOT.zst"
CHECKSUM="$COMPRESSED.sha256"
LOCAL_MANIFEST="$WORK_DIR/latest-gdrive-backup-manifest.json"

for command_name in python3 zstd sha256sum rclone flock; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "[ERROR] Required command not found: $command_name"
    exit 1
  fi
done

if [ ! -f "$STATE_DB" ]; then
  echo "[ERROR] SQLite state database not found: $STATE_DB"
  exit 1
fi

echo "[INFO] WIL v3.7.0 SQLite GDrive rollover backup"
echo "[INFO] state_db=$STATE_DB"
echo "[INFO] primary=$PRIMARY_REMOTE_NAME"
echo "[INFO] secondary=$SECONDARY_REMOTE_NAME"
echo "[INFO] rollover_used_percent=$ROLLOVER_USED_PERCENT"
echo "[INFO] upload_enabled=$UPLOAD_ENABLED"

echo
echo "[INFO] Checking active SQLite database"

python3 - "$STATE_DB" <<'PY'
import sqlite3
import sys
from pathlib import Path

database = Path(sys.argv[1])

connection = sqlite3.connect(
    f"file:{database}?mode=ro",
    uri=True,
)

result = connection.execute(
    "PRAGMA quick_check"
).fetchone()[0]

connection.close()

if result != "ok":
    raise SystemExit(
        f"Active SQLite quick_check failed: {result}"
    )

print("[OK] active SQLite quick_check: ok")
PY

SYNC_PHASE="$(
  python3 - "$STATE_DB" <<'PY'
import json
import sqlite3
import sys
from pathlib import Path

database = Path(sys.argv[1])

connection = sqlite3.connect(
    f"file:{database}?mode=ro",
    uri=True,
)

row = connection.execute(
    """
    SELECT value_json
    FROM checkpoint
    WHERE key = 'sync_phase'
    """
).fetchone()

connection.close()

if row is None:
    print("UNKNOWN")
else:
    print(json.loads(row[0]) or "UNKNOWN")
PY
)"

case "$SYNC_PHASE" in
  HISTORICAL_BACKFILL_IN_PROGRESS|LOCAL_RPC_HISTORICAL_BACKFILL)
    PHASE_FOLDER="Backfill to Genesis"
    ;;
  POST_BACKFILL_CATCH_UP|LOCAL_RPC_POST_BACKFILL_CATCH_UP)
    PHASE_FOLDER="Post Backfill Catch Up"
    ;;
  INCREMENTAL|LOCAL_RPC_INCREMENTAL)
    PHASE_FOLDER="Incremental"
    ;;
  *)
    PHASE_FOLDER="Backfill to Genesis"
    ;;
esac

echo "[INFO] sync_phase=$SYNC_PHASE"
echo "[INFO] phase_folder=$PHASE_FOLDER"

get_used_percent() {
  local remote="$1"
  local about_json

  about_json="$(rclone about "$remote:" --json)"

  ABOUT_JSON="$about_json" python3 -c '
import json
import os

data = json.loads(os.environ["ABOUT_JSON"])
used = int(data.get("used") or 0)
total = int(data.get("total") or 0)

print(
    round((used / total) * 100, 4)
    if total > 0
    else 0
)
'
}

PRIMARY_USED_PERCENT="$(get_used_percent "$PRIMARY_REMOTE_NAME")"

ROLLOVER_DECISION="$(
  python3 -c "
used = float('$PRIMARY_USED_PERCENT')
limit = float('$ROLLOVER_USED_PERCENT')
print('primary' if used < limit else 'secondary')
"
)"

USE_REMOTE="$PRIMARY_REMOTE_NAME"

if [ "$ROLLOVER_DECISION" = "secondary" ]; then
  USE_REMOTE="$SECONDARY_REMOTE_NAME"
fi

SELECTED_USED_PERCENT="$(get_used_percent "$USE_REMOTE")"

REMOTE_BASE="$USE_REMOTE:$BASE_FOLDER"
REMOTE_PHASE="$REMOTE_BASE/$PHASE_FOLDER"
REMOTE_LATEST="$REMOTE_BASE/latest"

echo "[INFO] primary_used_percent=$PRIMARY_USED_PERCENT"
echo "[INFO] selected_remote=$USE_REMOTE"
echo "[INFO] selected_used_percent=$SELECTED_USED_PERCENT"
echo "[INFO] remote_phase=$REMOTE_PHASE"
echo "[INFO] remote_latest=$REMOTE_LATEST"

echo
echo "[INFO] Creating consistent SQLite snapshot"

rm -f "$SNAPSHOT" "$COMPRESSED" "$CHECKSUM"

python3 - "$STATE_DB" "$SNAPSHOT" <<'PY'
import sqlite3
import sys
from pathlib import Path

source_path = Path(sys.argv[1])
snapshot_path = Path(sys.argv[2])

source = sqlite3.connect(source_path)
snapshot = sqlite3.connect(snapshot_path)

try:
    source.backup(
        snapshot,
        pages=4096,
        sleep=0.05,
    )
    snapshot.commit()

    result = snapshot.execute(
        "PRAGMA integrity_check"
    ).fetchone()[0]

    if result != "ok":
        raise RuntimeError(
            f"Snapshot integrity_check failed: {result}"
        )

finally:
    snapshot.close()
    source.close()

print("[OK] SQLite snapshot integrity_check: ok")
PY

echo
echo "[INFO] Compressing SQLite snapshot"

zstd -T0 -19 -f "$SNAPSHOT" -o "$COMPRESSED"

echo
echo "[INFO] Creating checksum"

(
  cd "$(dirname "$COMPRESSED")"
  sha256sum "$(basename "$COMPRESSED")"
) > "$CHECKSUM"

cat "$CHECKSUM"

echo
echo "[INFO] Local artifact sizes"

ls -lh "$STATE_DB" "$SNAPSHOT" "$COMPRESSED" "$CHECKSUM"

if [ "$UPLOAD_ENABLED" = "1" ]; then
  echo
  echo "[INFO] Ensuring remote folders"

  rclone mkdir "$REMOTE_PHASE"
  rclone mkdir "$REMOTE_LATEST"

  echo
  echo "[INFO] Uploading timestamped SQLite backup to selected drive only"

  rclone copy "$COMPRESSED" "$REMOTE_PHASE/" --progress
  rclone copy "$CHECKSUM" "$REMOTE_PHASE/" --progress

  echo
  echo "[INFO] Updating latest SQLite pointer on selected drive only"

  rclone copyto \
    "$COMPRESSED" \
    "$REMOTE_LATEST/wil-v3-rank-state.latest.sqlite.zst" \
    --progress

  rclone copyto \
    "$CHECKSUM" \
    "$REMOTE_LATEST/wil-v3-rank-state.latest.sqlite.zst.sha256" \
    --progress
else
  echo
  echo "[INFO] UPLOAD_ENABLED=0; remote upload skipped"
fi

echo
echo "[INFO] Writing local backup manifest"

python3 - \
  "$LOCAL_MANIFEST" \
  "$STATE_DB" \
  "$SNAPSHOT" \
  "$COMPRESSED" \
  "$CHECKSUM" \
  "$SYNC_PHASE" \
  "$PHASE_FOLDER" \
  "$USE_REMOTE" \
  "$REMOTE_PHASE" \
  "$REMOTE_LATEST" \
  "$PRIMARY_REMOTE_NAME" \
  "$SECONDARY_REMOTE_NAME" \
  "$PRIMARY_USED_PERCENT" \
  "$SELECTED_USED_PERCENT" \
  "$ROLLOVER_USED_PERCENT" \
  "$UPLOAD_ENABLED" <<'PY'
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

(
    manifest_path,
    state_db,
    snapshot,
    compressed,
    checksum,
    sync_phase,
    phase_folder,
    selected_remote,
    selected_remote_phase,
    selected_remote_latest,
    primary_remote,
    secondary_remote,
    primary_used_percent,
    selected_used_percent,
    rollover_used_percent,
    upload_enabled,
) = sys.argv[1:]

manifest = {
    "schema": "WIL_V3_GDRIVE_ROLLOVER_BACKUP_MANIFEST",
    "version": "v3.7.0",
    "state_backend": "SQLITE",
    "snapshot_method": "PYTHON_SQLITE_BACKUP_API",
    "created_at": datetime.now(
        timezone.utc
    ).replace(microsecond=0).isoformat(),
    "state_database": state_db,
    "snapshot_file": Path(snapshot).name,
    "compressed_file": Path(compressed).name,
    "checksum_file": Path(checksum).name,
    "sync_phase": sync_phase,
    "phase_folder": phase_folder,
    "selected_remote": selected_remote,
    "selected_remote_phase_path": selected_remote_phase,
    "selected_remote_latest_path": selected_remote_latest,
    "primary_remote": primary_remote,
    "secondary_remote": secondary_remote,
    "primary_used_percent_before_upload": primary_used_percent,
    "selected_used_percent_before_upload": selected_used_percent,
    "rollover_used_percent": rollover_used_percent,
    "upload_enabled": upload_enabled == "1",
    "snapshot_integrity_check": "ok",
}

Path(manifest_path).write_text(
    json.dumps(
        manifest,
        indent=2,
        sort_keys=True,
    ) + "\n",
    encoding="utf-8",
)

print(json.dumps(manifest, indent=2, sort_keys=True))
PY

if [ "$UPLOAD_ENABLED" = "1" ]; then
  echo
  echo "[INFO] Remote latest files"

  rclone ls "$REMOTE_LATEST"

  echo
  echo "[INFO] Recent files in phase folder"

  rclone lsf "$REMOTE_PHASE" | tail -10

  echo
  echo "[INFO] Selected remote quota after upload"

  rclone about "$USE_REMOTE:"
fi

echo
echo "[INFO] Cleaning local upload work older than ${KEEP_LOCAL_DAYS} days"

find "$WORK_DIR" \
  -type f \
  -name 'wil-v3-rank-state-*.sqlite' \
  -mtime +"$KEEP_LOCAL_DAYS" \
  -delete

find "$WORK_DIR" \
  -type f \
  -name 'wil-v3-rank-state-*.sqlite.zst' \
  -mtime +"$KEEP_LOCAL_DAYS" \
  -delete

find "$WORK_DIR" \
  -type f \
  -name 'wil-v3-rank-state-*.sqlite.zst.sha256' \
  -mtime +"$KEEP_LOCAL_DAYS" \
  -delete

echo
echo "[OK] WIL v3.7.0 SQLite GDrive rollover backup complete"
