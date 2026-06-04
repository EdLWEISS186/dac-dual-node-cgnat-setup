#!/usr/bin/env python3

import json
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
REPORT_VERSION = "v1.1.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
REPORT_DIR = BASE_DIR / "reports" / "generated"

LATEST_FILE = DATA_DIR / "latest.json"
REPORT_FILE = REPORT_DIR / "infrastructure-health-report.md"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe(value, fallback="N/A"):
    if value is None or value == "":
        return fallback
    return str(value).replace("|", "\\|")


def load_snapshots():
    snapshots = []
    for path in sorted(SNAPSHOT_DIR.glob("*.json")):
        try:
            snapshots.append((path, load_json(path)))
        except Exception:
            continue
    return snapshots


def count_statuses(items, extractor):
    counts = {}
    for item in items:
        status = extractor(item) or "UNKNOWN"
        counts[status] = counts.get(status, 0) + 1
    return counts


def format_counts(counts):
    if not counts:
        return "N/A"
    return ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))


def endpoint_status_counts(snapshots):
    output = {}

    for _, data in snapshots:
        endpoints = data.get("endpoints", {})
        for key, endpoint in endpoints.items():
            output.setdefault(key, {})
            status = endpoint.get("status", "UNKNOWN")
            output[key][status] = output[key].get(status, 0) + 1

    return output


def endpoint_table(latest):
    lines = [
        "| Endpoint | Status | Summary |",
        "|---|---|---|",
    ]

    for key, endpoint in latest.get("endpoints", {}).items():
        lines.append(
            f"| {safe(endpoint.get('name', key))} | "
            f"{safe(endpoint.get('status'))} | "
            f"{safe(endpoint.get('summary'))} |"
        )

    return "\n".join(lines)


def rpc_checks_table(latest):
    rpc = latest.get("endpoints", {}).get("official_public_rpc", {})
    checks = rpc.get("checks", {})

    lines = [
        "| Method | OK | HTTP Status | Result | Error |",
        "|---|---:|---:|---|---|",
    ]

    for method, check in checks.items():
        lines.append(
            f"| {safe(method)} | "
            f"{safe(check.get('ok'))} | "
            f"{safe(check.get('http_status'))} | "
            f"{safe(check.get('result'))} | "
            f"{safe(check.get('error'))} |"
        )

    return "\n".join(lines)


def recent_timeline_table(snapshots, limit=20):
    lines = [
        "| # | Snapshot | Overall | RPC | Explorer Web | Explorer API |",
        "|---:|---|---|---|---|---|",
    ]

    selected = snapshots[-limit:]
    start_index = max(1, len(snapshots) - len(selected) + 1)

    for offset, (path, data) in enumerate(selected):
        endpoints = data.get("endpoints", {})
        lines.append(
            f"| {start_index + offset} | {safe(path.name)} | "
            f"{safe(data.get('overall', {}).get('overall_status'))} | "
            f"{safe(endpoints.get('official_public_rpc', {}).get('status'))} | "
            f"{safe(endpoints.get('explorer_web', {}).get('status'))} | "
            f"{safe(endpoints.get('primary_explorer_api', {}).get('status'))} |"
        )

    return "\n".join(lines)


def build_report():
    latest = load_json(LATEST_FILE)
    snapshots = load_snapshots()

    generated_from_latest = latest.get("checked_at_utc", "N/A")

    overall = latest.get("overall", {})
    monitoring = latest.get("monitoring_scope", {})
    endpoints = latest.get("endpoints", {})

    rpc = endpoints.get("official_public_rpc", {})
    explorer_web = endpoints.get("explorer_web", {})
    explorer_api = endpoints.get("primary_explorer_api", {})

    overall_counts = count_statuses(
        snapshots,
        lambda item: item[1].get("overall", {}).get("overall_status"),
    )

    per_endpoint_counts = endpoint_status_counts(snapshots)

    first_snapshot = snapshots[0][0].name if snapshots else "N/A"
    latest_snapshot = snapshots[-1][0].name if snapshots else "N/A"

    lines = [
        "# DAC Infrastructure Intelligence Watcher — Health Report",
        "",
        f"Generated from latest watcher state UTC: **{generated_from_latest}**",
        "",
        "This report is generated from DAC Infrastructure Intelligence Watcher JSON outputs.",
        "",
        "It summarizes public RPC health, explorer web availability, explorer API reachability, and endpoint-level health-state history.",
        "",
        "---",
        "",
        "## 1. Latest Overall Health",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Project | {safe(latest.get('project', PROJECT))} |",
        f"| Watcher version | {safe(latest.get('version'))} |",
        f"| Report layer version | {REPORT_VERSION} |",
        f"| Checked at UTC | {safe(latest.get('checked_at_utc'))} |",
        f"| Overall status | {safe(overall.get('overall_status'))} |",
        f"| Overall summary | {safe(overall.get('summary'))} |",
        f"| Healthy endpoints | {safe(overall.get('healthy_count'))} |",
        f"| Degraded endpoints | {safe(overall.get('degraded_count'))} |",
        f"| Unhealthy endpoints | {safe(overall.get('unhealthy_count'))} |",
        f"| Total endpoints | {safe(overall.get('total_endpoints'))} |",
        "",
        "## 2. Monitoring Scope",
        "",
        "| Component | URL |",
        "|---|---|",
        f"| Official Public RPC | {safe(monitoring.get('official_public_rpc'))} |",
        f"| Explorer Web | {safe(monitoring.get('explorer_web'))} |",
        f"| Primary Explorer API | {safe(monitoring.get('primary_explorer_api'))} |",
        f"| Timeout seconds | {safe(monitoring.get('timeout_seconds'))} |",
        "",
        "## 3. Endpoint Status Summary",
        "",
        endpoint_table(latest),
        "",
        "## 4. Public RPC Details",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| RPC status | {safe(rpc.get('status'))} |",
        f"| Chain ID | {safe(rpc.get('chain_id_decimal'))} |",
        f"| Chain ID hex | {safe(rpc.get('chain_id_hex'))} |",
        f"| Latest block hex | {safe(rpc.get('latest_block_hex'))} |",
        f"| Latest block decimal | {safe(rpc.get('latest_block_decimal'))} |",
        f"| Average response time | {safe(rpc.get('latency_ms_avg'))} ms |",
        f"| Maximum response time | {safe(rpc.get('latency_ms_max'))} ms |",
        f"| Response class | {safe(rpc.get('latency_class'))} |",
        "",
        rpc_checks_table(latest),
        "",
        "## 5. Explorer Details",
        "",
        "| Field | Explorer Web | Primary Explorer API |",
        "|---|---|---|",
        f"| Status | {safe(explorer_web.get('status'))} | {safe(explorer_api.get('status'))} |",
        f"| OK | {safe(explorer_web.get('ok'))} | {safe(explorer_api.get('ok'))} |",
        f"| HTTP / validation | {safe(explorer_web.get('http_status'))} | root_validation={safe(explorer_api.get('root_expected_validation'))}, stats_ok={safe(explorer_api.get('stats_ok'))} |",
        f"| Response time | {safe(explorer_web.get('latency_ms'))} ms | avg={safe(explorer_api.get('latency_ms_avg'))} ms, max={safe(explorer_api.get('latency_ms_max'))} ms |",
        f"| Response class | {safe(explorer_web.get('latency_class'))} | {safe(explorer_api.get('latency_class'))} |",
        f"| Title / API URL | {safe(explorer_web.get('title'))} | {safe(explorer_api.get('url'))} |",
        "",
        "## 6. Snapshot History Summary",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| Snapshot count | {len(snapshots)} |",
        f"| First snapshot | {safe(first_snapshot)} |",
        f"| Latest snapshot | {safe(latest_snapshot)} |",
        f"| Overall status counts | {safe(format_counts(overall_counts))} |",
        "",
        "| Endpoint | Status counts |",
        "|---|---|",
    ]

    for endpoint, counts in per_endpoint_counts.items():
        lines.append(f"| {safe(endpoint)} | {safe(format_counts(counts))} |")

    lines.extend([
        "",
        "## 7. Recent Snapshot Timeline",
        "",
        recent_timeline_table(snapshots),
        "",
        "## 8. Interpretation Notes",
        "",
    ])

    for note in latest.get("interpretation_notes", []):
        lines.append(f"- {note}")

    lines.extend([
        "",
        "## 9. Report-Use Notes",
        "",
        "This report is intended as supporting material for DAC Testnet infrastructure observation.",
        "",
        "It can be used to review service-level health windows, public RPC reliability, explorer availability, explorer API reachability, partial infrastructure states, and recovery behavior.",
        "",
        "It should not be treated as an official DAC service status page.",
        "",
        "---",
        "",
        "Prepared by **JERUZZALEM — DAC Infra Tester**.",
        "",
    ])

    return "\n".join(lines)


def main():
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    REPORT_FILE.write_text(report, encoding="utf-8")

    print("[OK] Infrastructure health Markdown report generated.")
    print(f"[OK] Output: {REPORT_FILE}")


if __name__ == "__main__":
    main()
