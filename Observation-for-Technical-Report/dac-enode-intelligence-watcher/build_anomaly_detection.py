import json
from collections import Counter
from pathlib import Path


PROJECT_NAME = "DAC Enode Intelligence Watcher"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

ROTATION_SUMMARY_FILE = DATA_DIR / "rotation-intelligence-summary.json"
OUTPUT_FILE = DATA_DIR / "anomaly-detection-summary.json"

EXPECTED_TARGET_PORT = 28657


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def severity_rank(severity: str) -> int:
    ranks = {
        "INFO": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4,
    }

    return ranks.get(severity, 0)


def add_anomaly(
    anomalies: list[dict],
    observation: dict,
    anomaly_type: str,
    severity: str,
    reason: str,
    technical_impact: str,
    recommended_action: str
) -> None:
    anomalies.append({
        "anomaly_type": anomaly_type,
        "severity": severity,
        "reason": reason,
        "technical_impact": technical_impact,
        "recommended_action": recommended_action,
        "observation": {
            "observation_index": observation.get("observation_index"),
            "phase": observation.get("phase"),
            "status": observation.get("status"),
            "generated_at_source": observation.get("generated_at_source"),
            "checked_at_utc": observation.get("checked_at_utc"),
            "target_port": observation.get("target_port"),
            "previous_total": observation.get("previous_total"),
            "current_total": observation.get("current_total"),
            "added_count": observation.get("added_count"),
            "removed_count": observation.get("removed_count"),
            "unchanged_count": observation.get("unchanged_count"),
            "change_severity": observation.get("change_severity"),
            "severity_reason": observation.get("severity_reason"),
            "snapshot_file": observation.get("snapshot_file")
        }
    })


def detect_anomalies(rotation_summary: dict) -> list[dict]:
    timeline = rotation_summary.get("observation_timeline", [])
    anomalies = []

    for observation in timeline:
        observation_index = observation.get("observation_index")
        phase = observation.get("phase")
        target_port = observation.get("target_port")
        previous_total = observation.get("previous_total")
        current_total = observation.get("current_total")
        added_count = observation.get("added_count") or 0
        removed_count = observation.get("removed_count") or 0
        unchanged_count = observation.get("unchanged_count") or 0

        if current_total is None:
            continue

        if current_total == 0:
            add_anomaly(
                anomalies=anomalies,
                observation=observation,
                anomaly_type="NO_ENODES_DETECTED",
                severity="CRITICAL",
                reason="No official enodes were detected in this observation.",
                technical_impact="The official enode source may be empty, unreachable, malformed, or temporarily unavailable.",
                recommended_action="Do not overwrite local peer records until the next observation confirms the state."
            )

        if target_port is not None and target_port != EXPECTED_TARGET_PORT:
            add_anomaly(
                anomalies=anomalies,
                observation=observation,
                anomaly_type="UNEXPECTED_TARGET_PORT",
                severity="HIGH",
                reason=f"Observed target port {target_port}, expected {EXPECTED_TARGET_PORT}.",
                technical_impact="A target port change may affect node runners who manually refresh official peer commands.",
                recommended_action="Verify the official source and review local node peer configuration before updating peer commands."
            )

        if previous_total and previous_total > 0:
            total_delta = current_total - previous_total
            changed_count = added_count + removed_count
            unchanged_ratio = unchanged_count / previous_total if previous_total else 0
            removed_ratio = removed_count / previous_total if previous_total else 0

            if current_total <= max(2, int(previous_total * 0.3)):
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="SHARP_ENODE_COUNT_DROP",
                    severity="CRITICAL",
                    reason=f"Official enode count dropped sharply from {previous_total} to {current_total}.",
                    technical_impact="A sharp drop may indicate source generation issues, infrastructure maintenance, or significant bootstrap peer removal.",
                    recommended_action="Preserve this snapshot and wait for the next observation before drawing a final conclusion."
                )

            elif total_delta <= -5:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="LARGE_ENODE_COUNT_DROP",
                    severity="HIGH",
                    reason=f"Official enode count decreased by {abs(total_delta)} from {previous_total} to {current_total}.",
                    technical_impact="A large decrease may indicate a significant peer-list refresh or infrastructure rotation.",
                    recommended_action="Compare removed enodes and check whether the next observation restores the count."
                )

            if removed_count >= 5 or removed_ratio >= 0.5:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="HIGH_REMOVAL_EVENT",
                    severity="HIGH",
                    reason=f"{removed_count} enodes were removed from a previous total of {previous_total}.",
                    technical_impact="High removal count may indicate bootstrap peer replacement or infrastructure rotation.",
                    recommended_action="Review removed enodes and preserve the snapshot for future report comparison."
                )

            if changed_count >= 8:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="AGGRESSIVE_ROTATION",
                    severity="HIGH",
                    reason=f"Large rotation intensity detected: {added_count} added and {removed_count} removed.",
                    technical_impact="High rotation intensity may suggest infrastructure maintenance, peer refresh, or node replacement.",
                    recommended_action="Track whether the next observations stabilize or continue rotating heavily."
                )

            elif changed_count >= 6:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="MODERATE_ROTATION_SPIKE",
                    severity="MEDIUM",
                    reason=f"Moderate rotation spike detected: {added_count} added and {removed_count} removed.",
                    technical_impact="This may represent a normal but meaningful bootstrap peer rotation event.",
                    recommended_action="Keep the event as report evidence and compare with surrounding observations."
                )

            if previous_total >= 8 and unchanged_ratio < 0.4:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="LOW_CONTINUITY_RATIO",
                    severity="MEDIUM",
                    reason=f"Only {unchanged_count} of {previous_total} previous enodes remained unchanged.",
                    technical_impact="Low continuity may indicate broader peer-list replacement rather than a small refresh.",
                    recommended_action="Review added and removed lists to identify whether this was a broad rotation event."
                )

        if phase == "automated_watcher":
            watcher_severity = observation.get("change_severity")

            if watcher_severity in {"HIGH", "CRITICAL"}:
                add_anomaly(
                    anomalies=anomalies,
                    observation=observation,
                    anomaly_type="WATCHER_HIGH_SEVERITY_SIGNAL",
                    severity=watcher_severity,
                    reason=observation.get("severity_reason") or f"Watcher classified this observation as {watcher_severity}.",
                    technical_impact="The automated watcher detected a high-severity condition.",
                    recommended_action="Review the generated snapshot and email alert for detailed context."
                )

    return anomalies


def build_report_summary(rotation_summary: dict, anomalies: list[dict]) -> dict:
    timeline = rotation_summary.get("observation_timeline", [])
    severity_counts = Counter(item["severity"] for item in anomalies)
    anomaly_type_counts = Counter(item["anomaly_type"] for item in anomalies)

    highest_severity = "INFO"

    for anomaly in anomalies:
        if severity_rank(anomaly["severity"]) > severity_rank(highest_severity):
            highest_severity = anomaly["severity"]

    if not anomalies:
        short_summary = (
            "No anomaly events were detected across the available observation dataset."
        )
        technical_interpretation = (
            "The observed enode rotation appears to remain within the configured normal range."
        )
        recommended_action = (
            "Continue scheduled monitoring and regenerate this summary as more snapshots are collected."
        )
    else:
        short_summary = (
            f"{len(anomalies)} anomaly signals were detected across {len(timeline)} observations. "
            f"The highest observed anomaly severity is {highest_severity}."
        )

        technical_interpretation = (
            "The anomaly layer highlights observations that may indicate unusually large peer rotation, "
            "sharp enode count changes, low continuity, or unexpected target port behavior."
        )

        recommended_action = (
            "Use these anomaly events as candidates for deeper manual review and future technical reporting."
        )

    return {
        "short_summary": short_summary,
        "highest_severity": highest_severity,
        "anomaly_count": len(anomalies),
        "severity_counts": dict(severity_counts),
        "anomaly_type_counts": dict(anomaly_type_counts),
        "technical_interpretation": technical_interpretation,
        "recommended_action": recommended_action
    }


def main() -> None:
    if not ROTATION_SUMMARY_FILE.exists():
        raise FileNotFoundError(
            f"Rotation intelligence summary not found: {ROTATION_SUMMARY_FILE}"
        )

    rotation_summary = load_json(ROTATION_SUMMARY_FILE)
    anomalies = detect_anomalies(rotation_summary)
    report_summary = build_report_summary(rotation_summary, anomalies)

    timeline = rotation_summary.get("observation_timeline", [])

    payload = {
        "project": PROJECT_NAME,
        "summary_type": "anomaly_detection_summary",
        "description": "Rule-based anomaly detection over DAC official enode observation history.",
        "input_file": "data/rotation-intelligence-summary.json",
        "output_file": "data/anomaly-detection-summary.json",
        "detector_type": "deterministic_rule_based",
        "machine_learning_used": False,
        "coverage_note": "Manual backfill is a partial archive. Missing dates represent missed observation windows, not confirmed absence of changes.",
        "observation_scope": {
            "total_observations": len(timeline),
            "first_observation": timeline[0] if timeline else None,
            "latest_observation": timeline[-1] if timeline else None
        },
        "rules": [
            {
                "rule": "NO_ENODES_DETECTED",
                "severity": "CRITICAL",
                "description": "Current enode count equals zero."
            },
            {
                "rule": "UNEXPECTED_TARGET_PORT",
                "severity": "HIGH",
                "description": f"Observed target port is not {EXPECTED_TARGET_PORT}."
            },
            {
                "rule": "SHARP_ENODE_COUNT_DROP",
                "severity": "CRITICAL",
                "description": "Current enode count drops to 30% or less of previous total."
            },
            {
                "rule": "LARGE_ENODE_COUNT_DROP",
                "severity": "HIGH",
                "description": "Current enode count decreases by at least 5."
            },
            {
                "rule": "HIGH_REMOVAL_EVENT",
                "severity": "HIGH",
                "description": "At least 5 enodes removed or at least 50% of previous enodes removed."
            },
            {
                "rule": "AGGRESSIVE_ROTATION",
                "severity": "HIGH",
                "description": "Added plus removed enode count is at least 8."
            },
            {
                "rule": "MODERATE_ROTATION_SPIKE",
                "severity": "MEDIUM",
                "description": "Added plus removed enode count is at least 6."
            },
            {
                "rule": "LOW_CONTINUITY_RATIO",
                "severity": "MEDIUM",
                "description": "Less than 40% of previous enodes remained unchanged."
            },
            {
                "rule": "WATCHER_HIGH_SEVERITY_SIGNAL",
                "severity": "HIGH_OR_CRITICAL",
                "description": "Automated watcher classified the observation as HIGH or CRITICAL."
            }
        ],
        "report_summary": report_summary,
        "anomalies": anomalies
    }

    save_json(OUTPUT_FILE, payload)

    print(f"[OK] Anomaly detection summary generated: {OUTPUT_FILE}")
    print(f"[OK] Total observations scanned: {len(timeline)}")
    print(f"[OK] Anomaly signals detected: {len(anomalies)}")
    print(f"[OK] Highest severity: {report_summary['highest_severity']}")
    print(f"[OK] Severity counts: {report_summary['severity_counts']}")
    print(f"[OK] Anomaly type counts: {report_summary['anomaly_type_counts']}")


if __name__ == "__main__":
    main()
