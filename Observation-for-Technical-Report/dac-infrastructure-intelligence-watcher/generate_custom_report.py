#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.4.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
OUTPUT_DIR = BASE_DIR / "reports" / "generated" / "custom"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_dt(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def safe(value, fallback="N/A"):
    if value is None or value == "":
        return fallback
    return str(value).replace("|", "\\|")


def safe_number(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except Exception:
        return None


def avg(values):
    clean = [safe_number(value) for value in values]
    clean = [value for value in clean if value is not None]

    if not clean:
        return None

    return round(sum(clean) / len(clean), 2)


def max_value(values):
    clean = [safe_number(value) for value in values]
    clean = [value for value in clean if value is not None]

    if not clean:
        return None

    return round(max(clean), 2)


def count(values):
    output = {}

    for value in values:
        key = value or "UNKNOWN"
        output[key] = output.get(key, 0) + 1

    return dict(sorted(output.items()))


def format_counts(counts):
    if not counts:
        return "N/A"

    return ", ".join(f"{key}: {value}" for key, value in counts.items())


def load_snapshots():
    rows = []

    for index, path in enumerate(sorted(SNAPSHOT_DIR.glob("*.json")), start=1):
        try:
            data = load_json(path)
        except Exception:
            continue

        checked_at = parse_dt(data.get("checked_at_utc"))

        rows.append({
            "index": index,
            "path": path,
            "file": path.name,
            "checked_at": checked_at,
            "data": data,
        })

    return rows


def filter_by_range(rows, range_name):
    if range_name == "all":
        return rows

    now = datetime.now(timezone.utc)

    if range_name == "7d":
        cutoff = now - timedelta(days=7)
    elif range_name == "30d":
        cutoff = now - timedelta(days=30)
    else:
        raise ValueError(f"Unsupported range: {range_name}")

    return [
        row for row in rows
        if row["checked_at"] is not None and row["checked_at"] >= cutoff
    ]


def filter_by_index(rows, start_index, end_index):
    start = int(start_index)
    end = int(end_index)

    if start > end:
        start, end = end, start

    return [
        row for row in rows
        if start <= row["index"] <= end
    ]


def endpoint(data, key):
    return data.get("endpoints", {}).get(key, {})


def summarize(rows):
    overall_statuses = [
        row["data"].get("overall", {}).get("overall_status")
        for row in rows
    ]

    rpc_rows = [endpoint(row["data"], "official_public_rpc") for row in rows]
    web_rows = [endpoint(row["data"], "explorer_web") for row in rows]
    api_rows = [endpoint(row["data"], "primary_explorer_api") for row in rows]

    return {
        "snapshot_count": len(rows),
        "first_snapshot": rows[0]["file"] if rows else None,
        "latest_snapshot": rows[-1]["file"] if rows else None,
        "first_checked_at_utc": rows[0]["data"].get("checked_at_utc") if rows else None,
        "latest_checked_at_utc": rows[-1]["data"].get("checked_at_utc") if rows else None,
        "overall_status_counts": count(overall_statuses),
        "endpoint_status_counts": {
            "official_public_rpc": count([item.get("status") for item in rpc_rows]),
            "explorer_web": count([item.get("status") for item in web_rows]),
            "primary_explorer_api": count([item.get("status") for item in api_rows]),
        },
        "response_time_summary": {
            "official_public_rpc": {
                "avg_response_ms_avg": avg([item.get("latency_ms_avg") for item in rpc_rows]),
                "max_response_ms": max_value([item.get("latency_ms_max") for item in rpc_rows]),
                "response_class_counts": count([item.get("latency_class") for item in rpc_rows]),
            },
            "explorer_web": {
                "avg_response_ms": avg([item.get("latency_ms") for item in web_rows]),
                "max_response_ms": max_value([item.get("latency_ms") for item in web_rows]),
                "response_class_counts": count([item.get("latency_class") for item in web_rows]),
            },
            "primary_explorer_api": {
                "avg_response_ms_avg": avg([item.get("latency_ms_avg") for item in api_rows]),
                "max_response_ms": max_value([item.get("latency_ms_max") for item in api_rows]),
                "response_class_counts": count([item.get("latency_class") for item in api_rows]),
            },
        },
    }


def build_timeline(rows):
    lines = [
        "| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]

    for row in rows:
        data = row["data"]
        rpc = endpoint(data, "official_public_rpc")
        web = endpoint(data, "explorer_web")
        api = endpoint(data, "primary_explorer_api")

        lines.append(
            f"| {row['index']} | "
            f"{safe(data.get('checked_at_utc'))} | "
            f"{safe(data.get('overall', {}).get('overall_status'))} | "
            f"{safe(rpc.get('status'))} | "
            f"{safe(rpc.get('latency_class'))} | "
            f"{safe(web.get('status'))} | "
            f"{safe(web.get('latency_class'))} | "
            f"{safe(api.get('status'))} | "
            f"{safe(api.get('latency_class'))} |"
        )

    return "\n".join(lines)


def build_report(rows, label):
    summary = summarize(rows)

    lines = [
        f"# DAC Infrastructure Intelligence Watcher — Custom Range Report",
        "",
        f"Range: **{label}**",
        "",
        f"Report layer version: **{VERSION}**",
        "",
        "This report is generated from infrastructure health snapshots and is intended for range-based technical review.",
        "",
        "---",
        "",
        "## 1. Range Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Project | {PROJECT} |",
        f"| Snapshot count | {safe(summary['snapshot_count'])} |",
        f"| First snapshot | {safe(summary['first_snapshot'])} |",
        f"| Latest snapshot | {safe(summary['latest_snapshot'])} |",
        f"| First checked at UTC | {safe(summary['first_checked_at_utc'])} |",
        f"| Latest checked at UTC | {safe(summary['latest_checked_at_utc'])} |",
        f"| Overall status counts | {safe(format_counts(summary['overall_status_counts']))} |",
        "",
        "## 2. Endpoint Status Counts",
        "",
        "| Endpoint | Status counts |",
        "|---|---|",
    ]

    for key, counts in summary["endpoint_status_counts"].items():
        lines.append(f"| {key} | {safe(format_counts(counts))} |")

    lines.extend([
        "",
        "## 3. Response-Time Summary",
        "",
        "| Endpoint | Average response | Max response | Response class counts |",
        "|---|---:|---:|---|",
    ])

    for key, item in summary["response_time_summary"].items():
        avg_response = item.get("avg_response_ms_avg", item.get("avg_response_ms"))
        lines.append(
            f"| {key} | "
            f"{safe(avg_response)} ms | "
            f"{safe(item.get('max_response_ms'))} ms | "
            f"{safe(format_counts(item.get('response_class_counts')))} |"
        )

    lines.extend([
        "",
        "## 4. Snapshot Timeline",
        "",
        build_timeline(rows),
        "",
        "## 5. Interpretation Guide",
        "",
        "- Availability status describes whether a service is reachable and usable.",
        "- Response class describes response-time behavior, not availability.",
        "- Older snapshots may show `N/A` response class because response-time classification was added after the initial watcher release.",
        "- This custom range report is independent observation material and not an official DAC service status page.",
        "",
        "---",
        "",
        "Prepared by **JERUZZALEM — DAC Infra Tester**.",
        "",
    ])

    return "\n".join(lines)


def output_name(label):
    safe_label = label.lower().replace(" ", "-").replace("_", "-").replace("#", "obs-")
    return f"infrastructure-report-{safe_label}.md"


def main():
    parser = argparse.ArgumentParser(description="Generate DAC infrastructure custom range report.")
    parser.add_argument("--range", choices=["7d", "30d", "all"], help="Predefined snapshot time range.")
    parser.add_argument("--from", dest="from_index", help="Custom start snapshot index.")
    parser.add_argument("--to", dest="to_index", help="Custom end snapshot index.")
    args = parser.parse_args()

    rows = load_snapshots()

    if args.range:
        selected = filter_by_range(rows, args.range)
        label = args.range
    elif args.from_index and args.to_index:
        selected = filter_by_index(rows, args.from_index, args.to_index)
        label = f"custom-obs-{args.from_index}-to-{args.to_index}"
    else:
        raise SystemExit("Use --range 7d|30d|all or --from INDEX --to INDEX.")

    if not selected:
        raise SystemExit(f"No snapshots matched range: {label}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    report = build_report(selected, label)
    output_file = OUTPUT_DIR / output_name(label)
    output_file.write_text(report, encoding="utf-8")

    print("[OK] Custom infrastructure range report generated.")
    print(f"[OK] Range: {label}")
    print(f"[OK] Snapshot count: {len(selected)}")
    print(f"[OK] Output: {output_file}")


if __name__ == "__main__":
    main()
