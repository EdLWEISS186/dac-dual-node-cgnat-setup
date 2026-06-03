import json
from pathlib import Path
from datetime import datetime, timezone


PROJECT_NAME = "DAC Enode Intelligence Watcher"
MAINTAINER = "JERUZZALEM — DAC Infra Tester"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports" / "generated"

LATEST_FILE = DATA_DIR / "latest.json"
MANUAL_SUMMARY_FILE = DATA_DIR / "manual-backfill" / "manual-backfill-summary.json"
ROTATION_SUMMARY_FILE = DATA_DIR / "rotation-intelligence-summary.json"
ANOMALY_SUMMARY_FILE = DATA_DIR / "anomaly-detection-summary.json"

OUTPUT_FILE = REPORT_DIR / "dac-enode-intelligence-report.md"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def safe(value, fallback="N/A"):
    if value is None:
        return fallback

    if value == "":
        return fallback

    return value


def short_enode(enode: str, head: int = 18, tail: int = 10) -> str:
    if not enode or len(enode) <= head + tail:
        return enode or "N/A"

    return f"{enode[:head]}...{enode[-tail:]}"


def table(headers, rows) -> str:
    output = []
    output.append("| " + " | ".join(headers) + " |")
    output.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in rows:
        output.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")

    return "\n".join(output)


def section(title: str) -> str:
    return f"\n## {title}\n"


def build_report() -> str:
    latest = load_json(LATEST_FILE)
    manual = load_json(MANUAL_SUMMARY_FILE)
    rotation = load_json(ROTATION_SUMMARY_FILE)
    anomaly = load_json(ANOMALY_SUMMARY_FILE)

    # Use watcher data timestamp instead of runtime timestamp.
    # This keeps the generated report deterministic when no watcher data changes.
    generated_at = (
        load_json(LATEST_FILE).get("checked_at_utc")
        or load_json(LATEST_FILE).get("generated_at_source")
        or datetime.now(timezone.utc).isoformat()
    )

    observation_scope = rotation.get("observation_scope", {})
    enode_stats = rotation.get("enode_count_statistics", {})
    report_ready = rotation.get("report_ready_summary", {})
    anomaly_report = anomaly.get("report_summary", {})

    latest_observation = observation_scope.get("latest_observation", {})
    first_observation = observation_scope.get("first_observation", {})

    persistent_enodes = rotation.get("most_persistent_enodes", [])[:10]
    persistent_ips = rotation.get("most_persistent_ips", [])[:10]
    provider_asn_summary = rotation.get("provider_asn_summary", [])
    provider_detection = rotation.get("provider_detection", {})
    dac_signal_meta = rotation.get("dac_infrastructure_signal", {})
    dac_signal_summary = rotation.get("dac_infrastructure_signal_summary", [])
    live_asn_meta = rotation.get("live_asn_lookup", {})
    live_asn_summary = rotation.get("live_asn_summary", [])
    timeline = rotation.get("observation_timeline", [])
    anomalies = anomaly.get("anomalies", [])

    lines = []

    lines.append("# DAC Enode Intelligence Watcher — Technical Observation Report")
    lines.append("")
    lines.append(f"Generated at UTC: `{generated_at}`")
    lines.append("")
    lines.append(f"Project: **{PROJECT_NAME}**")
    lines.append("")
    lines.append(f"Maintainer: **{MAINTAINER}**")
    lines.append("")
    lines.append("Related previous report:")
    lines.append("")
    lines.append("- `5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation`")
    lines.append("")
    lines.append("---")

    lines.append(section("1. Executive Summary"))
    lines.append(
        report_ready.get(
            "short_summary",
            "This report summarizes DAC official enode observations collected from manual backfill and automated watcher snapshots."
        )
    )
    lines.append("")
    lines.append(
        report_ready.get(
            "manual_to_automated_context",
            "The dataset combines pre-watcher manual observations with automated watcher snapshots."
        )
    )
    lines.append("")
    lines.append(
        report_ready.get(
            "technical_value",
            "The dataset supports analysis of bootstrap peer rotation, persistent official enodes, IP recurrence, and infrastructure maturation patterns."
        )
    )

    lines.append(section("2. Observation Scope"))
    lines.append(table(
        ["Metric", "Value"],
        [
            ["Manual backfill snapshots", observation_scope.get("manual_backfill_snapshots", manual.get("total_manual_snapshots", "N/A"))],
            ["Automated watcher snapshots", observation_scope.get("automated_watcher_snapshots", "N/A")],
            ["Total observations", observation_scope.get("total_snapshots", "N/A")],
            ["First observation", first_observation.get("generated_at_source", "N/A")],
            ["Latest observation", latest_observation.get("generated_at_source", latest.get("generated_at_source", "N/A"))],
            ["Target ports observed", ", ".join(str(port) for port in rotation.get("target_ports_observed", [])) or "N/A"],
            ["Unique enodes", rotation.get("unique_enode_count", "N/A")],
            ["Unique IPs", rotation.get("unique_ip_count", "N/A")],
        ]
    ))

    lines.append(section("3. Manual Backfill Context"))
    lines.append("Before the automated watcher was deployed, enode observations were collected manually.")
    lines.append("")
    lines.append("The manual backfill dataset preserves those earlier observations as structured JSON.")
    lines.append("")
    lines.append(table(
        ["Manual Dataset Metric", "Value"],
        [
            ["Observation completeness", manual.get("observation_completeness", "partial_manual_archive")],
            ["First manual snapshot", manual.get("first_generated_at_source", "N/A")],
            ["Last manual snapshot", manual.get("last_generated_at_source", "N/A")],
            ["Total manual snapshots", manual.get("total_manual_snapshots", "N/A")],
            ["Unique enodes in manual archive", manual.get("unique_enode_count", "N/A")],
            ["Minimum enode count", manual.get("min_enode_count", "N/A")],
            ["Maximum enode count", manual.get("max_enode_count", "N/A")],
            ["Target ports observed", ", ".join(str(port) for port in manual.get("target_ports_observed", [])) or "N/A"],
        ]
    ))
    lines.append("")
    lines.append("> Missing dates in the manual archive represent missed observation windows, not confirmed absence of infrastructure changes.")

    lines.append(section("4. Latest Automated Watcher State"))
    lines.append(table(
        ["Latest Field", "Value"],
        [
            ["Generated at source", latest.get("generated_at_source", "N/A")],
            ["Checked at UTC", latest.get("checked_at_utc", "N/A")],
            ["Target port", latest.get("target_port", "N/A")],
            ["Previous total", latest.get("previous_total", "N/A")],
            ["Current total", latest.get("current_total", "N/A")],
            ["Added count", latest.get("added_count", "N/A")],
            ["Removed count", latest.get("removed_count", "N/A")],
            ["Unchanged count", latest.get("unchanged_count", "N/A")],
            ["Change severity", latest.get("change_severity", "N/A")],
            ["Severity reason", latest.get("severity_reason", "N/A")],
        ]
    ))

    ai_summary = latest.get("ai_style_summary", {})
    if ai_summary:
        lines.append("")
        lines.append("Latest AI-style summary:")
        lines.append("")
        lines.append(f"> {ai_summary.get('summary', 'N/A')}")
        lines.append("")
        lines.append(f"Rotation interpretation: **{ai_summary.get('rotation_interpretation', 'N/A')}**")
        lines.append("")
        lines.append(f"Technical impact: {latest.get('technical_impact', 'N/A')}")
        lines.append("")
        lines.append(f"Recommended action: {latest.get('recommended_action', 'N/A')}")

    lines.append(section("5. Enode Count Statistics"))
    lines.append(table(
        ["Statistic", "Value"],
        [
            ["Minimum enode count", enode_stats.get("minimum", "N/A")],
            ["Maximum enode count", enode_stats.get("maximum", "N/A")],
            ["Average enode count", enode_stats.get("average", "N/A")],
        ]
    ))

    lines.append(section("6. Most Persistent Enodes"))
    persistent_enode_rows = []

    for item in persistent_enodes:
        persistent_enode_rows.append([
            short_enode(item.get("enode")),
            item.get("ip", "N/A"),
            item.get("port", "N/A"),
            item.get("appearance_count", "N/A"),
            item.get("appearance_ratio", "N/A"),
            ", ".join(item.get("phases_seen", [])),
        ])

    lines.append(table(
        ["Enode", "IP", "Port", "Appearances", "Ratio", "Phases Seen"],
        persistent_enode_rows or [["N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]]
    ))

    lines.append(section("7. Most Persistent IPs"))
    persistent_ip_rows = []

    for item in persistent_ips:
        persistent_ip_rows.append([
            item.get("ip", "N/A"),
            safe(item.get("dac_infrastructure_signal")),
            safe(item.get("signal_confidence")),
            safe(item.get("peer_identity_hint")),
            safe(item.get("provider_guess")),
            safe(item.get("asn_hint")),
            safe(item.get("provider_confidence")),
            safe(item.get("live_asn")),
            safe(item.get("live_asn_name")),
            safe(item.get("live_country_code")),
            item.get("appearance_count", "N/A"),
            item.get("appearance_ratio", "N/A"),
            ", ".join(item.get("phases_seen", [])),
            item.get("first_seen", {}).get("generated_at_source", "N/A"),
            item.get("last_seen", {}).get("generated_at_source", "N/A"),
        ])

    lines.append(table(
        ["IP", "DAC Signal", "Signal Confidence", "Peer Identity", "Static Provider", "Static ASN", "Provider Confidence", "Live ASN", "Live ASN Name", "Country", "Appearances", "Ratio", "Phases Seen", "First Seen", "Last Seen"],
        persistent_ip_rows or [["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]]
    ))

    lines.append(section("8. Live ASN Lookup Summary"))
    lines.append("Live ASN lookup is used as an enrichment layer only.")
    lines.append("")
    lines.append("ASN and provider names are based on external routing data and should be treated as operational context, not official DAC node ownership.")
    lines.append("")
    lines.append(table(
        ["Detection Field", "Value"],
        [
            ["Enabled", live_asn_meta.get("enabled", "N/A")],
            ["Method", live_asn_meta.get("lookup_method", "N/A")],
            ["Source", live_asn_meta.get("source", "N/A")],
            ["Cache file", live_asn_meta.get("cache_file", "N/A")],
            ["Failure behavior", live_asn_meta.get("failure_behavior", "N/A")],
            ["Disclaimer", live_asn_meta.get("disclaimer", "N/A")],
        ]
    ))
    lines.append("")

    live_asn_rows = []

    for item in live_asn_summary:
        live_asn_rows.append([
            item.get("live_asn", "N/A"),
            item.get("unique_ip_count", "N/A"),
            ", ".join(item.get("asn_names", [])),
            ", ".join(item.get("country_codes", [])),
            ", ".join(item.get("ips", [])),
        ])

    lines.append(table(
        ["Live ASN", "Unique IPs", "ASN Name", "Country", "IPs"],
        live_asn_rows or [["N/A", "N/A", "N/A", "N/A", "N/A"]]
    ))

    lines.append(section("9. DAC Infrastructure Signal Summary"))
    lines.append("DAC Infrastructure Signal is a community inference layer based on observed registry history, peer identity strings, persistence, subnet patterns, and provider hints.")
    lines.append("")
    lines.append("It is not an official DAC classification and should not be treated as confirmed node ownership.")
    lines.append("")
    lines.append(table(
        ["Detection Field", "Value"],
        [
            ["Method", dac_signal_meta.get("method", "N/A")],
            ["Official ownership claim", dac_signal_meta.get("official_ownership_claim", "N/A")],
            ["Source reference", dac_signal_meta.get("source_reference", "N/A")],
            ["Disclaimer", dac_signal_meta.get("disclaimer", "N/A")],
        ]
    ))
    lines.append("")

    dac_signal_rows = []

    for item in dac_signal_summary:
        dac_signal_rows.append([
            safe(item.get("dac_infrastructure_signal")),
            item.get("unique_ip_count", "N/A"),
            ", ".join(item.get("confidence_levels", [])),
            ", ".join(item.get("peer_identity_hints", [])),
            ", ".join(item.get("ips", [])),
        ])

    lines.append(table(
        ["DAC Infrastructure Signal", "Unique IPs", "Confidence", "Peer Identity Hints", "IPs"],
        dac_signal_rows or [["N/A", "N/A", "N/A", "N/A", "N/A"]]
    ))

    lines.append(section("10. Provider / ASN Hint Summary"))
    lines.append("Provider and ASN values in this section are heuristic hints based on static IP prefix matching.")
    lines.append("")
    lines.append("They should be treated as enrichment for infrastructure analysis, not final verified ASN truth.")
    lines.append("")
    lines.append(table(
        ["Detection Field", "Value"],
        [
            ["Method", provider_detection.get("method", "N/A")],
            ["Machine learning used", provider_detection.get("machine_learning_used", "N/A")],
            ["Live ASN lookup used", provider_detection.get("live_asn_lookup_used", "N/A")],
            ["Confidence note", provider_detection.get("confidence_note", "N/A")],
        ]
    ))
    lines.append("")

    provider_rows = []

    for item in provider_asn_summary:
        provider_rows.append([
            safe(item.get("provider_guess")),
            safe(item.get("asn_hint")),
            item.get("provider_type", "N/A"),
            item.get("country_hint", "N/A"),
            item.get("confidence", "N/A"),
            item.get("unique_ip_count", "N/A"),
            ", ".join(item.get("ips", [])),
        ])

    lines.append(table(
        ["Provider", "ASN", "Type", "Country Hint", "Confidence", "Unique IPs", "IPs"],
        provider_rows or [["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]]
    ))

    lines.append(section("11. Anomaly Detection Summary"))
    lines.append(table(
        ["Anomaly Metric", "Value"],
        [
            ["Anomaly count", anomaly_report.get("anomaly_count", "N/A")],
            ["Highest severity", anomaly_report.get("highest_severity", "N/A")],
            ["Severity counts", anomaly_report.get("severity_counts", "N/A")],
            ["Anomaly type counts", anomaly_report.get("anomaly_type_counts", "N/A")],
        ]
    ))
    lines.append("")
    lines.append(anomaly_report.get("technical_interpretation", "No anomaly interpretation available."))
    lines.append("")
    lines.append(f"Recommended action: {anomaly_report.get('recommended_action', 'N/A')}")

    lines.append(section("12. Detected Anomaly Events"))
    anomaly_rows = []

    for item in anomalies:
        obs = item.get("observation", {})
        anomaly_rows.append([
            item.get("anomaly_type", "N/A"),
            item.get("severity", "N/A"),
            obs.get("observation_index", "N/A"),
            obs.get("phase", "N/A"),
            obs.get("generated_at_source", "N/A"),
            obs.get("previous_total", "N/A"),
            obs.get("current_total", "N/A"),
            item.get("reason", "N/A"),
        ])

    lines.append(table(
        ["Type", "Severity", "Index", "Phase", "Generated At", "Previous", "Current", "Reason"],
        anomaly_rows or [["None", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "No anomaly events detected."]]
    ))

    lines.append(section("13. Observation Timeline"))
    timeline_rows = []

    for item in timeline:
        timeline_rows.append([
            item.get("observation_index", "N/A"),
            item.get("phase", "N/A"),
            item.get("generated_at_source", "N/A"),
            item.get("target_port", "N/A"),
            item.get("current_total", "N/A"),
            item.get("added_count", "N/A"),
            item.get("removed_count", "N/A"),
            item.get("change_severity", "N/A"),
        ])

    lines.append(table(
        ["Index", "Phase", "Generated At", "Port", "Total", "Added", "Removed", "Severity"],
        timeline_rows
    ))

    lines.append(section("14. Technical Interpretation"))
    lines.append("The current dataset shows a transition from manual observation into automated infrastructure monitoring.")
    lines.append("")
    lines.append("The official enode list shows visible peer rotation across the observation period, while the target port remains consistent at `28657`.")
    lines.append("")
    lines.append("Provider and ASN hints add an additional infrastructure-enrichment layer by grouping observed IPs into likely hosting providers or ASN categories where static prefix matching is available.")
    lines.append("")
    lines.append("Live ASN lookup adds a routing-data enrichment layer that can reduce Unknown provider/ASN coverage while remaining separate from official ownership claims.")
    lines.append("")
    lines.append("DAC Infrastructure Signal adds a separate community inference layer for interpreting observed node roles without claiming official ownership.")
    lines.append("")
    lines.append("The anomaly layer detected selected high-impact rotation events, but these should be interpreted as review signals rather than direct evidence of network failure.")
    lines.append("")
    lines.append("In a testnet environment, enode rotation may reflect infrastructure maintenance, bootstrap peer refreshes, scaling experiments, or network maturation.")

    lines.append(section("15. Conclusion"))
    lines.append("DAC Enode Intelligence Watcher now provides a structured evidence pipeline for official enode observation.")
    lines.append("")
    lines.append("The project currently supports:")
    lines.append("")
    lines.append("- manual pre-watcher archive preservation")
    lines.append("- automated enode monitoring")
    lines.append("- JSON snapshot generation")
    lines.append("- severity classification")
    lines.append("- AI-style summary generation")
    lines.append("- rotation intelligence aggregation")
    lines.append("- anomaly detection")
    lines.append("- report-ready Markdown generation")
    lines.append("- heuristic provider / ASN hint enrichment")
    lines.append("- DAC Infrastructure Signal enrichment")
    lines.append("- optional live ASN lookup enrichment")
    lines.append("")
    lines.append("This report can be used as a draft foundation for future DAC Testnet infrastructure technical reports.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"Generated by `{Path(__file__).name}`")
    lines.append("")
    lines.append(f"Maintainer: **{MAINTAINER}**")

    return "\n".join(lines) + "\n"


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    report = build_report()

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"[OK] Technical report generated: {OUTPUT_FILE}")
    print(f"[OK] Report size: {OUTPUT_FILE.stat().st_size} bytes")


if __name__ == "__main__":
    main()
