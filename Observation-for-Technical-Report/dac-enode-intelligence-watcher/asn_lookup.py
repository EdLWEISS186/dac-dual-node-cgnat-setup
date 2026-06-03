import json
import socket
from datetime import datetime, timezone
from ipaddress import ip_address
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ASN_CACHE_FILE = DATA_DIR / "asn-cache.json"

CYMRU_WHOIS_HOST = "whois.cymru.com"
CYMRU_WHOIS_PORT = 43

LOOKUP_METHOD = "team_cymru_whois_live_lookup"
CACHE_SCHEMA_VERSION = 1

DISCLAIMER = (
    "Live ASN lookup is used as an enrichment layer only. ASN and provider names are based on external "
    "routing data and should be treated as operational context, not official DAC node ownership."
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_default(ip: str, reason: str = "Live ASN lookup not available.") -> dict:
    return {
        "ip": ip,
        "live_lookup_used": False,
        "live_lookup_success": False,
        "lookup_method": LOOKUP_METHOD,
        "asn": None,
        "asn_name": None,
        "bgp_prefix": None,
        "country_code": None,
        "registry": None,
        "allocated": None,
        "source": "team_cymru",
        "cached": False,
        "checked_at_utc": utc_now(),
        "error": reason,
        "disclaimer": DISCLAIMER,
    }


def normalize_ip(ip: str) -> str | None:
    if not ip:
        return None

    try:
        return str(ip_address(ip))
    except ValueError:
        return None


def load_asn_cache(cache_file: Path = ASN_CACHE_FILE) -> dict:
    if not cache_file.exists():
        return {
            "schema_version": CACHE_SCHEMA_VERSION,
            "updated_at_utc": None,
            "lookup_method": LOOKUP_METHOD,
            "entries": {},
        }

    try:
        with cache_file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if "entries" not in data:
            data["entries"] = {}

        data.setdefault("schema_version", CACHE_SCHEMA_VERSION)
        data.setdefault("lookup_method", LOOKUP_METHOD)
        data.setdefault("updated_at_utc", None)

        return data
    except Exception:
        return {
            "schema_version": CACHE_SCHEMA_VERSION,
            "updated_at_utc": None,
            "lookup_method": LOOKUP_METHOD,
            "entries": {},
        }


def save_asn_cache(cache: dict, cache_file: Path = ASN_CACHE_FILE) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache["updated_at_utc"] = utc_now()

    ordered = {
        "schema_version": cache.get("schema_version", CACHE_SCHEMA_VERSION),
        "updated_at_utc": cache.get("updated_at_utc"),
        "lookup_method": cache.get("lookup_method", LOOKUP_METHOD),
        "entries": dict(sorted(cache.get("entries", {}).items())),
    }

    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(ordered, f, indent=2, sort_keys=False)


def parse_cymru_response(ip: str, response: str) -> dict:
    lines = [
        line.strip()
        for line in response.splitlines()
        if line.strip()
    ]

    data_lines = [
        line
        for line in lines
        if "|" in line and not line.lower().startswith("as")
    ]

    if not data_lines:
        return safe_default(ip, "No parseable Team Cymru WHOIS response.")

    parts = [part.strip() for part in data_lines[-1].split("|")]

    if len(parts) < 7:
        return safe_default(ip, f"Unexpected Team Cymru response format: {data_lines[-1]}")

    asn, returned_ip, bgp_prefix, country_code, registry, allocated, asn_name = parts[:7]

    return {
        "ip": returned_ip or ip,
        "live_lookup_used": True,
        "live_lookup_success": True,
        "lookup_method": LOOKUP_METHOD,
        "asn": f"AS{asn}" if asn and not asn.upper().startswith("AS") else asn,
        "asn_name": asn_name or None,
        "bgp_prefix": bgp_prefix or None,
        "country_code": country_code or None,
        "registry": registry or None,
        "allocated": allocated or None,
        "source": "team_cymru",
        "cached": False,
        "checked_at_utc": utc_now(),
        "error": None,
        "disclaimer": DISCLAIMER,
    }


def query_team_cymru_whois(ip: str, timeout: float = 8.0) -> dict:
    normalized_ip = normalize_ip(ip)

    if not normalized_ip:
        return safe_default(ip, "Invalid or missing IP address.")

    query = f" -v {normalized_ip}\n"

    try:
        with socket.create_connection((CYMRU_WHOIS_HOST, CYMRU_WHOIS_PORT), timeout=timeout) as sock:
            sock.settimeout(timeout)
            sock.sendall(query.encode("utf-8"))

            chunks = []
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                chunks.append(data)

        response = b"".join(chunks).decode("utf-8", errors="replace")
        return parse_cymru_response(normalized_ip, response)

    except Exception as exc:
        return safe_default(normalized_ip, f"Team Cymru WHOIS lookup failed: {exc}")


def lookup_asn(
    ip: str,
    cache: dict | None = None,
    use_live_lookup: bool = True,
    refresh: bool = False,
) -> tuple[dict, dict]:
    normalized_ip = normalize_ip(ip)

    if not normalized_ip:
        result = safe_default(ip, "Invalid or missing IP address.")
        return result, cache or load_asn_cache()

    if cache is None:
        cache = load_asn_cache()

    entries = cache.setdefault("entries", {})

    if not refresh and normalized_ip in entries:
        cached_result = dict(entries[normalized_ip])
        cached_result["cached"] = True
        return cached_result, cache

    if not use_live_lookup:
        result = safe_default(normalized_ip, "Live ASN lookup disabled.")
        entries[normalized_ip] = result
        return result, cache

    result = query_team_cymru_whois(normalized_ip)
    entries[normalized_ip] = result
    return result, cache


def lookup_many(
    ips: list[str],
    use_live_lookup: bool = True,
    refresh: bool = False,
    save_cache: bool = True,
) -> dict:
    cache = load_asn_cache()
    results = {}

    for ip in sorted(set(filter(None, ips))):
        result, cache = lookup_asn(
            ip=ip,
            cache=cache,
            use_live_lookup=use_live_lookup,
            refresh=refresh,
        )
        results[ip] = result

    if save_cache:
        save_asn_cache(cache)

    return results


if __name__ == "__main__":
    test_ips = [
        "213.136.82.243",
        "206.189.127.204",
        "95.216.70.180",
        "157.173.127.30",
    ]

    results = lookup_many(test_ips, use_live_lookup=True, refresh=False, save_cache=True)

    for ip, result in results.items():
        print(
            ip,
            "=>",
            result.get("asn"),
            "|",
            result.get("asn_name"),
            "|",
            result.get("bgp_prefix"),
            "|",
            "success=",
            result.get("live_lookup_success"),
            "|",
            "cached=",
            result.get("cached"),
        )
