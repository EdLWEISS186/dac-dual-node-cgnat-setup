#!/usr/bin/env python3

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.8.1"

BASE_DIR = Path(__file__).resolve().parent
SNAPSHOT_DIR = BASE_DIR / "data" / "snapshots"
OUTPUT_DIR = BASE_DIR / "reports" / "generated" / "comparison"


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


def as_number(value):
    if value is None or value == "":
        return None

    try:
        return float(value)
    except Exception:
        return None


def average(values):
    clean = [as_number(value) for value in values]
    clean = [value for value in clean if value is not None]

    if not clean:
        return None

    return round(sum(clean) / len(clean), 2)


def maximum(values):
    clean = [as_number(value) for value in values]
    clean = [value for value in clean if value is not None]

    if not clean:
        return None

    return round(max(clean), 2)


def count_values(values):
    counts = {}

    for value in values:
        key = value or "UNKNOWN"
        counts[key] = counts.get(key, 0) + 1

    return dict(sorted(counts.items()))


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

        rows.append({
            "index": index,
            "file": path.name,
            "path": path,
            "checked_at": parse_dt(data.get("checked_at_utc")),
            "data": data,
        })

    return rows


def endpoint(data, key):
    return data.get("endpoints", {}).get(key, {})


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


def split_rows(rows):
    if len(rows) < 2:
        raise SystemExit("At least 2 snapshots are required for comparison.")

    midpoint = len(rows) // 2
    return rows[:midpoint], rows[midpoint:]


def summarize_window(rows):
    overall_statuses = [
        row["data"].get("overall", {}).get("overall_status")
        for row in rows
    ]

    endpoint_status_counts = {}
    endpoint_response_summary = {}

    for key in ENDPOINTS:
        endpoint_rows = [endpoint(row["data"], key) for row in rows]

        endpoint_status_counts[key] = count_values([
            item.get("status")
            for item in endpoint_rows
        ])

        if key == "explorer_web":
            response_values = [item.get("latency_ms") for item in endpoint_rows]
            max_response_values = [item.get("latency_ms") for item in endpoint_rows]
        else:
            response_values = [item.get("latency_ms_avg") for item in endpoint_rows]
            max_response_values = [item.get("latency_ms_max") for item in endpoint_rows]

        endpoint_response_summary[key] = {
            "average_response_ms": average(response_values),
            "max_response_ms": maximum(max_response_values),
            "response_class_counts": count_values([
                item.get("latency_class")
                for item in endpoint_rows
            ]),
        }

    return {
        "snapshot_count": len(rows),
        "first_index": rows[0]["index"] if rows else None,
        "latest_index": rows[-1]["index"] if rows else None,
        "first_checked_at_utc": rows[0]["data"].get("checked_at_utc") if rows else None,
        "latest_checked_at_utc": rows[-1]["data"].get("checked_at_utc") if rows else None,
        "overall_status_counts": count_values(overall_statuses),
        "endpoint_status_counts": endpoint_status_counts,
        "endpoint_response_summary": endpoint_response_summary,
    }


def score_availability(summary):
    counts = summary.get("overall_status_counts", {})
    total = summary.get("snapshot_count") or 1

    healthy = counts.get("HEALTHY", 0)
    degraded = counts.get("DEGRADED", 0)
    partial = counts.get("PARTIAL_OUTAGE", 0)
    unhealthy = counts.get("UNHEALTHY", 0)

    return round(
        ((healthy * 1.0) + (degraded * 0.55) + (partial * 0.2) + (unhealthy * 0.0)) / total,
        4,
    )


def compare_direction(a_value, b_value, lower_is_better=False):
    if a_value is None or b_value is None:
        return "N/A"

    if b_value == a_value:
        return "UNCHANGED"

    if lower_is_better:
        return "IMPROVED" if b_value < a_value else "WORSENED"

    return "IMPROVED" if b_value > a_value else "WORSENED"


def build_interpretation(summary_a, summary_b):
    score_a = score_availability(summary_a)
    score_b = score_availability(summary_b)

    availability_direction = compare_direction(score_a, score_b)

    rpc_a = summary_a["endpoint_response_summary"]["official_public_rpc"].get("average_response_ms")
    rpc_b = summary_b["endpoint_response_summary"]["official_public_rpc"].get("average_response_ms")
    rpc_response_direction = compare_direction(rpc_a, rpc_b, lower_is_better=True)

    web_a = summary_a["endpoint_response_summary"]["explorer_web"].get("average_response_ms")
    web_b = summary_b["endpoint_response_summary"]["explorer_web"].get("average_response_ms")
    web_response_direction = compare_direction(web_a, web_b, lower_is_better=True)

    api_a = summary_a["endpoint_response_summary"]["primary_explorer_api"].get("average_response_ms")
    api_b = summary_b["endpoint_response_summary"]["primary_explorer_api"].get("average_response_ms")
    api_response_direction = compare_direction(api_a, api_b, lower_is_better=True)

    notes = [
        f"Overall availability score changed from {score_a} to {score_b}: {availability_direction}.",
        f"Official Public RPC average response changed from {safe(rpc_a)} ms to {safe(rpc_b)} ms: {rpc_response_direction}.",
        f"Explorer Web average response changed from {safe(web_a)} ms to {safe(web_b)} ms: {web_response_direction}.",
        f"Primary Explorer API average response changed from {safe(api_a)} ms to {safe(api_b)} ms: {api_response_direction}.",
    ]

    if availability_direction == "WORSENED":
        notes.append("The later observation window shows weaker overall infrastructure availability.")
    elif availability_direction == "IMPROVED":
        notes.append("The later observation window shows stronger overall infrastructure availability.")
    else:
        notes.append("The later observation window shows no major overall availability change.")

    return notes


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


def build_payload(label, rows_a, rows_b):
    summary_a = summarize_window(rows_a)
    summary_b = summarize_window(rows_b)

    return {
        "project": PROJECT,
        "report_type": "observation_window_comparison",
        "comparison_layer_version": VERSION,
        "comparison_scope": label,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "window_a": {
            "label": "Window A",
            "description": "Earlier observation segment.",
            "summary": summary_a,
            "timeline": build_timeline(rows_a),
        },
        "window_b": {
            "label": "Window B",
            "description": "Later observation segment.",
            "summary": summary_b,
            "timeline": build_timeline(rows_b),
        },
        "comparison": {
            "availability_score_a": score_availability(summary_a),
            "availability_score_b": score_availability(summary_b),
            "availability_direction": compare_direction(score_availability(summary_a), score_availability(summary_b)),
            "interpretation": build_interpretation(summary_a, summary_b),
        },
        "interpretation_guide": [
            "Window A represents the earlier observation segment.",
            "Window B represents the later observation segment.",
            "For availability score, higher is better.",
            "For response time, lower is better.",
            "Older snapshots may show N/A or UNKNOWN response classes because response-time classification was added after the initial watcher release.",
            "This comparison report is independent observation material and not an official DAC service status page.",
        ],
        "prepared_by": "JERUZZALEM — DAC Infra Tester",
    }


def render_summary_table(title, summary):
    lines = [
        f"### {title}",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Snapshot count | {safe(summary.get('snapshot_count'))} |",
        f"| Observation index range | {safe(summary.get('first_index'))} -> {safe(summary.get('latest_index'))} |",
        f"| First checked at UTC | {safe(summary.get('first_checked_at_utc'))} |",
        f"| Latest checked at UTC | {safe(summary.get('latest_checked_at_utc'))} |",
        f"| Overall status counts | {safe(format_counts(summary.get('overall_status_counts')))} |",
        f"| Availability score | {safe(score_availability(summary))} |",
        "",
    ]

    return "\n".join(lines)


def render_endpoint_comparison(summary_a, summary_b):
    lines = [
        "| Endpoint | Window A status counts | Window B status counts | Window A avg response | Window B avg response | Direction |",
        "|---|---|---|---:|---:|---|",
    ]

    for key in ENDPOINTS:
        a_response = summary_a["endpoint_response_summary"][key].get("average_response_ms")
        b_response = summary_b["endpoint_response_summary"][key].get("average_response_ms")
        direction = compare_direction(a_response, b_response, lower_is_better=True)

        lines.append(
            f"| {key} | "
            f"{safe(format_counts(summary_a['endpoint_status_counts'].get(key)))} | "
            f"{safe(format_counts(summary_b['endpoint_status_counts'].get(key)))} | "
            f"{safe(a_response)} ms | "
            f"{safe(b_response)} ms | "
            f"{safe(direction)} |"
        )

    return "\n".join(lines)


def render_response_class_comparison(summary_a, summary_b):
    lines = [
        "| Endpoint | Window A response classes | Window B response classes | Window A max response | Window B max response |",
        "|---|---|---|---:|---:|",
    ]

    for key in ENDPOINTS:
        a_item = summary_a["endpoint_response_summary"][key]
        b_item = summary_b["endpoint_response_summary"][key]

        lines.append(
            f"| {key} | "
            f"{safe(format_counts(a_item.get('response_class_counts')))} | "
            f"{safe(format_counts(b_item.get('response_class_counts')))} | "
            f"{safe(a_item.get('max_response_ms'))} ms | "
            f"{safe(b_item.get('max_response_ms'))} ms |"
        )

    return "\n".join(lines)


def render_timeline(title, timeline):
    lines = [
        f"### {title}",
        "",
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
    summary_a = payload["window_a"]["summary"]
    summary_b = payload["window_b"]["summary"]

    lines = [
        "# DAC Infrastructure Intelligence Watcher — Observation Window Comparison",
        "",
        f"Comparison scope: **{payload['comparison_scope']}**",
        "",
        f"Comparison layer version: **{payload['comparison_layer_version']}**",
        "",
        "This report compares two infrastructure observation windows derived from tracked health snapshots.",
        "",
        "---",
        "",
        "## 1. Window Summary",
        "",
        render_summary_table("Window A", summary_a),
        render_summary_table("Window B", summary_b),
        "## 2. Endpoint Availability and Response Comparison",
        "",
        render_endpoint_comparison(summary_a, summary_b),
        "",
        "## 3. Response Class Comparison",
        "",
        render_response_class_comparison(summary_a, summary_b),
        "",
        "## 4. Interpretation",
        "",
    ]

    for note in payload["comparison"]["interpretation"]:
        lines.append(f"- {note}")

    lines.extend([
        "",
        "## 5. Window Timelines",
        "",
        render_timeline("Window A Timeline", payload["window_a"]["timeline"]),
        "",
        render_timeline("Window B Timeline", payload["window_b"]["timeline"]),
        "",
        "## 6. Interpretation Guide",
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
    safe_label = label.lower().replace(" ", "-").replace("_", "-")
    return f"infrastructure-comparison-{safe_label}"


def write_outputs(payload, output_format):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    stem = output_stem(payload["comparison_scope"])
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
    parser = argparse.ArgumentParser(description="Compare DAC infrastructure observation windows.")
    parser.add_argument("--range", choices=["7d", "30d", "all"], help="Predefined range to split into two comparison windows.")
    parser.add_argument("--a-from", dest="a_from", help="Window A start snapshot index.")
    parser.add_argument("--a-to", dest="a_to", help="Window A end snapshot index.")
    parser.add_argument("--b-from", dest="b_from", help="Window B start snapshot index.")
    parser.add_argument("--b-to", dest="b_to", help="Window B end snapshot index.")
    parser.add_argument("--format", choices=["md", "json", "both"], default="md", help="Output format. Default: md.")
    args = parser.parse_args()

    rows = load_snapshots()

    if args.range:
        selected = filter_by_range(rows, args.range)
        rows_a, rows_b = split_rows(selected)
        label = args.range
    elif args.a_from and args.a_to and args.b_from and args.b_to:
        rows_a = filter_by_index(rows, args.a_from, args.a_to)
        rows_b = filter_by_index(rows, args.b_from, args.b_to)
        label = f"custom-a-{args.a_from}-to-{args.a_to}-vs-b-{args.b_from}-to-{args.b_to}"

        if not rows_a or not rows_b:
            raise SystemExit("Custom comparison windows must both contain at least one snapshot.")
    else:
        raise SystemExit("Use --range 7d|30d|all or --a-from/--a-to/--b-from/--b-to.")

    payload = build_payload(label, rows_a, rows_b)
    outputs = write_outputs(payload, args.format)

    print("[OK] Infrastructure observation comparison report generated.")
    print(f"[OK] Scope: {label}")
    print(f"[OK] Format: {args.format}")
    print(f"[OK] Window A snapshots: {len(rows_a)}")
    print(f"[OK] Window B snapshots: {len(rows_b)}")

    for output in outputs:
        print(f"[OK] Output: {output}")


if __name__ == "__main__":
    main()
