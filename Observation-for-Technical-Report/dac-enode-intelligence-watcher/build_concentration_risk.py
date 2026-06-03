import json
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ROTATION_FILE = DATA_DIR / "rotation-intelligence-summary.json"
OUTPUT_FILE = DATA_DIR / "concentration-risk-summary.json"


DISCLAIMER = (
    "Provider concentration and decentralization risk summary is an observation-based heuristic. "
    "It is based on currently available watcher data, live ASN enrichment, static provider hints, "
    "and DAC Infrastructure Signal labels. It should not be treated as an official DAC classification "
    "or as a definitive decentralization measurement."
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def pct(part: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((part / total) * 100, 2)


def concentration_label(top_ratio: float, unknown_ratio: float = 0.0) -> str:
    if unknown_ratio >= 50:
        return "INCONCLUSIVE"
    if top_ratio >= 70:
        return "HIGH"
    if top_ratio >= 50:
        return "ELEVATED"
    if top_ratio >= 35:
        return "MODERATE"
    return "LOW"


def distribution_from_counts(counts: dict, total: int) -> list[dict]:
    rows = []

    for name, count in sorted(counts.items(), key=lambda item: (-item[1], str(item[0]))):
        rows.append({
            "name": str(name),
            "unique_ip_count": count,
            "percentage": pct(count, total),
        })

    return rows


def summarize_counts(
    dimension: str,
    counts: dict,
    total: int,
    unknown_keys: set[str] | None = None,
) -> dict:
    unknown_keys = unknown_keys or {"Unknown", "N/A", "None", ""}

    clean_counts = {
        str(key if key is not None else "Unknown"): int(value)
        for key, value in counts.items()
    }

    if not clean_counts or total <= 0:
        return {
            "dimension": dimension,
            "total_unique_ips": total,
            "top_name": "N/A",
            "top_count": 0,
            "top_percentage": 0.0,
            "unknown_count": 0,
            "unknown_percentage": 0.0,
            "concentration_label": "INCONCLUSIVE",
            "distribution": [],
        }

    top_name, top_count = sorted(
        clean_counts.items(),
        key=lambda item: (-item[1], item[0])
    )[0]

    unknown_count = sum(
        count
        for key, count in clean_counts.items()
        if key in unknown_keys
    )

    top_percentage = pct(top_count, total)
    unknown_percentage = pct(unknown_count, total)

    return {
        "dimension": dimension,
        "total_unique_ips": total,
        "top_name": top_name,
        "top_count": top_count,
        "top_percentage": top_percentage,
        "unknown_count": unknown_count,
        "unknown_percentage": unknown_percentage,
        "concentration_label": concentration_label(top_percentage, unknown_percentage),
        "distribution": distribution_from_counts(clean_counts, total),
    }


def classify_overall_risk(live_asn: dict, live_country: dict, dac_signal: dict) -> tuple[str, list[str]]:
    reasons = []

    if live_asn["concentration_label"] == "HIGH":
        reasons.append("Top live ASN controls at least 70% of observed unique IPs.")
    elif live_asn["concentration_label"] == "ELEVATED":
        reasons.append("Top live ASN controls at least 50% of observed unique IPs.")
    elif live_asn["concentration_label"] == "MODERATE":
        reasons.append("Top live ASN controls at least 35% of observed unique IPs.")

    if live_country["concentration_label"] in {"HIGH", "ELEVATED"}:
        reasons.append("Observed IPs show notable concentration in one live ASN country code.")

    if dac_signal["top_percentage"] >= 50:
        reasons.append("One DAC Infrastructure Signal category dominates the observed IP set.")

    if live_asn["unknown_percentage"] >= 50:
        reasons.append("Live ASN coverage is insufficient; overall assessment remains inconclusive.")
        return "INCONCLUSIVE", reasons

    label_rank = {
        "LOW": 0,
        "MODERATE": 1,
        "ELEVATED": 2,
        "HIGH": 3,
        "INCONCLUSIVE": -1,
    }

    strongest = max(
        [
            live_asn["concentration_label"],
            live_country["concentration_label"],
            dac_signal["concentration_label"],
        ],
        key=lambda label: label_rank.get(label, 0),
    )

    if not reasons:
        reasons.append("No single ASN, country, provider, or DAC signal category dominates under the current heuristic thresholds.")

    return strongest, reasons


def build_report_ready_summary(overall_label: str, live_asn: dict, live_country: dict, reasons: list[str]) -> dict:
    if overall_label == "INCONCLUSIVE":
        headline = "Concentration assessment is inconclusive under the current observation model."
    elif overall_label == "HIGH":
        headline = "Observed infrastructure shows high concentration under the current heuristic model."
    elif overall_label == "ELEVATED":
        headline = "Observed infrastructure shows elevated concentration under the current heuristic model."
    elif overall_label == "MODERATE":
        headline = "Observed infrastructure shows moderate concentration under the current heuristic model."
    else:
        headline = "Observed infrastructure does not show strong concentration under the current heuristic model."

    return {
        "headline": headline,
        "key_observation": (
            f"Top live ASN is {live_asn['top_name']} with "
            f"{live_asn['top_count']} unique IPs "
            f"({live_asn['top_percentage']}%)."
        ),
        "country_observation": (
            f"Top live ASN country code is {live_country['top_name']} with "
            f"{live_country['top_count']} unique IPs "
            f"({live_country['top_percentage']}%)."
        ),
        "interpretation": " ".join(reasons),
        "recommended_action": (
            "Use this as an observation aid only. Compare it with registry history, DAC Infrastructure Signal, "
            "manual peer identity evidence, live ASN lookup updates, and future watcher snapshots before drawing conclusions."
        ),
    }


def main() -> None:
    rotation = load_json(ROTATION_FILE)

    total_unique_ips = int(rotation.get("unique_ip_count") or 0)

    live_asn_counts = rotation.get("live_asn_counts", {})
    live_asn_name_counts = rotation.get("live_asn_name_counts", {})
    live_country_counts = rotation.get("live_asn_country_counts", {})
    static_provider_counts = rotation.get("provider_counts", {})
    static_asn_counts = rotation.get("asn_counts", {})
    dac_signal_counts = rotation.get("dac_infrastructure_signal_counts", {})

    live_asn_summary = summarize_counts(
        "live_asn",
        live_asn_counts,
        total_unique_ips,
        unknown_keys={"Unknown", "N/A", "None", ""},
    )

    live_asn_name_summary = summarize_counts(
        "live_asn_name",
        live_asn_name_counts,
        total_unique_ips,
        unknown_keys={"Unknown", "N/A", "None", ""},
    )

    live_country_summary = summarize_counts(
        "live_country_code",
        live_country_counts,
        total_unique_ips,
        unknown_keys={"Unknown", "N/A", "None", ""},
    )

    static_provider_summary = summarize_counts(
        "static_provider_hint",
        static_provider_counts,
        total_unique_ips,
        unknown_keys={"Unknown", "N/A", "None", ""},
    )

    static_asn_summary = summarize_counts(
        "static_asn_hint",
        static_asn_counts,
        total_unique_ips,
        unknown_keys={"Unknown", "N/A", "None", ""},
    )

    dac_signal_summary = summarize_counts(
        "dac_infrastructure_signal",
        dac_signal_counts,
        total_unique_ips,
        unknown_keys={"Unknown / No Signal", "Unknown", "N/A", "None", ""},
    )

    overall_label, reasons = classify_overall_risk(
        live_asn_summary,
        live_country_summary,
        dac_signal_summary,
    )

    summary = {
        "generated_at_utc": utc_now(),
        "source_file": "data/rotation-intelligence-summary.json",
        "method": "heuristic_concentration_assessment",
        "official_classification": False,
        "disclaimer": DISCLAIMER,
        "total_unique_ips": total_unique_ips,
        "overall_concentration_label": overall_label,
        "overall_reasons": reasons,
        "thresholds": {
            "LOW": "top concentration below 35%",
            "MODERATE": "top concentration at least 35%",
            "ELEVATED": "top concentration at least 50%",
            "HIGH": "top concentration at least 70%",
            "INCONCLUSIVE": "unknown coverage at least 50%",
        },
        "live_asn_concentration": live_asn_summary,
        "live_asn_name_concentration": live_asn_name_summary,
        "live_country_concentration": live_country_summary,
        "static_provider_concentration": static_provider_summary,
        "static_asn_concentration": static_asn_summary,
        "dac_signal_concentration": dac_signal_summary,
        "report_ready_summary": build_report_ready_summary(
            overall_label,
            live_asn_summary,
            live_country_summary,
            reasons,
        ),
    }

    OUTPUT_FILE.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"[OK] Concentration risk summary generated: {OUTPUT_FILE}")
    print(f"[OK] Total unique IPs: {total_unique_ips}")
    print(f"[OK] Overall concentration label: {overall_label}")
    print(f"[OK] Top live ASN: {live_asn_summary['top_name']} | {live_asn_summary['top_percentage']}%")
    print(f"[OK] Top live ASN country: {live_country_summary['top_name']} | {live_country_summary['top_percentage']}%")
    print(f"[OK] Top static provider hint: {static_provider_summary['top_name']} | {static_provider_summary['top_percentage']}%")


if __name__ == "__main__":
    main()
