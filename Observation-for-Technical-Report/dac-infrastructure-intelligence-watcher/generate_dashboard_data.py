#!/usr/bin/env python3

import json
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.2.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
DASHBOARD_DATA_DIR = BASE_DIR / "dashboard" / "data"

LATEST_FILE = DATA_DIR / "latest.json"
DASHBOARD_DATA_FILE = DASHBOARD_DATA_DIR / "health-dashboard-data.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_latest():
    return load_json(LATEST_FILE)


def load_snapshots():
    snapshots = []

    for path in sorted(SNAPSHOT_DIR.glob("*.json")):
        try:
            snapshots.append((path, load_json(path)))
        except Exception:
            continue

    return snapshots


def count_statuses(values):
    counts = {}

    for value in values:
        status = value or "UNKNOWN"
        counts[status] = counts.get(status, 0) + 1

    return dict(sorted(counts.items()))


def endpoint_status_counts(snapshots):
    output = {}

    for _, data in snapshots:
        endpoints = data.get("endpoints", {})

        for key, endpoint in endpoints.items():
            output.setdefault(key, [])
            output[key].append(endpoint.get("status", "UNKNOWN"))

    return {
        key: count_statuses(values)
        for key, values in output.items()
    }


def build_timeline(snapshots):
    rows = []

    for index, (path, data) in enumerate(snapshots, start=1):
        endpoints = data.get("endpoints", {})

        rows.append({
            "index": index,
            "snapshot_file": path.name,
            "checked_at_utc": data.get("checked_at_utc"),
            "overall_status": data.get("overall", {}).get("overall_status"),
            "official_public_rpc_status": endpoints.get("official_public_rpc", {}).get("status"),
            "explorer_web_status": endpoints.get("explorer_web", {}).get("status"),
            "primary_explorer_api_status": endpoints.get("primary_explorer_api", {}).get("status"),
            "rpc_latest_block_decimal": endpoints.get("official_public_rpc", {}).get("latest_block_decimal"),
            "rpc_latest_block_hex": endpoints.get("official_public_rpc", {}).get("latest_block_hex"),
        })

    return rows


def build_endpoint_cards(latest):
    cards = []

    for key, endpoint in latest.get("endpoints", {}).items():
        card = {
            "key": key,
            "name": endpoint.get("name", key),
            "url": endpoint.get("url"),
            "status": endpoint.get("status"),
            "ok": endpoint.get("ok"),
            "summary": endpoint.get("summary"),
        }

        if key == "official_public_rpc":
            card.update({
                "chain_id_hex": endpoint.get("chain_id_hex"),
                "latest_block_hex": endpoint.get("latest_block_hex"),
                "latest_block_decimal": endpoint.get("latest_block_decimal"),
                "latency_ms_avg": endpoint.get("latency_ms_avg"),
                "latency_ms_max": endpoint.get("latency_ms_max"),
                "latency_class": endpoint.get("latency_class"),
            })

        if key == "explorer_web":
            card.update({
                "http_status": endpoint.get("http_status"),
                "latency_ms": endpoint.get("latency_ms"),
                "latency_class": endpoint.get("latency_class"),
                "title": endpoint.get("title"),
                "has_explorer_signal": endpoint.get("has_explorer_signal"),
            })

        if key == "primary_explorer_api":
            card.update({
                "root_expected_validation": endpoint.get("root_expected_validation"),
                "stats_ok": endpoint.get("stats_ok"),
                "latency_ms_avg": endpoint.get("latency_ms_avg"),
                "latency_ms_max": endpoint.get("latency_ms_max"),
                "latency_class": endpoint.get("latency_class"),
            })

        cards.append(card)

    return cards


def build_dashboard_data():
    latest = load_latest()
    snapshots = load_snapshots()
    timeline = build_timeline(snapshots)

    overall_status_values = [
        item.get("overall_status")
        for item in timeline
    ]

    latest_overall = latest.get("overall", {})

    return {
        "project": PROJECT,
        "version": VERSION,
        "source_latest_checked_at_utc": latest.get("checked_at_utc"),
        "summary_type": "infrastructure_health_dashboard_data",
        "links": {
            "health_report": "../reports/generated/infrastructure-health-report.md",
            "latest_json": "../data/latest.json",
            "project_readme": "../README.md",
        },
        "latest": {
            "overall": latest_overall,
            "monitoring_scope": latest.get("monitoring_scope", {}),
            "endpoint_cards": build_endpoint_cards(latest),
            "interpretation_notes": latest.get("interpretation_notes", []),
        },
        "history": {
            "snapshot_count": len(snapshots),
            "first_snapshot": snapshots[0][0].name if snapshots else None,
            "latest_snapshot": snapshots[-1][0].name if snapshots else None,
            "overall_status_counts": count_statuses(overall_status_values),
            "endpoint_status_counts": endpoint_status_counts(snapshots),
            "timeline": timeline,
        },
    }


def main():
    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)

    dashboard_data = build_dashboard_data()
    DASHBOARD_DATA_FILE.write_text(
        json.dumps(dashboard_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print("[OK] Infrastructure health dashboard data generated.")
    print(f"[OK] Output: {DASHBOARD_DATA_FILE}")
    print(f"[OK] Snapshot count: {dashboard_data['history']['snapshot_count']}")
    print(f"[OK] Latest overall: {dashboard_data['latest']['overall'].get('overall_status')}")


if __name__ == "__main__":
    main()
