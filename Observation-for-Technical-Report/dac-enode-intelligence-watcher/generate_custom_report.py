import argparse
import json
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports" / "generated" / "custom"

LATEST_FILE = DATA_DIR / "latest.json"
ROTATION_FILE = DATA_DIR / "rotation-intelligence-summary.json"
ANOMALY_FILE = DATA_DIR / "anomaly-detection-summary.json"
CONCENTRATION_FILE = DATA_DIR / "concentration-risk-summary.json"

RANGE_OPTIONS = {"7d", "30d", "all"}
FORMAT_OPTIONS = {"markdown", "json", "both"}

MONTH_INDEX = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12,
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_source_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None

    pattern = (
        r"^[A-Za-z]{3}\s+"
        r"([A-Za-z]{3})\s+"
        r"(\d{1,2})\s+"
        r"(\d{1,2}):(\d{2}):(\d{2})\s+"
        r"(AM|PM)\s+"
        r"([A-Z]{2,5})\s+"
        r"(\d{4})$"
    )

    match = re.match(pattern, value.strip())
    if not match:
        return None

    month_name, day, hour, minute, second, meridiem, _timezone_name, year = match.groups()

    month = MONTH_INDEX.get(month_name)
    if not month:
        return None

    hour_num = int(hour)
    if meridiem == "AM" and hour_num == 12:
        hour_num = 0
    elif meridiem == "PM" and hour_num != 12:
        hour_num += 12

    return datetime(
        int(year),
        month,
        int(day),
        hour_num,
        int(minute),
        int(second),
        tzinfo=timezone.utc,
    )


def format_source_time(value: str | None) -> str:
    if not value:
        return "N/A"

    parsed = parse_source_timestamp(value)
    if not parsed:
        return value

    match = re.search(r"(\d{1,2}):(\d{2}):(\d{2})\s+(AM|PM)\s+([A-Z]{2,5})", value)
    timezone_name = match.group(5) if match else "UTC"

    return f"{parsed.strftime('%b')} {parsed.day}, {parsed.year} ({parsed.strftime('%H:%M')} {timezone_name})"


def filter_timeline_by_range(timeline: list[dict], selected_range: str) -> list[dict]:
    if selected_range == "all":
        return timeline

    dated_items = []
    for item in timeline:
        parsed = parse_source_timestamp(item.get("generated_at_source"))
        if parsed:
            dated_items.append((parsed, item))

    if not dated_items:
        return timeline

    latest_time = max(parsed for parsed, _item in dated_items)
    days = 7 if selected_range == "7d" else 30
    cutoff = latest_time - timedelta(days=days)

    filtered = [item for parsed, item in dated_items if parsed >= cutoff]
    return filtered or timeline


def count_by(items: list[dict], key: str) -> dict:
    counts = Counter(item.get(key) or "Unknown" for item in items)
    return dict(counts)


def table(headers: list[str], rows: list[list[object]]) -> str:
    normalized_rows = [[str(cell) if cell is not None else "N/A" for cell in row] for row in rows]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]

    for row in normalized_rows:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def section(title: str) -> str:
    return f"\n## {title}\n"


def range_title(selected_range: str) -> str:
    if selected_range == "7d":
        return "Last 7 Days"
    if selected_range == "30d":
        return "Last 30 Days"
    return "All Time"


def summarize_timeline(timeline: list[dict]) -> dict:
    if not timeline:
        return {
            "observations": 0,
            "first_source_time": "N/A",
            "last_source_time": "N/A",
            "min_enodes": "N/A",
            "max_enodes": "N/A",
            "avg_enodes": "N/A",
            "total_added": 0,
            "total_removed": 0,
            "target_ports": [],
            "phase_counts": {},
            "status_counts": {},
        }

    totals = [int(item.get("current_total") or 0) for item in timeline]
    added = sum(int(item.get("added_count") or 0) for item in timeline)
    removed = sum(int(item.get("removed_count") or 0) for item in timeline)

    return {
        "observations": len(timeline),
        "first_source_time": format_source_time(timeline[0].get("generated_at_source")),
        "last_source_time": format_source_time(timeline[-1].get("generated_at_source")),
        "min_enodes": min(totals),
        "max_enodes": max(totals),
        "avg_enodes": round(sum(totals) / len(totals), 2),
        "total_added": added,
        "total_removed": removed,
        "target_ports": sorted(set(item.get("target_port") for item in timeline if item.get("target_port"))),
        "phase_counts": count_by(timeline, "phase"),
        "status_counts": count_by(timeline, "status"),
    }


def filter_anomalies_by_timeline(anomalies: list[dict], timeline: list[dict]) -> list[dict]:
    timeline_indexes = {item.get("observation_index") for item in timeline}

    return [
        anomaly
        for anomaly in anomalies
        if anomaly.get("observation", {}).get("observation_index") in timeline_indexes
    ]



def build_custom_summary_data(selected_range: str) -> dict:
    latest = load_json(LATEST_FILE)
    rotation = load_json(ROTATION_FILE)
    anomaly = load_json(ANOMALY_FILE)
    concentration = load_json(CONCENTRATION_FILE)

    timeline = rotation.get("observation_timeline", [])
    selected_timeline = filter_timeline_by_range(timeline, selected_range)

    timeline_summary = summarize_timeline(selected_timeline)
    selected_anomalies = filter_anomalies_by_timeline(anomaly.get("anomalies", []), selected_timeline)

    selected_severity_counts = Counter(item.get("severity") or "Unknown" for item in selected_anomalies)
    selected_anomaly_type_counts = Counter(item.get("anomaly_type") or "Unknown" for item in selected_anomalies)

    concentration_report = concentration.get("report_ready_summary", {})

    timeline_rows = []
    for item in selected_timeline:
        timeline_rows.append({
            "observation_index": item.get("observation_index"),
            "phase": item.get("phase"),
            "status": item.get("status"),
            "source_time_raw": item.get("generated_at_source"),
            "source_time_readable": format_source_time(item.get("generated_at_source")),
            "checked_at_utc": item.get("checked_at_utc"),
            "current_total": item.get("current_total"),
            "previous_total": item.get("previous_total"),
            "added_count": item.get("added_count"),
            "removed_count": item.get("removed_count"),
            "unchanged_count": item.get("unchanged_count"),
            "target_port": item.get("target_port"),
            "change_severity": item.get("change_severity"),
            "severity_reason": item.get("severity_reason"),
            "snapshot_file": item.get("snapshot_file"),
        })

    anomaly_rows = []
    for item in selected_anomalies:
        observation = item.get("observation", {})
        anomaly_rows.append({
            "anomaly_type": item.get("anomaly_type"),
            "severity": item.get("severity"),
            "reason": item.get("reason"),
            "technical_impact": item.get("technical_impact"),
            "recommended_action": item.get("recommended_action"),
            "observation_index": observation.get("observation_index"),
            "phase": observation.get("phase"),
            "source_time_raw": observation.get("generated_at_source"),
            "source_time_readable": format_source_time(observation.get("generated_at_source")),
            "current_total": observation.get("current_total"),
            "previous_total": observation.get("previous_total"),
            "added_count": observation.get("added_count"),
            "removed_count": observation.get("removed_count"),
            "unchanged_count": observation.get("unchanged_count"),
            "target_port": observation.get("target_port"),
            "snapshot_file": observation.get("snapshot_file"),
        })

    live_asn = concentration.get("live_asn_concentration", {})
    live_country = concentration.get("live_country_concentration", {})
    dac_signal = concentration.get("dac_signal_concentration", {})

    return {
        "project": "DAC Enode Intelligence Watcher",
        "summary_type": "custom_json_report_summary",
        "generated_at_utc": utc_now(),
        "range": selected_range,
        "range_label": range_title(selected_range),
        "source_files": {
            "latest": str(LATEST_FILE.relative_to(BASE_DIR)),
            "rotation": str(ROTATION_FILE.relative_to(BASE_DIR)),
            "anomaly": str(ANOMALY_FILE.relative_to(BASE_DIR)),
            "concentration": str(CONCENTRATION_FILE.relative_to(BASE_DIR)),
        },
        "important_note": (
            "This custom JSON summary is observation-based. It does not make official DAC ownership claims "
            "and should not be treated as a definitive decentralization measurement."
        ),
        "latest_observation": {
            "checked_at_utc": latest.get("checked_at_utc"),
            "generated_at_source": latest.get("generated_at_source"),
            "target_port": latest.get("target_port"),
            "current_total": latest.get("current_total"),
            "previous_total": latest.get("previous_total"),
            "added_count": latest.get("added_count"),
            "removed_count": latest.get("removed_count"),
            "unchanged_count": latest.get("unchanged_count"),
            "change_severity": latest.get("change_severity"),
            "severity_reason": latest.get("severity_reason"),
        },
        "observation_scope": {
            "selected_observation_count": timeline_summary["observations"],
            "first_observed_source_time": timeline_summary["first_source_time"],
            "last_observed_source_time": timeline_summary["last_source_time"],
            "phase_counts": timeline_summary["phase_counts"],
            "status_counts": timeline_summary["status_counts"],
            "target_ports_observed": timeline_summary["target_ports"],
        },
        "enode_movement_summary": {
            "min_enode_count": timeline_summary["min_enodes"],
            "max_enode_count": timeline_summary["max_enodes"],
            "avg_enode_count": timeline_summary["avg_enodes"],
            "total_added_events": timeline_summary["total_added"],
            "total_removed_events": timeline_summary["total_removed"],
        },
        "anomaly_summary": {
            "selected_anomaly_signal_count": len(selected_anomalies),
            "selected_severity_counts": dict(selected_severity_counts),
            "selected_anomaly_type_counts": dict(selected_anomaly_type_counts),
            "global_short_summary": anomaly.get("report_summary", {}).get("short_summary"),
            "global_highest_severity": anomaly.get("report_summary", {}).get("highest_severity"),
            "global_recommended_action": anomaly.get("report_summary", {}).get("recommended_action"),
        },
        "concentration_summary": {
            "overall_concentration_label": concentration.get("overall_concentration_label"),
            "headline": concentration_report.get("headline"),
            "key_observation": concentration_report.get("key_observation"),
            "country_observation": concentration_report.get("country_observation"),
            "interpretation": concentration_report.get("interpretation"),
            "recommended_action": concentration_report.get("recommended_action"),
            "disclaimer": concentration.get("disclaimer"),
            "top_dimensions": {
                "live_asn": {
                    "top_name": live_asn.get("top_name"),
                    "top_count": live_asn.get("top_count"),
                    "top_percentage": live_asn.get("top_percentage"),
                    "label": live_asn.get("concentration_label"),
                },
                "live_country": {
                    "top_name": live_country.get("top_name"),
                    "top_count": live_country.get("top_count"),
                    "top_percentage": live_country.get("top_percentage"),
                    "label": live_country.get("concentration_label"),
                },
                "dac_infrastructure_signal": {
                    "top_name": dac_signal.get("top_name"),
                    "top_count": dac_signal.get("top_count"),
                    "top_percentage": dac_signal.get("top_percentage"),
                    "label": dac_signal.get("concentration_label"),
                },
            },
        },
        "timeline": timeline_rows,
        "anomalies": anomaly_rows,
        "report_use_notes": [
            "Use the 7D report for short-range rotation and recent watcher movement.",
            "Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.",
            "Use the All Time report for full testnet observation history preserved by this watcher.",
            "Use JSON summaries for structured AI-assisted analysis, dashboards, and future export layers.",
        ],
    }

def build_custom_report(selected_range: str) -> str:
    latest = load_json(LATEST_FILE)
    rotation = load_json(ROTATION_FILE)
    anomaly = load_json(ANOMALY_FILE)
    concentration = load_json(CONCENTRATION_FILE)

    timeline = rotation.get("observation_timeline", [])
    selected_timeline = filter_timeline_by_range(timeline, selected_range)

    timeline_summary = summarize_timeline(selected_timeline)
    selected_anomalies = filter_anomalies_by_timeline(anomaly.get("anomalies", []), selected_timeline)

    selected_severity_counts = Counter(item.get("severity") or "Unknown" for item in selected_anomalies)
    selected_anomaly_type_counts = Counter(item.get("anomaly_type") or "Unknown" for item in selected_anomalies)

    concentration_report = concentration.get("report_ready_summary", {})
    live_asn = concentration.get("live_asn_concentration", {})
    live_country = concentration.get("live_country_concentration", {})
    dac_signal = concentration.get("dac_signal_concentration", {})

    lines = [
        f"# DAC Enode Intelligence Watcher — Custom {range_title(selected_range)} Report",
        "",
        f"Generated at UTC: `{utc_now()}`",
        "",
        f"Report range: **{range_title(selected_range)}**",
        "",
        "Project: **DAC Enode Intelligence Watcher**",
        "",
        "This custom report is generated from local watcher JSON outputs.",
        "",
        "Important note: this report is observation-based. It does not make official DAC ownership claims and should not be treated as a definitive decentralization measurement.",
    ]

    lines.append(section("1. Report Scope"))
    lines.append(table(
        ["Field", "Value"],
        [
            ["Range", range_title(selected_range)],
            ["Observation count", timeline_summary["observations"]],
            ["First observed source time", timeline_summary["first_source_time"]],
            ["Last observed source time", timeline_summary["last_source_time"]],
            ["Latest watcher checked_at_utc", latest.get("checked_at_utc", "N/A")],
            ["Latest source generated time", latest.get("generated_at_source", "N/A")],
        ],
    ))

    lines.append(section("2. Enode Movement Summary"))
    lines.append(table(
        ["Metric", "Value"],
        [
            ["Minimum enode count", timeline_summary["min_enodes"]],
            ["Maximum enode count", timeline_summary["max_enodes"]],
            ["Average enode count", timeline_summary["avg_enodes"]],
            ["Total added observations", timeline_summary["total_added"]],
            ["Total removed observations", timeline_summary["total_removed"]],
            ["Target ports observed", ", ".join(map(str, timeline_summary["target_ports"])) or "N/A"],
        ],
    ))

    lines.append(section("3. Observation Source Coverage"))
    phase_rows = [
        [phase, count]
        for phase, count in sorted(timeline_summary["phase_counts"].items(), key=lambda item: item[0])
    ]
    lines.append(table(["Phase", "Observations"], phase_rows or [["N/A", "N/A"]]))

    lines.append(section("4. Anomaly Summary"))
    lines.append(table(
        ["Field", "Value"],
        [
            ["Selected anomaly signals", len(selected_anomalies)],
            ["Global anomaly summary", anomaly.get("report_summary", {}).get("short_summary", "N/A")],
            ["Global highest severity", anomaly.get("report_summary", {}).get("highest_severity", "N/A")],
            ["Recommended action", anomaly.get("report_summary", {}).get("recommended_action", "N/A")],
        ],
    ))

    lines.append("")
    lines.append(table(
        ["Severity", "Signals in selected range"],
        [[severity, count] for severity, count in selected_severity_counts.most_common()] or [["N/A", "0"]],
    ))

    lines.append("")
    lines.append(table(
        ["Anomaly Type", "Signals in selected range"],
        [[anomaly_type, count] for anomaly_type, count in selected_anomaly_type_counts.most_common()] or [["N/A", "0"]],
    ))

    lines.append(section("5. Provider / ASN Concentration Context"))
    lines.append(table(
        ["Field", "Value"],
        [
            ["Overall concentration label", concentration.get("overall_concentration_label", "N/A")],
            ["Headline", concentration_report.get("headline", "N/A")],
            ["Key observation", concentration_report.get("key_observation", "N/A")],
            ["Country observation", concentration_report.get("country_observation", "N/A")],
            ["Interpretation", concentration_report.get("interpretation", "N/A")],
            ["Disclaimer", concentration.get("disclaimer", "N/A")],
        ],
    ))

    lines.append("")
    lines.append(table(
        ["Dimension", "Top Name", "Top Count", "Top %", "Label"],
        [
            [
                "Live ASN",
                live_asn.get("top_name", "N/A"),
                live_asn.get("top_count", "N/A"),
                live_asn.get("top_percentage", "N/A"),
                live_asn.get("concentration_label", "N/A"),
            ],
            [
                "Live Country",
                live_country.get("top_name", "N/A"),
                live_country.get("top_count", "N/A"),
                live_country.get("top_percentage", "N/A"),
                live_country.get("concentration_label", "N/A"),
            ],
            [
                "DAC Infrastructure Signal",
                dac_signal.get("top_name", "N/A"),
                dac_signal.get("top_count", "N/A"),
                dac_signal.get("top_percentage", "N/A"),
                dac_signal.get("concentration_label", "N/A"),
            ],
        ],
    ))

    lines.append(section("6. Observation Timeline"))
    timeline_rows = []
    for item in selected_timeline:
        timeline_rows.append([
            item.get("observation_index", "N/A"),
            item.get("phase", "N/A"),
            item.get("status", "N/A"),
            format_source_time(item.get("generated_at_source")),
            item.get("current_total", "N/A"),
            item.get("added_count", "N/A"),
            item.get("removed_count", "N/A"),
            item.get("unchanged_count", "N/A"),
            item.get("target_port", "N/A"),
        ])

    lines.append(table(
        ["#", "Phase", "Status", "Source Time", "Current", "Added", "Removed", "Unchanged", "Port"],
        timeline_rows or [["N/A"] * 9],
    ))

    lines.append(section("7. Report-Use Notes"))
    lines.append("- Use the 7D report for short-range rotation and recent watcher movement.")
    lines.append("- Use the 30D report for broader trend context once the 15-minute watcher has accumulated enough observations.")
    lines.append("- Use the All Time report for full testnet observation history preserved by this watcher.")
    lines.append("- For publication-quality interpretation, compare this Markdown output with dashboard charts, raw JSON outputs, and selected snapshots.")

    return "\n".join(lines).rstrip() + "\n"


def output_file_for_range(selected_range: str) -> Path:
    return REPORT_DIR / f"dac-enode-report-{selected_range}.md"


def json_output_file_for_range(selected_range: str) -> Path:
    return REPORT_DIR / f"dac-enode-report-{selected_range}.json"


def write_custom_json_summary(selected_range: str) -> Path:
    output_file = json_output_file_for_range(selected_range)
    output_file.write_text(
        json.dumps(build_custom_summary_data(selected_range), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate custom DAC enode Markdown reports.")
    parser.add_argument(
        "--range",
        choices=sorted(RANGE_OPTIONS),
        default="all",
        help="Report range: 7d, 30d, or all.",
    )
    parser.add_argument(
        "--format",
        choices=sorted(FORMAT_OPTIONS),
        default="markdown",
        help="Output format: markdown, json, or both.",
    )

    args = parser.parse_args()
    selected_range = args.range
    selected_format = args.format

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if selected_format in {"markdown", "both"}:
        report = build_custom_report(selected_range)
        output_file = output_file_for_range(selected_range)
        output_file.write_text(report, encoding="utf-8")
        print(f"[OK] Custom Markdown report generated: {output_file}")

    if selected_format in {"json", "both"}:
        json_output_file = write_custom_json_summary(selected_range)
        print(f"[OK] Custom JSON summary generated: {json_output_file}")

    print(f"[OK] Range: {selected_range}")
    print(f"[OK] Format: {selected_format}")


if __name__ == "__main__":
    main()
