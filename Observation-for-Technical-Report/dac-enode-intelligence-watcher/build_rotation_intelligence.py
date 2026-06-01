import json
from collections import Counter, defaultdict
from pathlib import Path

from provider_hints import detect_provider_hint


PROJECT_NAME = "DAC Enode Intelligence Watcher"
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
MANUAL_BACKFILL_DIR = DATA_DIR / "manual-backfill"
AUTOMATED_SNAPSHOT_DIR = DATA_DIR / "snapshots"
OUTPUT_FILE = DATA_DIR / "rotation-intelligence-summary.json"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def parse_enode_details(enode: str) -> dict:
    try:
        without_prefix = enode.replace("enode://", "")
        node_id, endpoint = without_prefix.split("@", 1)
        ip, port = endpoint.rsplit(":", 1)
        provider_hint = detect_provider_hint(ip)

        return {
            "enode": enode,
            "node_id": node_id,
            "ip": ip,
            "port": int(port),
            "provider_hint": provider_hint,
            "provider_guess": provider_hint.get("provider_guess"),
            "asn_hint": provider_hint.get("asn_hint"),
            "provider_type": provider_hint.get("provider_type"),
            "country_hint": provider_hint.get("country_hint"),
            "provider_confidence": provider_hint.get("confidence"),
            "provider_detection_method": provider_hint.get("detection_method"),
            "matched_prefix": provider_hint.get("matched_prefix"),
            "provider_notes": provider_hint.get("notes")
        }
    except Exception:
        provider_hint = detect_provider_hint(None)

        return {
            "enode": enode,
            "node_id": None,
            "ip": None,
            "port": None,
            "provider_hint": provider_hint,
            "provider_guess": provider_hint.get("provider_guess"),
            "asn_hint": provider_hint.get("asn_hint"),
            "provider_type": provider_hint.get("provider_type"),
            "country_hint": provider_hint.get("country_hint"),
            "provider_confidence": provider_hint.get("confidence"),
            "provider_detection_method": provider_hint.get("detection_method"),
            "matched_prefix": provider_hint.get("matched_prefix"),
            "provider_notes": provider_hint.get("notes")
        }


def snapshot_sort_key(snapshot: dict) -> str:
    if snapshot.get("generated_date") and snapshot.get("generated_time"):
        return f'{snapshot["generated_date"]}T{snapshot["generated_time"]}'

    if snapshot.get("checked_at_utc"):
        return snapshot["checked_at_utc"]

    if snapshot.get("generated_at_source"):
        return snapshot["generated_at_source"]

    return snapshot.get("snapshot_file", "")


def load_snapshots() -> list[dict]:
    snapshots = []

    for path in sorted(MANUAL_BACKFILL_DIR.glob("*-manual.json")):
        payload = load_json(path)
        payload["_phase"] = "manual_backfill"
        payload["_local_path"] = str(path.relative_to(BASE_DIR))
        snapshots.append(payload)

    for path in sorted(AUTOMATED_SNAPSHOT_DIR.glob("*.json")):
        payload = load_json(path)
        payload["_phase"] = "automated_watcher"
        payload["_local_path"] = str(path.relative_to(BASE_DIR))
        snapshots.append(payload)

    snapshots.sort(key=snapshot_sort_key)
    return snapshots


def build_presence_table(snapshots: list[dict]) -> list[dict]:
    enode_presence = defaultdict(list)

    for index, snapshot in enumerate(snapshots, start=1):
        for enode in snapshot.get("enodes", []):
            enode_presence[enode].append({
                "observation_index": index,
                "phase": snapshot["_phase"],
                "generated_at_source": snapshot.get("generated_at_source"),
                "checked_at_utc": snapshot.get("checked_at_utc"),
                "snapshot_file": snapshot.get("snapshot_file", snapshot["_local_path"])
            })

    table = []

    for enode, appearances in enode_presence.items():
        details = parse_enode_details(enode)

        table.append({
            "enode": enode,
            "node_id": details["node_id"],
            "ip": details["ip"],
            "port": details["port"],
            "appearance_count": len(appearances),
            "first_seen": appearances[0],
            "last_seen": appearances[-1],
            "phases_seen": sorted({item["phase"] for item in appearances}),
            "appearance_ratio": round(len(appearances) / len(snapshots), 4) if snapshots else 0,
            "appearances": appearances
        })

    table.sort(
        key=lambda item: (
            item["appearance_count"],
            item["last_seen"]["observation_index"]
        ),
        reverse=True
    )

    return table


def build_ip_table(snapshots: list[dict]) -> list[dict]:
    ip_presence = defaultdict(list)

    for index, snapshot in enumerate(snapshots, start=1):
        seen_ips_in_snapshot = set()

        for enode in snapshot.get("enodes", []):
            details = parse_enode_details(enode)
            ip = details["ip"]

            if not ip or ip in seen_ips_in_snapshot:
                continue

            seen_ips_in_snapshot.add(ip)

            ip_presence[ip].append({
                "observation_index": index,
                "phase": snapshot["_phase"],
                "generated_at_source": snapshot.get("generated_at_source"),
                "checked_at_utc": snapshot.get("checked_at_utc"),
                "snapshot_file": snapshot.get("snapshot_file", snapshot["_local_path"])
            })

    table = []

    for ip, appearances in ip_presence.items():
        provider_hint = detect_provider_hint(ip)

        table.append({
            "ip": ip,
            "provider_hint": provider_hint,
            "provider_guess": provider_hint.get("provider_guess"),
            "asn_hint": provider_hint.get("asn_hint"),
            "provider_type": provider_hint.get("provider_type"),
            "country_hint": provider_hint.get("country_hint"),
            "provider_confidence": provider_hint.get("confidence"),
            "provider_detection_method": provider_hint.get("detection_method"),
            "matched_prefix": provider_hint.get("matched_prefix"),
            "provider_notes": provider_hint.get("notes"),
            "appearance_count": len(appearances),
            "first_seen": appearances[0],
            "last_seen": appearances[-1],
            "phases_seen": sorted({item["phase"] for item in appearances}),
            "appearance_ratio": round(len(appearances) / len(snapshots), 4) if snapshots else 0,
            "appearances": appearances
        })

    table.sort(
        key=lambda item: (
            item["appearance_count"],
            item["last_seen"]["observation_index"]
        ),
        reverse=True
    )

    return table


def build_observation_timeline(snapshots: list[dict]) -> list[dict]:
    timeline = []

    for index, snapshot in enumerate(snapshots, start=1):
        timeline.append({
            "observation_index": index,
            "phase": snapshot["_phase"],
            "status": snapshot.get("status"),
            "generated_at_source": snapshot.get("generated_at_source"),
            "checked_at_utc": snapshot.get("checked_at_utc"),
            "target_port": snapshot.get("target_port"),
            "current_total": snapshot.get("current_total", len(snapshot.get("enodes", []))),
            "previous_total": snapshot.get("previous_total"),
            "added_count": snapshot.get("added_count"),
            "removed_count": snapshot.get("removed_count"),
            "unchanged_count": snapshot.get("unchanged_count"),
            "change_severity": snapshot.get("change_severity"),
            "severity_reason": snapshot.get("severity_reason"),
            "snapshot_file": snapshot.get("snapshot_file", snapshot["_local_path"])
        })

    return timeline


def build_transition_summary(timeline: list[dict]) -> dict:
    if not timeline:
        return {
            "largest_added_count": None,
            "largest_removed_count": None,
            "largest_total_delta": None,
            "high_rotation_observations": []
        }

    largest_added = max(timeline, key=lambda item: item.get("added_count") or 0)
    largest_removed = max(timeline, key=lambda item: item.get("removed_count") or 0)

    def total_delta(item):
        previous_total = item.get("previous_total")
        current_total = item.get("current_total")

        if previous_total is None or current_total is None:
            return 0

        return abs(current_total - previous_total)

    largest_delta = max(timeline, key=total_delta)

    high_rotation = [
        item for item in timeline
        if (item.get("added_count") or 0) + (item.get("removed_count") or 0) >= 6
    ]

    return {
        "largest_added_count": {
            "added_count": largest_added.get("added_count"),
            "observation_index": largest_added.get("observation_index"),
            "phase": largest_added.get("phase"),
            "generated_at_source": largest_added.get("generated_at_source"),
            "snapshot_file": largest_added.get("snapshot_file")
        },
        "largest_removed_count": {
            "removed_count": largest_removed.get("removed_count"),
            "observation_index": largest_removed.get("observation_index"),
            "phase": largest_removed.get("phase"),
            "generated_at_source": largest_removed.get("generated_at_source"),
            "snapshot_file": largest_removed.get("snapshot_file")
        },
        "largest_total_delta": {
            "total_delta": total_delta(largest_delta),
            "previous_total": largest_delta.get("previous_total"),
            "current_total": largest_delta.get("current_total"),
            "observation_index": largest_delta.get("observation_index"),
            "phase": largest_delta.get("phase"),
            "generated_at_source": largest_delta.get("generated_at_source"),
            "snapshot_file": largest_delta.get("snapshot_file")
        },
        "high_rotation_observations": high_rotation
    }


def main() -> None:
    snapshots = load_snapshots()

    if not snapshots:
        raise RuntimeError("No snapshots found. Cannot build rotation intelligence summary.")

    timeline = build_observation_timeline(snapshots)
    enode_table = build_presence_table(snapshots)
    ip_table = build_ip_table(snapshots)

    enode_counts = [item["current_total"] for item in timeline]
    target_ports = sorted({
        item["target_port"]
        for item in timeline
        if item["target_port"] is not None
    })

    phases = Counter(item["phase"] for item in timeline)
    severity_counts = Counter(
        item["change_severity"]
        for item in timeline
        if item.get("change_severity")
    )

    provider_counts = Counter(
        item.get("provider_guess") or "Unknown"
        for item in ip_table
    )

    asn_counts = Counter(
        item.get("asn_hint") or "Unknown"
        for item in ip_table
    )

    provider_type_counts = Counter(
        item.get("provider_type") or "Unknown"
        for item in ip_table
    )

    provider_confidence_counts = Counter(
        item.get("provider_confidence") or "LOW"
        for item in ip_table
    )

    provider_summary = [
        {
            "provider_guess": provider,
            "unique_ip_count": count,
            "ips": sorted([
                item["ip"]
                for item in ip_table
                if (item.get("provider_guess") or "Unknown") == provider
            ])
        }
        for provider, count in provider_counts.most_common()
    ]

    asn_summary = [
        {
            "asn_hint": asn,
            "unique_ip_count": count,
            "ips": sorted([
                item["ip"]
                for item in ip_table
                if (item.get("asn_hint") or "Unknown") == asn
            ])
        }
        for asn, count in asn_counts.most_common()
    ]

    provider_asn_groups = {}

    for item in ip_table:
        key = (
            item.get("provider_guess") or "Unknown",
            item.get("asn_hint") or "Unknown",
            item.get("provider_type") or "Unknown",
            item.get("country_hint") or "Unknown",
            item.get("provider_confidence") or "LOW"
        )

        provider_asn_groups.setdefault(key, []).append(item["ip"])

    provider_asn_summary = [
        {
            "provider_guess": provider,
            "asn_hint": asn,
            "provider_type": provider_type,
            "country_hint": country,
            "confidence": confidence,
            "unique_ip_count": len(ips),
            "ips": sorted(ips)
        }
        for (provider, asn, provider_type, country, confidence), ips in provider_asn_groups.items()
    ]

    provider_asn_summary.sort(
        key=lambda item: (
            item["provider_guess"] == "Unknown",
            -item["unique_ip_count"],
            item["provider_guess"],
            item["asn_hint"]
        )
    )

    most_persistent_enodes = enode_table[:10]
    most_persistent_ips = ip_table[:10]

    summary = {
        "project": PROJECT_NAME,
        "summary_type": "enode_rotation_intelligence",
        "description": "Aggregated rotation intelligence derived from manual backfill and automated watcher snapshots.",
        "observation_scope": {
            "manual_backfill_snapshots": phases.get("manual_backfill", 0),
            "automated_watcher_snapshots": phases.get("automated_watcher", 0),
            "total_snapshots": len(timeline),
            "first_observation": timeline[0],
            "latest_observation": timeline[-1]
        },
        "coverage_note": "Manual backfill is a partial archive. Missing dates represent missed observation windows, not confirmed absence of changes.",
        "target_ports_observed": target_ports,
        "enode_count_statistics": {
            "minimum": min(enode_counts),
            "maximum": max(enode_counts),
            "average": round(sum(enode_counts) / len(enode_counts), 2)
        },
        "unique_enode_count": len(enode_table),
        "unique_ip_count": len(ip_table),
        "severity_counts": dict(severity_counts),
        "provider_detection": {
            "method": "static_prefix_heuristic",
            "machine_learning_used": False,
            "live_asn_lookup_used": False,
            "confidence_note": "Provider and ASN values are heuristic hints based on static IP prefix matching. Treat as enrichment, not final verified ASN truth."
        },
        "provider_counts": dict(provider_counts),
        "asn_counts": dict(asn_counts),
        "provider_type_counts": dict(provider_type_counts),
        "provider_confidence_counts": dict(provider_confidence_counts),
        "provider_summary": provider_summary,
        "asn_summary": asn_summary,
        "provider_asn_summary": provider_asn_summary,
        "most_persistent_enodes": most_persistent_enodes,
        "most_persistent_ips": most_persistent_ips,
        "transition_summary": build_transition_summary(timeline),
        "observation_timeline": timeline,
        "report_ready_summary": {
            "short_summary": (
                f"Across {len(timeline)} total observations, the DAC official enode list "
                f"showed {len(enode_table)} unique enodes and {len(ip_table)} unique IPs. "
                f"The observed target port remained within {target_ports}. "
                f"Enode count ranged from {min(enode_counts)} to {max(enode_counts)}, "
                f"with an average of {round(sum(enode_counts) / len(enode_counts), 2)}."
            ),
            "manual_to_automated_context": (
                "The dataset combines partial manual observations from the pre-watcher period "
                "with automated GitHub Actions snapshots after the watcher was deployed."
            ),
            "technical_value": (
                "This summary provides a structured basis for analyzing bootstrap peer rotation, "
                "persistent official enodes, IP recurrence, provider hints, ASN hints, and possible infrastructure maturation patterns."
            )
        }
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    print(f"[OK] Rotation intelligence summary generated: {OUTPUT_FILE}")
    print(f"[OK] Total observations: {len(timeline)}")
    print(f"[OK] Manual backfill snapshots: {phases.get('manual_backfill', 0)}")
    print(f"[OK] Automated watcher snapshots: {phases.get('automated_watcher', 0)}")
    print(f"[OK] Unique enodes: {len(enode_table)}")
    print(f"[OK] Unique IPs: {len(ip_table)}")
    print(f"[OK] Provider hints: {dict(provider_counts)}")
    print(f"[OK] ASN hints: {dict(asn_counts)}")
    print(f"[OK] Provider / ASN groups: {len(provider_asn_summary)}")
    print(f"[OK] Target ports observed: {target_ports}")
    print(f"[OK] Enode count min/max/avg: {min(enode_counts)} / {max(enode_counts)} / {round(sum(enode_counts) / len(enode_counts), 2)}")


if __name__ == "__main__":
    main()
