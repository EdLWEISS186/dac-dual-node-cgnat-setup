#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.8.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
OUTPUT_DIR = BASE_DIR / "reports" / "generated" / "custom"


ENDPOINTS = [
    "official_public_rpc",
    "explorer_web",
    "primary_explorer_api",
]


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

    endpoint_rows = {
        key: [endpoint(row["data"], key) for row in rows]
        for key in ENDPOINTS
    }

    response_time_summary = {}

    for key, items in endpoint_rows.items():
        if key == "explorer_web":
            average_values = [item.get("latency_ms") for item in items]
            max_values = [item.get("latency_ms") for item in items]
        else:
            average_values = [item.get("latency_ms_avg") for item in items]
            max_values = [item.get("latency_ms_max") for item in items]

        response_time_summary[key] = {
            "average_response_ms": avg(average_values),
            "max_response_ms": max_value(max_values),
            "response_class_counts": count([item.get("latency_class") for item in items]),
        }

    return {
        "snapshot_count": len(rows),
        "first_snapshot": rows[0]["file"] if rows else None,
        "latest_snapshot": rows[-1]["file"] if rows else None,
        "first_checked_at_utc": rows[0]["data"].get("checked_at_utc") if rows else None,
        "latest_checked_at_utc": rows[-1]["data"].get("checked_at_utc") if rows else None,
        "overall_status_counts": count(overall_statuses),
        "endpoint_status_counts": {
            key: count([item.get("status") for item in items])
            for key, items in endpoint_rows.items()
        },
        "response_time_summary": response_time_summary,
    }


def build_timeline(rows):
    timeline = []

    for row in rows:
        data = row["data"]
        rpc = endpoint(data, "official_public_rpc")
        web = endpoint(data, "explorer_web")
        api = endpoint(data, "primary_explorer_api")

        timeline.append({
            "index": row["index"],
            "snapshot_file": row["file"],
            "checked_at_utc": data.get("checked_at_utc"),
            "overall_status": data.get("overall", {}).get("overall_status"),
            "official_public_rpc_status": rpc.get("status"),
            "official_public_rpc_response_class": rpc.get("latency_class"),
            "explorer_web_status": web.get("status"),
            "explorer_web_response_class": web.get("latency_class"),
            "primary_explorer_api_status": api.get("status"),
            "primary_explorer_api_response_class": api.get("latency_class"),
            "rpc_latest_block_decimal": rpc.get("latest_block_decimal"),
            "rpc_latest_block_hex": rpc.get("latest_block_hex"),
        })

    return timeline


def build_report_payload(rows, label):
    summary = summarize(rows)
    timeline = build_timeline(rows)

    return {
        "project": PROJECT,
        "report_type": "custom_range_infrastructure_report",
        "report_layer_version": VERSION,
        "range": label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "timeline": timeline,
        "interpretation_guide": [
            "Availability status describes whether a service is reachable and usable.",
            "Response class describes response-time behavior, not availability.",
            "Older snapshots may show UNKNOWN or null response class because response-time classification was added after the initial watcher release.",
            "This custom range report is independent observation material and not an official DAC service status page.",
        ],
        "prepared_by": "JERUZZALEM — DAC Infra Tester",
    }


def render_timeline_markdown(timeline):
    lines = [
        "| # | Checked at UTC | Overall | RPC | RPC class | Explorer Web | Web class | Explorer API | API class |",
        "|---:|---|---|---|---|---|---|---|---|",
    ]

    for item in timeline:
        lines.append(
            f"| {item.get('index')} | "
            f"{safe(item.get('checked_at_utc'))} | "
            f"{safe(item.get('overall_status'))} | "
            f"{safe(item.get('official_public_rpc_status'))} | "
            f"{safe(item.get('official_public_rpc_response_class'))} | "
            f"{safe(item.get('explorer_web_status'))} | "
            f"{safe(item.get('explorer_web_response_class'))} | "
            f"{safe(item.get('primary_explorer_api_status'))} | "
            f"{safe(item.get('primary_explorer_api_response_class'))} |"
        )

    return "\n".join(lines)


def build_markdown_report(payload):
    summary = payload["summary"]

    lines = [
        "# DAC Infrastructure Intelligence Watcher — Custom Range Report",
        "",
        f"Range: **{payload['range']}**",
        "",
        f"Report layer version: **{payload['report_layer_version']}**",
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
        lines.append(
            f"| {key} | "
            f"{safe(item.get('average_response_ms'))} ms | "
            f"{safe(item.get('max_response_ms'))} ms | "
            f"{safe(format_counts(item.get('response_class_counts')))} |"
        )

    lines.extend([
        "",
        "## 4. Snapshot Timeline",
        "",
        render_timeline_markdown(payload["timeline"]),
        "",
        "## 5. Interpretation Guide",
        "",
    ])

    for note in payload["interpretation_guide"]:
        lines.append(f"- {note}")

    lines.extend([
        "",
        "---",
        "",
        f"Prepared by **{payload['prepared_by']}**.",
        "",
    ])

    return "\n".join(lines)


def output_stem(label):
    safe_label = label.lower().replace(" ", "-").replace("_", "-").replace("#", "obs-")
    return f"infrastructure-report-{safe_label}"


def write_outputs(payload, output_format):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stem = output_stem(payload["range"])
    outputs = []

    if output_format in ("md", "both"):
        md_file = OUTPUT_DIR / f"{stem}.md"
        md_file.write_text(build_markdown_report(payload), encoding="utf-8")
        outputs.append(md_file)

    if output_format in ("json", "both"):
        json_file = OUTPUT_DIR / f"{stem}.json"
        json_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        outputs.append(json_file)

    return outputs


def main():
    parser = argparse.ArgumentParser(description="Generate DAC infrastructure custom range report.")
    parser.add_argument("--range", choices=["7d", "30d", "all"], help="Predefined snapshot time range.")
    parser.add_argument("--from", dest="from_index", help="Custom start snapshot index.")
    parser.add_argument("--to", dest="to_index", help="Custom end snapshot index.")
    parser.add_argument("--format", choices=["md", "json", "both"], default="md", help="Output format. Default: md.")
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

    payload = build_report_payload(selected, label)
    outputs = write_outputs(payload, args.format)

    print("[OK] Custom infrastructure range report generated.")
    print(f"[OK] Range: {label}")
    print(f"[OK] Format: {args.format}")
    print(f"[OK] Snapshot count: {len(selected)}")

    for output in outputs:
        print(f"[OK] Output: {output}")


if __name__ == "__main__":
    main()
