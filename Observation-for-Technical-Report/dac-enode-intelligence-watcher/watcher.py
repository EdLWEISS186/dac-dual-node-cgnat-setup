import os
import re
import json
import smtplib
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path

import requests
from bs4 import BeautifulSoup


PROJECT_NAME = "DAC Enode Intelligence Watcher"
TARGET_URL = "https://enodes.dachain.tech/testnet/"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
SNAPSHOT_DIR = DATA_DIR / "snapshots"
LATEST_FILE = DATA_DIR / "latest.json"

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
EMAIL_FROM = os.environ.get("EMAIL_FROM", SMTP_USER)
EMAIL_TO = os.environ.get("EMAIL_TO", "suryaawalaka@gmail.com")

ENODE_REGEX = re.compile(
    r'enode://[0-9a-fA-F]+@[^\s"\')]+',
    re.IGNORECASE
)

GENERATED_REGEX = re.compile(
    r"Generated:\s*(.*?)\s*\|\s*Target Port:\s*(\d+)",
    re.IGNORECASE
)


def fetch_page_text() -> str:
    headers = {
        "User-Agent": "DAC-Enode-Intelligence-Watcher/1.0 by JERUZZALEM"
    }

    response = requests.get(TARGET_URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    visible_text = soup.get_text("\n")
    raw_html = response.text

    return visible_text + "\n" + raw_html


def extract_generated_info(text: str) -> dict:
    match = GENERATED_REGEX.search(text)

    if not match:
        return {
            "generated_at_source": None,
            "target_port": None
        }

    return {
        "generated_at_source": match.group(1).strip(),
        "target_port": int(match.group(2))
    }


def extract_enodes(text: str) -> list[str]:
    enodes = ENODE_REGEX.findall(text)
    return sorted(set(enodes))


def parse_enode_details(enode: str) -> dict:
    try:
        without_prefix = enode.replace("enode://", "")
        node_id, endpoint = without_prefix.split("@", 1)
        ip, port = endpoint.rsplit(":", 1)

        return {
            "enode": enode,
            "node_id": node_id,
            "ip": ip,
            "port": int(port)
        }
    except Exception:
        return {
            "enode": enode,
            "node_id": None,
            "ip": None,
            "port": None
        }


def admin_addpeer_line(enode: str) -> str:
    return f'admin.addPeer("{enode}");'


def classify_change(
    added: list[str],
    removed: list[str],
    unchanged: list[str],
    previous_enodes: list[str],
    current_enodes: list[str],
    previous_target_port: int | None,
    current_target_port: int | None,
    target_port_changed: bool,
    is_initial: bool
) -> tuple[str, str]:
    added_count = len(added)
    removed_count = len(removed)
    changed_count = added_count + removed_count
    previous_total = len(previous_enodes)
    current_total = len(current_enodes)

    if is_initial:
        return (
            "INFO",
            "Initial baseline snapshot captured because no previous watcher state existed."
        )

    if current_total == 0:
        return (
            "CRITICAL",
            "No enodes were detected from the official source."
        )

    if target_port_changed:
        return (
            "HIGH",
            f"Target port changed from {previous_target_port} to {current_target_port}."
        )

    if previous_total > 0 and current_total <= max(2, int(previous_total * 0.3)):
        return (
            "CRITICAL",
            f"Official enode count dropped sharply from {previous_total} to {current_total}."
        )

    if previous_total > 0 and removed_count >= max(5, int(previous_total * 0.5)):
        return (
            "HIGH",
            f"{removed_count} enodes were removed from a previous total of {previous_total}."
        )

    if changed_count == 0:
        return (
            "NONE",
            "No enode or target-port change detected."
        )

    if changed_count <= 2:
        return (
            "LOW",
            f"Small enode rotation detected: {added_count} added and {removed_count} removed."
        )

    if changed_count <= 6:
        return (
            "MEDIUM",
            f"Moderate enode rotation detected: {added_count} added and {removed_count} removed."
        )

    return (
        "HIGH",
        f"Large enode rotation detected: {added_count} added and {removed_count} removed."
    )


def build_ai_style_summary(
    added: list[str],
    removed: list[str],
    unchanged: list[str],
    previous_enodes: list[str],
    current_enodes: list[str],
    previous_target_port: int | None,
    current_target_port: int | None,
    target_port_changed: bool,
    change_severity: str,
    is_initial: bool
) -> dict:
    added_count = len(added)
    removed_count = len(removed)
    unchanged_count = len(unchanged)
    previous_total = len(previous_enodes)
    current_total = len(current_enodes)

    if is_initial:
        summary = (
            f"Initial DAC official enode baseline captured with {current_total} enodes. "
            f"The observed target port is {current_target_port}."
        )
        technical_impact = (
            "This snapshot becomes the first automated comparison baseline for future enode observations."
        )
        recommended_action = (
            "Keep this baseline as the starting point for automated watcher history."
        )
        rotation_interpretation = "Initial baseline capture; no previous automated snapshot exists for comparison."

    elif target_port_changed:
        summary = (
            f"DAC official enode target port changed from {previous_target_port} to {current_target_port}. "
            f"The current list contains {current_total} enodes."
        )
        technical_impact = (
            "A target port change may affect node runners who manually rely on the official enode page for peer configuration."
        )
        recommended_action = (
            "Review the updated official enode list before refreshing local peer commands."
        )
        rotation_interpretation = "Target port migration or configuration update detected."

    elif added_count or removed_count:
        summary = (
            f"DAC official enode list changed: {added_count} enodes added, "
            f"{removed_count} removed, and {unchanged_count} remained unchanged. "
            f"Current total: {current_total} enodes."
        )

        if change_severity == "LOW":
            rotation_interpretation = "Small bootstrap peer rotation detected."
            technical_impact = "This appears to be a minor peer-list refresh."
            recommended_action = "No urgent action is required, but the snapshot is preserved for history."

        elif change_severity == "MEDIUM":
            rotation_interpretation = "Moderate bootstrap peer rotation detected."
            technical_impact = "Node runners may review the updated list if they manually refresh official peers."
            recommended_action = "Compare added and removed enodes before updating manual peer records."

        elif change_severity == "HIGH":
            rotation_interpretation = "Large bootstrap peer rotation detected."
            technical_impact = "This may indicate infrastructure rotation, maintenance, scaling, or peer replacement."
            recommended_action = "Review the full snapshot and preserve it for technical reporting."

        else:
            rotation_interpretation = "Enode list changed."
            technical_impact = "The official peer list changed and should be tracked as infrastructure evidence."
            recommended_action = "Review the generated JSON snapshot."

    else:
        summary = (
            f"No meaningful DAC official enode change detected. "
            f"The current list remains at {current_total} enodes with target port {current_target_port}."
        )
        technical_impact = "No new technical action is required."
        recommended_action = "Continue scheduled monitoring."
        rotation_interpretation = "Stable peer-list state."

    return {
        "summary": summary,
        "rotation_interpretation": rotation_interpretation,
        "technical_impact": technical_impact,
        "recommended_action": recommended_action,
        "previous_total": previous_total,
        "current_total": current_total,
        "added_count": added_count,
        "removed_count": removed_count,
        "unchanged_count": unchanged_count,
        "target_port_changed": target_port_changed
    }


def load_latest() -> dict | None:
    if not LATEST_FILE.exists():
        return None

    with open(LATEST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)


def send_email(subject: str, body: str) -> None:
    if not all([SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_TO]):
        print("[WARN] Email config incomplete. Skipping email notification.")
        print("[WARN] Required: SMTP_USER, SMTP_PASS, EMAIL_FROM, EMAIL_TO")
        return

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message.set_content(body)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(message)


def build_email_body(snapshot: dict) -> str:
    added_lines = "\n".join(snapshot["added_admin_addpeer_lines"]) or "None"
    removed_lines = "\n".join(snapshot["removed_admin_addpeer_lines"]) or "None"
    unchanged_lines = "\n".join(snapshot["unchanged_admin_addpeer_lines"]) or "None"

    return f"""
{PROJECT_NAME}

DAC Official Enode list update detected.

Source:
{snapshot["source"]}

Source generated time:
{snapshot["generated_at_source"]}

Checked at UTC:
{snapshot["checked_at_utc"]}

Target port changed:
{snapshot["target_port_changed"]}

Previous target port:
{snapshot["previous_target_port"]}

Current target port:
{snapshot["current_target_port"]}

Change severity:
{snapshot["change_severity"]}

Severity reason:
{snapshot["severity_reason"]}

AI-style summary:
{snapshot["ai_style_summary"]["summary"]}

Rotation interpretation:
{snapshot["ai_style_summary"]["rotation_interpretation"]}

Technical impact:
{snapshot["technical_impact"]}

Recommended action:
{snapshot["recommended_action"]}

Previous total:
{snapshot["previous_total"]}

Current total:
{snapshot["current_total"]}

Added count:
{snapshot["added_count"]}

Removed count:
{snapshot["removed_count"]}

Unchanged count:
{snapshot["unchanged_count"]}

====================
ADDED ENODES
====================
{added_lines}

====================
REMOVED ENODES
====================
{removed_lines}

====================
UNCHANGED ENODES
====================
{unchanged_lines}

Snapshot file:
{snapshot["snapshot_file"]}
"""


def main() -> None:
    checked_at = datetime.now(timezone.utc).isoformat()
    filename_time = checked_at.replace(":", "-").replace(".", "-")

    print(f"[INFO] Checking DAC enode page at {checked_at}")
    print(f"[INFO] Source: {TARGET_URL}")

    page_text = fetch_page_text()
    source_info = extract_generated_info(page_text)
    current_enodes = extract_enodes(page_text)

    if not current_enodes:
        warning_snapshot = {
            "project": PROJECT_NAME,
            "source": TARGET_URL,
            "checked_at_utc": checked_at,
            "status": "warning_no_enodes_detected",
            "message": "No enode entries were detected from the target page."
        }

        warning_file = f"data/snapshots/{filename_time}-warning-no-enodes.json"
        warning_path = BASE_DIR / warning_file
        save_json(warning_path, warning_snapshot)

        send_email(
            "[DAC Enode Watcher] Warning: No enodes detected",
            f"""
No enode entries were detected.

Source:
{TARGET_URL}

Checked at UTC:
{checked_at}

Possible causes:
- DAC enode page structure changed
- Page temporarily unavailable
- Content rendering changed
- Regex parser needs update

Warning snapshot:
{warning_file}
"""
        )

        raise RuntimeError("No enodes detected.")

    previous_snapshot = load_latest()
    previous_enodes = previous_snapshot.get("enodes", []) if previous_snapshot else []

    previous_target_port = previous_snapshot.get("target_port") if previous_snapshot else None
    current_target_port = source_info["target_port"]

    current_set = set(current_enodes)
    previous_set = set(previous_enodes)

    added = sorted(current_set - previous_set)
    removed = sorted(previous_set - current_set)
    unchanged = sorted(current_set & previous_set)

    target_port_changed = (
        previous_snapshot is not None
        and previous_target_port != current_target_port
    )

    is_initial = previous_snapshot is None
    has_changed = bool(added or removed or target_port_changed)

    change_severity, severity_reason = classify_change(
        added=added,
        removed=removed,
        unchanged=unchanged,
        previous_enodes=previous_enodes,
        current_enodes=current_enodes,
        previous_target_port=previous_target_port,
        current_target_port=current_target_port,
        target_port_changed=target_port_changed,
        is_initial=is_initial
    )

    ai_style_summary = build_ai_style_summary(
        added=added,
        removed=removed,
        unchanged=unchanged,
        previous_enodes=previous_enodes,
        current_enodes=current_enodes,
        previous_target_port=previous_target_port,
        current_target_port=current_target_port,
        target_port_changed=target_port_changed,
        change_severity=change_severity,
        is_initial=is_initial
    )

    print(f"[INFO] Current enodes: {len(current_enodes)}")
    print(f"[INFO] Previous enodes: {len(previous_enodes)}")
    print(f"[INFO] Added: {len(added)} | Removed: {len(removed)} | Unchanged: {len(unchanged)}")
    print(f"[INFO] Target port: {previous_target_port} -> {current_target_port} | Changed: {target_port_changed}")
    print(f"[INFO] Change severity: {change_severity} | Reason: {severity_reason}")

    if not is_initial and not has_changed:
        print("[OK] No enode changes detected. No snapshot created.")
        return

    snapshot_type = "initial" if is_initial else "changed"
    snapshot_file = f"data/snapshots/{filename_time}-{snapshot_type}.json"
    snapshot_path = BASE_DIR / snapshot_file

    snapshot = {
        "project": PROJECT_NAME,
        "source": TARGET_URL,
        "status": snapshot_type,
        "checked_at_utc": checked_at,
        "generated_at_source": source_info["generated_at_source"],
        "target_port": current_target_port,
        "previous_target_port": previous_target_port,
        "current_target_port": current_target_port,
        "target_port_changed": target_port_changed,

        "change_severity": change_severity,
        "severity_reason": severity_reason,
        "ai_style_summary": ai_style_summary,
        "technical_impact": ai_style_summary["technical_impact"],
        "recommended_action": ai_style_summary["recommended_action"],

        "previous_total": len(previous_enodes),
        "current_total": len(current_enodes),

        "added_count": len(added),
        "removed_count": len(removed),
        "unchanged_count": len(unchanged),

        "added": added,
        "removed": removed,
        "unchanged": unchanged,
        "enodes": current_enodes,

        "added_details": [parse_enode_details(e) for e in added],
        "removed_details": [parse_enode_details(e) for e in removed],
        "unchanged_details": [parse_enode_details(e) for e in unchanged],
        "enode_details": [parse_enode_details(e) for e in current_enodes],

        "added_admin_addpeer_lines": [admin_addpeer_line(e) for e in added],
        "removed_admin_addpeer_lines": [admin_addpeer_line(e) for e in removed],
        "unchanged_admin_addpeer_lines": [admin_addpeer_line(e) for e in unchanged],
        "admin_addpeer_lines": [admin_addpeer_line(e) for e in current_enodes],

        "snapshot_file": snapshot_file
    }

    save_json(LATEST_FILE, snapshot)
    save_json(snapshot_path, snapshot)

    if is_initial:
        subject = f"[DAC Enode Watcher] Initial snapshot captured | {len(current_enodes)} enodes"
    else:
        if target_port_changed:
            subject = f"[DAC Enode Watcher] {change_severity} | port {previous_target_port} -> {current_target_port} | +{len(added)} / -{len(removed)}"
        else:
            subject = f"[DAC Enode Watcher] {change_severity} change | +{len(added)} / -{len(removed)}"

    email_body = build_email_body(snapshot)
    send_email(subject, email_body)

    print(f"[OK] {snapshot_type.capitalize()} snapshot saved.")
    print(f"[OK] latest.json updated.")
    print(f"[OK] Snapshot file: {snapshot_file}")


if __name__ == "__main__":
    main()
