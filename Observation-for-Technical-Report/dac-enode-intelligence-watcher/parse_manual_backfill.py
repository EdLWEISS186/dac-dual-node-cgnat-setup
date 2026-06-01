import re
import json
from pathlib import Path
from datetime import datetime


PROJECT_NAME = "DAC Enode Intelligence Watcher"
SOURCE_TYPE = "pre_watcher_manual_backfill"
SOURCE_FILE = "manual-archive/Old Data Before Intelligence Watcher Created.txt"

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / SOURCE_FILE
OUTPUT_DIR = BASE_DIR / "data" / "manual-backfill"
SUMMARY_FILE = OUTPUT_DIR / "manual-backfill-summary.json"

HEADER_REGEX = re.compile(
    r"Generated:\s*(.*?)\s*\|\s*Target Port:?\s*(\d+)",
    re.IGNORECASE
)

ENODE_REGEX = re.compile(
    r'enode://[0-9a-fA-F]+@[^\s"\')]+',
    re.IGNORECASE
)

DATE_REGEX = re.compile(
    r"(?P<weekday>\w+)\s+"
    r"(?P<month>\w+)\s+"
    r"(?P<day>\d{1,2})\s+"
    r"(?P<hour>\d{1,2}):(?P<minute>\d{2}):(?P<second>\d{2})\s+"
    r"(?P<ampm>AM|PM)\s+"
    r"(?P<tz>\w+)\s+"
    r"(?P<year>\d{4})",
    re.IGNORECASE
)

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def dedupe_preserve_order(items):
    seen = set()
    output = []

    for item in items:
        if item not in seen:
            seen.add(item)
            output.append(item)

    return output


def parse_generated_time(raw_generated):
    match = DATE_REGEX.search(raw_generated)

    if not match:
        return {
            "raw": raw_generated,
            "date": None,
            "time": None,
            "timezone": None,
            "filename_time": raw_generated.replace(" ", "_").replace(":", "-")
        }

    month = MONTHS[match.group("month").lower()[:3]]
    day = int(match.group("day"))
    year = int(match.group("year"))

    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    second = int(match.group("second"))
    ampm = match.group("ampm").upper()
    timezone_name = match.group("tz").upper()

    if ampm == "AM" and hour == 12:
        hour = 0
    elif ampm == "PM" and hour != 12:
        hour += 12

    dt = datetime(year, month, day, hour, minute, second)

    return {
        "raw": raw_generated,
        "date": dt.date().isoformat(),
        "time": dt.time().isoformat(),
        "timezone": timezone_name,
        "filename_time": f"{dt.strftime('%Y-%m-%dT%H-%M-%S')}-{timezone_name}"
    }


def parse_enode_details(enode):
    try:
        without_prefix = enode.replace("enode://", "")
        node_id, endpoint = without_prefix.split("@", 1)
        ip, port = endpoint.rsplit(":", 1)

        return {
            "enode": enode,
            "node_id": node_id,
            "ip": ip,
            "port": int(port)
        }
    except Exception:
        return {
            "enode": enode,
            "node_id": None,
            "ip": None,
            "port": None
        }


def admin_addpeer_line(enode):
    return f'admin.addPeer("{enode}");'


def build_snapshot(index, header_match, block_text, previous_snapshot):
    generated_raw = header_match.group(1).strip()
    target_port = int(header_match.group(2))
    generated = parse_generated_time(generated_raw)

    current_enodes = dedupe_preserve_order(ENODE_REGEX.findall(block_text))
    previous_enodes = previous_snapshot["enodes"] if previous_snapshot else []

    current_set = set(current_enodes)
    previous_set = set(previous_enodes)

    added = sorted(current_set - previous_set)
    removed = sorted(previous_set - current_set)
    unchanged = sorted(current_set & previous_set)

    previous_target_port = previous_snapshot["target_port"] if previous_snapshot else None
    target_port_changed = (
        previous_snapshot is not None
        and previous_target_port != target_port
    )

    if previous_snapshot is None:
        status = "manual_initial"
    elif added or removed or target_port_changed:
        status = "manual_changed"
    else:
        status = "manual_unchanged"

    snapshot_file = f"data/manual-backfill/{generated['filename_time']}-manual.json"

    snapshot = {
        "project": PROJECT_NAME,
        "source_type": SOURCE_TYPE,
        "source_file": SOURCE_FILE,
        "status": status,
        "manual_snapshot_index": index,
        "observation_completeness": "partial_manual_archive",
        "data_gap_note": "This snapshot belongs to the pre-watcher manual observation period. Missing days represent missed observation windows, not confirmed absence of changes.",

        "generated_at_source": generated_raw,
        "generated_date": generated["date"],
        "generated_time": generated["time"],
        "generated_timezone": generated["timezone"],

        "target_port": target_port,
        "previous_target_port": previous_target_port,
        "current_target_port": target_port,
        "target_port_changed": target_port_changed,

        "previous_total": len(previous_enodes),
        "current_total": len(current_enodes),

        "added_count": len(added),
        "removed_count": len(removed),
        "unchanged_count": len(unchanged),

        "added": added,
        "removed": removed,
        "unchanged": unchanged,
        "enodes": current_enodes,

        "added_details": [parse_enode_details(e) for e in added],
        "removed_details": [parse_enode_details(e) for e in removed],
        "unchanged_details": [parse_enode_details(e) for e in unchanged],
        "enode_details": [parse_enode_details(e) for e in current_enodes],

        "added_admin_addpeer_lines": [admin_addpeer_line(e) for e in added],
        "removed_admin_addpeer_lines": [admin_addpeer_line(e) for e in removed],
        "unchanged_admin_addpeer_lines": [admin_addpeer_line(e) for e in unchanged],
        "admin_addpeer_lines": [admin_addpeer_line(e) for e in current_enodes],

        "snapshot_file": snapshot_file
    }

    return snapshot


def save_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    text = INPUT_FILE.read_text(encoding="utf-8", errors="replace")
    headers = list(HEADER_REGEX.finditer(text))

    if not headers:
        raise RuntimeError("No manual snapshot headers found.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    snapshots = []
    previous_snapshot = None

    for index, header in enumerate(headers, start=1):
        start = header.start()
        end = headers[index].start() if index < len(headers) else len(text)
        block_text = text[start:end]

        snapshot = build_snapshot(index, header, block_text, previous_snapshot)
        snapshots.append(snapshot)
        previous_snapshot = snapshot

        output_path = BASE_DIR / snapshot["snapshot_file"]
        save_json(output_path, snapshot)

    all_enodes = sorted({enode for snapshot in snapshots for enode in snapshot["enodes"]})
    target_ports = sorted({snapshot["target_port"] for snapshot in snapshots})

    summary = {
        "project": PROJECT_NAME,
        "source_type": SOURCE_TYPE,
        "source_file": SOURCE_FILE,
        "observation_completeness": "partial_manual_archive",
        "data_gap_note": "This summary covers manually captured observations before the automated watcher was created. Missing dates represent missed observation windows.",
        "total_manual_snapshots": len(snapshots),
        "first_generated_at_source": snapshots[0]["generated_at_source"],
        "last_generated_at_source": snapshots[-1]["generated_at_source"],
        "first_generated_date": snapshots[0]["generated_date"],
        "last_generated_date": snapshots[-1]["generated_date"],
        "target_ports_observed": target_ports,
        "unique_enode_count": len(all_enodes),
        "min_enode_count": min(snapshot["current_total"] for snapshot in snapshots),
        "max_enode_count": max(snapshot["current_total"] for snapshot in snapshots),
        "snapshots": [
            {
                "manual_snapshot_index": snapshot["manual_snapshot_index"],
                "generated_at_source": snapshot["generated_at_source"],
                "target_port": snapshot["target_port"],
                "current_total": snapshot["current_total"],
                "added_count": snapshot["added_count"],
                "removed_count": snapshot["removed_count"],
                "unchanged_count": snapshot["unchanged_count"],
                "status": snapshot["status"],
                "snapshot_file": snapshot["snapshot_file"]
            }
            for snapshot in snapshots
        ],
        "unique_enodes": all_enodes,
        "manual_snapshot_files": [snapshot["snapshot_file"] for snapshot in snapshots]
    }

    save_json(SUMMARY_FILE, summary)

    print(f"[OK] Parsed manual snapshots: {len(snapshots)}")
    print(f"[OK] Unique enodes observed: {len(all_enodes)}")
    print(f"[OK] Target ports observed: {target_ports}")
    print(f"[OK] Output directory: {OUTPUT_DIR}")
    print(f"[OK] Summary file: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
