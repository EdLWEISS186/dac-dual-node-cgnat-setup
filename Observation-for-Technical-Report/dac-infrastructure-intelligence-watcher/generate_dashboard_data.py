#!/usr/bin/env python3

import json
from datetime import datetime, timezone
from pathlib import Path


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.8.0"

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

        rpc = endpoints.get("official_public_rpc", {})
        web = endpoints.get("explorer_web", {})
        api = endpoints.get("primary_explorer_api", {})

        rows.append({
            "index": index,
            "snapshot_file": path.name,
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
                "chain_id_decimal": endpoint.get("chain_id_decimal"),
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



def parse_iso_datetime(value):
    if not value:
        return None

    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def build_freshness(latest_checked_at_utc):
    checked_at = parse_iso_datetime(latest_checked_at_utc)
    now = datetime.now(timezone.utc)

    if checked_at is None:
        return {
            "status": "UNKNOWN",
            "age_minutes": None,
            "threshold_minutes": 30,
            "summary": "Freshness could not be determined because checked_at_utc is missing or invalid.",
        }

    age_seconds = max(0, int((now - checked_at).total_seconds()))
    age_minutes = round(age_seconds / 60, 2)

    if age_minutes <= 30:
        status = "FRESH"
        summary = "Latest watcher state is fresh."
    elif age_minutes <= 90:
        status = "STALE"
        summary = "Latest watcher state is older than the expected freshness window."
    else:
        status = "VERY_STALE"
        summary = "Latest watcher state is significantly old and should be refreshed."

    return {
        "status": status,
        "age_minutes": age_minutes,
        "threshold_minutes": 30,
        "summary": summary,
    }



def status_score(status):
    scores = {
        "HEALTHY": 100,
        "DEGRADED": 55,
        "PARTIAL_OUTAGE": 20,
        "UNHEALTHY": 0,
        "UNKNOWN": 0,
    }

    return scores.get(status or "UNKNOWN", 0)


def counts_to_chart_rows(counts, label_key="label"):
    return [
        {
            label_key: key,
            "count": value,
        }
        for key, value in sorted((counts or {}).items())
    ]


def build_response_class_counts(timeline):
    return {
        "official_public_rpc": count_statuses([
            item.get("official_public_rpc_response_class") or "UNKNOWN"
            for item in timeline
        ]),
        "explorer_web": count_statuses([
            item.get("explorer_web_response_class") or "UNKNOWN"
            for item in timeline
        ]),
        "primary_explorer_api": count_statuses([
            item.get("primary_explorer_api_response_class") or "UNKNOWN"
            for item in timeline
        ]),
    }


def build_chart_data(timeline, overall_status_counts, endpoint_counts):
    response_class_counts = build_response_class_counts(timeline)

    endpoint_rows = []
    for endpoint, counts in (endpoint_counts or {}).items():
        row = {"endpoint": endpoint}
        row.update(counts or {})
        endpoint_rows.append(row)

    response_rows = []
    for endpoint, counts in response_class_counts.items():
        row = {"endpoint": endpoint}
        row.update(counts or {})
        response_rows.append(row)

    health_score_rows = []
    for item in timeline:
        health_score_rows.append({
            "index": item.get("index"),
            "checked_at_utc": item.get("checked_at_utc"),
            "overall_status": item.get("overall_status") or "UNKNOWN",
            "score": status_score(item.get("overall_status")),
        })

    return {
        "overall_status_distribution": counts_to_chart_rows(overall_status_counts),
        "endpoint_status_distribution": endpoint_rows,
        "response_class_distribution": response_rows,
        "timeline_health_score": health_score_rows,
    }


def build_dashboard_data():
    latest = load_latest()
    snapshots = load_snapshots()
    timeline = build_timeline(snapshots)

    overall_status_values = [
        item.get("overall_status")
        for item in timeline
    ]

    latest_overall = latest.get("overall", {})

    freshness = build_freshness(latest.get("checked_at_utc"))

    overall_status_counts = count_statuses(overall_status_values)
    endpoint_counts = endpoint_status_counts(snapshots)
    charts = build_chart_data(timeline, overall_status_counts, endpoint_counts)

    return {
        "project": PROJECT,
        "version": VERSION,
        "source_latest_checked_at_utc": latest.get("checked_at_utc"),
        "freshness": freshness,
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
            "overall_status_counts": overall_status_counts,
            "endpoint_status_counts": endpoint_counts,
            "timeline": timeline,
        },
        "charts": charts,
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
