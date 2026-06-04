#!/usr/bin/env python3

import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


PROJECT = "DAC Infrastructure Intelligence Watcher"
VERSION = "v1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"

LATEST_FILE = DATA_DIR / "latest.json"

RPC_URL = "https://rpctest.dachain.tech/"
EXPLORER_WEB_URL = "https://exptest.dachain.tech/"
EXPLORER_API_URL = "https://exptest.dachain.tech/api"

TIMEOUT = 15


def now_utc():
    return datetime.now(timezone.utc)


def snapshot_name(dt):
    return dt.isoformat().replace(":", "-").replace(".", "-").replace("+", "+") + "-health.json"


def elapsed_ms(start):
    return int(round((time.perf_counter() - start) * 1000))


def safe_json(response):
    try:
        return response.json()
    except Exception:
        return None


def rpc_call(method):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": [],
    }

    start = time.perf_counter()

    try:
        response = requests.post(
            RPC_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT,
        )

        body = safe_json(response)
        ok = (
            response.status_code == 200
            and isinstance(body, dict)
            and body.get("result") is not None
            and body.get("error") is None
        )

        return {
            "method": method,
            "ok": ok,
            "http_status": response.status_code,
            "latency_ms": elapsed_ms(start),
            "result": body.get("result") if isinstance(body, dict) else None,
            "error": body.get("error") if isinstance(body, dict) else None,
        }

    except Exception as exc:
        return {
            "method": method,
            "ok": False,
            "http_status": None,
            "latency_ms": elapsed_ms(start),
            "result": None,
            "error": str(exc),
        }



def classify_latency(latency_ms):
    if latency_ms is None:
        return "N/A"
    if latency_ms <= 500:
        return "FAST"
    if latency_ms <= 1500:
        return "MODERATE"
    return "SLOW"


def latency_summary_from_checks(checks):
    latencies = [
        check.get("latency_ms")
        for check in checks.values()
        if isinstance(check.get("latency_ms"), int)
    ]

    if not latencies:
        return {
            "latency_ms_avg": None,
            "latency_ms_max": None,
            "latency_class": "N/A",
        }

    avg_latency = int(round(sum(latencies) / len(latencies)))
    max_latency = max(latencies)

    return {
        "latency_ms_avg": avg_latency,
        "latency_ms_max": max_latency,
        "latency_class": classify_latency(max_latency),
    }


def hex_to_int(value):
    if not value:
        return None

    try:
        return int(value, 16)
    except Exception:
        return None


def check_rpc():
    checks = {
        "eth_chainId": rpc_call("eth_chainId"),
        "eth_blockNumber": rpc_call("eth_blockNumber"),
        "web3_clientVersion": rpc_call("web3_clientVersion"),
    }

    required_ok = checks["eth_chainId"]["ok"] and checks["eth_blockNumber"]["ok"]
    optional_ok = checks["web3_clientVersion"]["ok"]

    latest_block_hex = checks["eth_blockNumber"].get("result")
    latest_block_decimal = None

    if isinstance(latest_block_hex, str) and latest_block_hex.startswith("0x"):
        try:
            latest_block_decimal = int(latest_block_hex, 16)
        except ValueError:
            latest_block_decimal = None

    any_ok = any(check.get("ok") for check in checks.values())

    if required_ok and optional_ok:
        status = "HEALTHY"
        summary = "Public RPC responded to required and optional JSON-RPC checks."
    elif any_ok:
        status = "DEGRADED"
        summary = "Public RPC is reachable, but one or more JSON-RPC checks failed."
    else:
        status = "UNHEALTHY"
        summary = "Public RPC failed all JSON-RPC checks."

    latency_summary = latency_summary_from_checks(checks)

    return {
        "name": "Official Public RPC",
        "url": RPC_URL,
        "status": status,
        "ok": required_ok,
        "summary": summary,
        "chain_id_hex": checks["eth_chainId"].get("result"),
        "chain_id_decimal": hex_to_int(checks["eth_chainId"].get("result")),
        "latest_block_hex": latest_block_hex,
        "latest_block_decimal": latest_block_decimal,
        "latency_ms_avg": latency_summary["latency_ms_avg"],
        "latency_ms_max": latency_summary["latency_ms_max"],
        "latency_class": latency_summary["latency_class"],
        "checks": checks,
    }


def check_explorer_web():
    start = time.perf_counter()

    try:
        response = requests.get(EXPLORER_WEB_URL, timeout=TIMEOUT, allow_redirects=True)
        body = response.text or ""
        lower_body = body.lower()

        title = None
        if "<title" in lower_body and "</title>" in lower_body:
            try:
                title_start = lower_body.index("<title")
                title_open_end = lower_body.index(">", title_start)
                title_end = lower_body.index("</title>", title_open_end)
                title = body[title_open_end + 1:title_end].strip()
            except Exception:
                title = None

        has_explorer_signal = (
            "dac inception testnet" in lower_body
            or "block explorer" in lower_body
            or "blockscout" in lower_body
        )

        ok = response.status_code == 200 and has_explorer_signal

        if ok:
            status = "HEALTHY"
            summary = "Explorer web returned HTTP 200 and recognizable explorer content."
        elif response.status_code == 200:
            status = "DEGRADED"
            summary = "Explorer web returned HTTP 200, but expected explorer content was not detected."
        else:
            status = "UNHEALTHY"
            summary = "Explorer web did not return HTTP 200."

        return {
            "name": "Explorer Web",
            "url": EXPLORER_WEB_URL,
            "status": status,
            "ok": ok,
            "summary": summary,
            "http_status": response.status_code,
            "latency_ms": elapsed_ms(start),
            "latency_class": classify_latency(elapsed_ms(start)),
            "content_type": response.headers.get("content-type"),
            "server": response.headers.get("server"),
            "x_powered_by": response.headers.get("x-powered-by"),
            "title": title,
            "has_explorer_signal": has_explorer_signal,
        }

    except Exception as exc:
        return {
            "name": "Explorer Web",
            "url": EXPLORER_WEB_URL,
            "status": "UNHEALTHY",
            "ok": False,
            "summary": "Explorer web request failed.",
            "http_status": None,
            "latency_ms": elapsed_ms(start),
            "latency_class": classify_latency(elapsed_ms(start)),
            "error": str(exc),
        }


def get_api(url):
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
        return {
            "url": url,
            "request_ok": True,
            "http_status": response.status_code,
            "latency_ms": elapsed_ms(start),
            "latency_class": classify_latency(elapsed_ms(start)),
            "json": safe_json(response),
            "error": None,
        }

    except Exception as exc:
        return {
            "url": url,
            "request_ok": False,
            "http_status": None,
            "latency_ms": elapsed_ms(start),
            "latency_class": classify_latency(elapsed_ms(start)),
            "json": None,
            "error": str(exc),
        }


def check_explorer_api():
    root = get_api(EXPLORER_API_URL)
    stats = get_api(EXPLORER_API_URL + "?module=stats&action=ethsupply")

    root_json = root.get("json") or {}
    stats_json = stats.get("json") or {}

    root_expected = (
        root.get("http_status") == 400
        and isinstance(root_json, dict)
        and root_json.get("status") == "0"
        and "module" in str(root_json.get("message", "")).lower()
        and "action" in str(root_json.get("message", "")).lower()
    )

    stats_ok = (
        stats.get("http_status") == 200
        and isinstance(stats_json, dict)
        and stats_json.get("status") == "1"
    )

    ok = root_expected or stats_ok

    if stats_ok:
        status = "HEALTHY"
        summary = "Explorer API responded successfully to supported stats endpoint."
    elif ok:
        status = "DEGRADED"
        summary = "Explorer API is reachable, but supported stats endpoint did not return status=1."
    else:
        status = "UNHEALTHY"
        summary = "Explorer API did not return expected validation or supported endpoint output."

    api_latency_summary = latency_summary_from_checks({
        "root": root,
        "stats_ethsupply": stats,
    })

    return {
        "name": "Primary Explorer API",
        "url": EXPLORER_API_URL,
        "status": status,
        "ok": ok,
        "summary": summary,
        "root_expected_validation": root_expected,
        "stats_ok": stats_ok,
        "latency_ms_avg": api_latency_summary["latency_ms_avg"],
        "latency_ms_max": api_latency_summary["latency_ms_max"],
        "latency_class": api_latency_summary["latency_class"],
        "checks": {
            "root": root,
            "stats_ethsupply": stats,
        },
    }


def derive_overall(endpoints):
    statuses = [item.get("status") for item in endpoints.values()]

    healthy = statuses.count("HEALTHY")
    degraded = statuses.count("DEGRADED")
    unhealthy = statuses.count("UNHEALTHY")

    if unhealthy == 0 and degraded == 0:
        overall_status = "HEALTHY"
        summary = "All monitored DAC infrastructure endpoints are healthy."
    elif unhealthy == 0:
        overall_status = "DEGRADED"
        summary = "All monitored endpoints are reachable, but at least one endpoint is degraded."
    elif healthy > 0 or degraded > 0:
        overall_status = "PARTIAL_OUTAGE"
        summary = "At least one endpoint is unhealthy while other monitored endpoints remain reachable."
    else:
        overall_status = "UNHEALTHY"
        summary = "All monitored endpoints are unhealthy or unreachable."

    return {
        "overall_status": overall_status,
        "summary": summary,
        "healthy_count": healthy,
        "degraded_count": degraded,
        "unhealthy_count": unhealthy,
        "total_endpoints": len(statuses),
    }



def build_health_signature(summary):
    endpoints = summary.get("endpoints", {})

    rpc = endpoints.get("official_public_rpc", {})
    explorer_web = endpoints.get("explorer_web", {})
    explorer_api = endpoints.get("primary_explorer_api", {})

    return {
        "overall_status": summary.get("overall", {}).get("overall_status"),
        "official_public_rpc_status": rpc.get("status"),
        "explorer_web_status": explorer_web.get("status"),
        "primary_explorer_api_status": explorer_api.get("status"),
    }

def build_summary():
    checked_at = now_utc()

    endpoints = {
        "official_public_rpc": check_rpc(),
        "explorer_web": check_explorer_web(),
        "primary_explorer_api": check_explorer_api(),
    }

    summary = {
        "project": PROJECT,
        "version": VERSION,
        "summary_type": "infrastructure_health",
        "checked_at_utc": checked_at.isoformat(),
        "monitoring_scope": {
            "official_public_rpc": RPC_URL,
            "explorer_web": EXPLORER_WEB_URL,
            "primary_explorer_api": EXPLORER_API_URL,
            "timeout_seconds": TIMEOUT,
        },
        "overall": derive_overall(endpoints),
        "endpoints": endpoints,
        "state_signature": None,
        "interpretation_notes": [
            "RPC health is based on JSON-RPC POST checks, not HTTP GET root behavior.",
            "Explorer API root returning a validation error for missing module/action is treated as reachability evidence.",
            "Explorer API proxy module is not assumed to be supported.",
            "This health summary is an independent observation aid and not an official DAC service status page.",
        ],
    }

    summary["state_signature"] = build_health_signature(summary)
    return summary


def load_previous_latest():
    if not LATEST_FILE.exists():
        return None

    try:
        return json.loads(LATEST_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_outputs(summary):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    previous = load_previous_latest()
    previous_signature = previous.get("state_signature") if isinstance(previous, dict) else None
    current_signature = summary.get("state_signature")

    checked_at = datetime.fromisoformat(summary["checked_at_utc"])
    snapshot_file = SNAPSHOT_DIR / snapshot_name(checked_at)

    text = json.dumps(summary, indent=2, ensure_ascii=False) + "\n"

    # latest.json should represent the latest health check, including latency and block state.
    # Snapshots remain state-change based to avoid noisy historical files.
    LATEST_FILE.write_text(text, encoding="utf-8")

    if previous_signature == current_signature:
        return None

    snapshot_file.write_text(text, encoding="utf-8")
    return snapshot_file

def main():
    summary = build_summary()
    snapshot_file = write_outputs(summary)

    print("[OK] DAC infrastructure health check completed.")
    print(f"[OK] Overall status: {summary['overall']['overall_status']}")

    print(f"[OK] Latest output refreshed: {LATEST_FILE}")

    if snapshot_file:
        print(f"[OK] Health state changed.")
        print(f"[OK] Snapshot output: {snapshot_file}")
    else:
        print("[OK] No health state change detected. Snapshot output was not created.")

    for key, endpoint in summary["endpoints"].items():
        print(f"[OK] {key}: {endpoint.get('status')} — {endpoint.get('summary')}")


if __name__ == "__main__":
    main()
