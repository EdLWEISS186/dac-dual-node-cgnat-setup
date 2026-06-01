from ipaddress import ip_address


DISCLAIMER = (
    "DAC Infrastructure Signal is a community inference layer based on observed registry history, "
    "peer identity strings, persistence, subnet patterns, and provider hints. It is not an official DAC "
    "classification and should not be treated as confirmed node ownership."
)


SIGNAL_SOURCE_REFERENCE = (
    "Derived from community observation evidence in Report 5: Official Enode Evolution Analysis — "
    "Infrastructure Rotation & Network Maturation, plus watcher observation history."
)


KNOWN_IP_SIGNALS = {
    "157.173.127.31": {
        "dac_infrastructure_signal": "Authority-like Core Signal",
        "signal_category": "authority_like_core",
        "signal_confidence": "HIGH",
        "peer_identity_hint": "DAC Testnet Authority 1",
        "historical_registry_status": "Observed in official registry phases; later removed but observed active via peer topology evidence.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as DAC Testnet Authority 1.",
            "Part of recurring 157.173.127.x cluster.",
            "Observed across multiple registry phases.",
            "Removed from later published registry but still observed as active peer in the referenced report."
        ]
    },
    "157.173.127.30": {
        "dac_infrastructure_signal": "Authority-like Core Signal",
        "signal_category": "authority_like_core",
        "signal_confidence": "HIGH",
        "peer_identity_hint": "DAC Testnet Authority 2",
        "historical_registry_status": "Long-surviving registry node across multiple phases.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as DAC Testnet Authority 2.",
            "Part of recurring 157.173.127.x cluster.",
            "Marked in prior analysis as long-surviving core backbone infrastructure."
        ]
    },
    "157.173.127.21": {
        "dac_infrastructure_signal": "Authority-like Core Signal",
        "signal_category": "authority_like_core",
        "signal_confidence": "HIGH",
        "peer_identity_hint": "DAC Testnet Authority 3",
        "historical_registry_status": "Long-surviving registry node across multiple phases.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as DAC Testnet Authority 3.",
            "Part of recurring 157.173.127.x cluster.",
            "Marked in prior analysis as long-surviving core backbone infrastructure."
        ]
    },
    "157.173.127.22": {
        "dac_infrastructure_signal": "Core Subnet Historical Signal",
        "signal_category": "core_subnet_historical",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": None,
        "historical_registry_status": "Observed in early bootstrap phases.",
        "signal_basis": [
            "Part of the recurring 157.173.127.x cluster.",
            "Appeared in earliest bootstrap observations.",
            "Prior analysis treated the subnet as coordinated early bootstrap infrastructure."
        ]
    },
    "157.173.127.18": {
        "dac_infrastructure_signal": "Core Subnet Historical Signal",
        "signal_category": "core_subnet_historical",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": None,
        "historical_registry_status": "Observed in early bootstrap phases.",
        "signal_basis": [
            "Part of the recurring 157.173.127.x cluster.",
            "Appeared in earliest bootstrap observations.",
            "Prior analysis treated the subnet as coordinated early bootstrap infrastructure."
        ]
    },
    "84.46.253.182": {
        "dac_infrastructure_signal": "Internal RPC-like Signal",
        "signal_category": "internal_rpc_like",
        "signal_confidence": "HIGH",
        "peer_identity_hint": "DAC Testnet RPC 03",
        "historical_registry_status": "Never published in the official enode registry in the referenced report.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as DAC Testnet RPC 03.",
            "Observed as active peer despite not appearing in the published registry.",
            "Identity string suggests RPC infrastructure role."
        ]
    },
    "206.189.127.204": {
        "dac_infrastructure_signal": "Relay-like DAC Node Signal",
        "signal_category": "relay_like",
        "signal_confidence": "HIGH",
        "peer_identity_hint": "DAC-Node 05",
        "historical_registry_status": "Observed across multiple registry phases.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as DAC-Node 05.",
            "Observed in multiple official registry phases.",
            "Prior analysis classified it as a proven relay / bootnode-style participant."
        ]
    },
    "152.228.141.231": {
        "dac_infrastructure_signal": "Legacy Relay-like Signal",
        "signal_category": "legacy_relay_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "gdacnode legacy build",
        "historical_registry_status": "Observed across later registry phases.",
        "signal_basis": [
            "Previously observed as gdacnode legacy build in peer identity evidence.",
            "Observed in official registry phases.",
            "Prior analysis classified it as an EU relay-like node."
        ]
    },
    "217.76.53.98": {
        "dac_infrastructure_signal": "Community VPS-like Signal",
        "signal_category": "community_vps_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "whale-vps1",
        "historical_registry_status": "Observed as replacement / addition in later registry phase.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as whale-vps1.",
            "Appeared as a newer replacement / addition.",
            "Prior analysis classified it as community VPS-like infrastructure."
        ]
    },
    "156.67.104.212": {
        "dac_infrastructure_signal": "Community VPS-like Signal",
        "signal_category": "community_vps_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "whale-vps2",
        "historical_registry_status": "Observed in prior registry phases; later removed but observed active via peer topology evidence.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as whale-vps2.",
            "Observed in prior registry phases.",
            "Removed from later registry but still observed as active peer in the referenced report."
        ]
    },
    "161.97.89.27": {
        "dac_infrastructure_signal": "Community VPS-like Signal",
        "signal_category": "community_vps_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "whale-vps3",
        "historical_registry_status": "Observed in prior registry phase; later removed but observed active via peer topology evidence.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as whale-vps3.",
            "Observed in prior registry phase.",
            "Removed from later registry but still observed as active peer in the referenced report."
        ]
    },
    "5.104.86.129": {
        "dac_infrastructure_signal": "Community Node Signal",
        "signal_category": "community_node_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "x0rabbit",
        "historical_registry_status": "Observed across later registry phases.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as x0rabbit.",
            "Observed in later registry phases.",
            "Prior analysis classified it as retained after evaluation / community node-like infrastructure."
        ]
    },
    "213.136.82.243": {
        "dac_infrastructure_signal": "Unlisted Active Peer Signal",
        "signal_category": "unlisted_active_peer",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "SAPInode",
        "historical_registry_status": "Never published in the official enode registry in the referenced report.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as SAPInode.",
            "Observed as active peer despite not appearing in the published registry.",
            "Prior analysis classified it as unlisted active peer."
        ]
    },
    "95.216.70.180": {
        "dac_infrastructure_signal": "Community VPS-like Signal",
        "signal_category": "community_vps_like",
        "signal_confidence": "MEDIUM",
        "peer_identity_hint": "Fertal",
        "historical_registry_status": "Observed in prior registry phase; later removed but observed active via peer topology evidence.",
        "signal_basis": [
            "Previously identified through admin.peers evidence as Fertal.",
            "Prior analysis associated it with Hetzner-style relay infrastructure.",
            "Removed from later registry but still observed as active peer in the referenced report."
        ]
    },
    "1.54.141.126": {
        "dac_infrastructure_signal": "External / Dynamic Participant Signal",
        "signal_category": "external_dynamic_participant",
        "signal_confidence": "LOW",
        "peer_identity_hint": None,
        "historical_registry_status": "Observed during high-count expansion phase.",
        "signal_basis": [
            "Prior analysis noted possible residential or dynamic IP characteristics.",
            "May represent external or community-operated validator participation.",
            "Low confidence because identity evidence is not available."
        ]
    },
    "144.91.74.181": {
        "dac_infrastructure_signal": "Temporary Infrastructure Signal",
        "signal_category": "temporary_infrastructure",
        "signal_confidence": "LOW",
        "peer_identity_hint": None,
        "historical_registry_status": "Observed in prior expansion phase.",
        "signal_basis": [
            "Observed during multi-provider expansion period.",
            "Prior analysis treated it as temporary or experimental infrastructure.",
            "Low confidence because identity evidence is not available."
        ]
    },
}


def _base_result(ip: str) -> dict:
    return {
        "ip": ip,
        "dac_infrastructure_signal": "Unknown / No Signal",
        "signal_category": "unknown",
        "signal_confidence": "LOW",
        "peer_identity_hint": None,
        "historical_registry_status": "No known prior signal mapping.",
        "signal_basis": [
            "No static DAC Infrastructure Signal mapping matched this IP."
        ],
        "official_ownership_claim": False,
        "detection_method": "static_report_evidence_and_observation_heuristic",
        "source_reference": SIGNAL_SOURCE_REFERENCE,
        "disclaimer": DISCLAIMER
    }


def detect_dac_infrastructure_signal(
    ip: str,
    provider_hint: dict | None = None,
    appearance_count: int | None = None,
    appearance_ratio: float | None = None,
    phases_seen: list[str] | None = None
) -> dict:
    result = _base_result(ip)

    if not ip:
        result["historical_registry_status"] = "Missing IP."
        result["signal_basis"] = ["No IP was provided for DAC Infrastructure Signal detection."]
        return result

    try:
        parsed_ip = ip_address(ip)
    except ValueError:
        result["historical_registry_status"] = "Invalid IP."
        result["signal_basis"] = ["Invalid IP format."]
        return result

    if ip in KNOWN_IP_SIGNALS:
        signal = KNOWN_IP_SIGNALS[ip]
        result.update(signal)
        result["official_ownership_claim"] = False
        result["detection_method"] = "static_report_evidence_and_observation_heuristic"
        result["source_reference"] = SIGNAL_SOURCE_REFERENCE
        result["disclaimer"] = DISCLAIMER
        return result

    if ip.startswith("157.173.127."):
        result.update({
            "dac_infrastructure_signal": "Core Subnet Pattern Signal",
            "signal_category": "core_subnet_pattern",
            "signal_confidence": "MEDIUM",
            "historical_registry_status": "Matched recurring 157.173.127.x subnet pattern.",
            "signal_basis": [
                "IP belongs to the recurring 157.173.127.x cluster observed in prior registry phases.",
                "No exact peer identity mapping is available for this IP in the static signal map."
            ]
        })
        return result

    provider_guess = None
    if provider_hint:
        provider_guess = provider_hint.get("provider_guess")

    if appearance_count is not None and appearance_count >= 10:
        result.update({
            "dac_infrastructure_signal": "Retained Infrastructure Signal",
            "signal_category": "retained_infrastructure",
            "signal_confidence": "MEDIUM",
            "historical_registry_status": "High persistence across watcher observations.",
            "signal_basis": [
                f"Observed {appearance_count} times across available watcher history.",
                "High persistence can indicate retained infrastructure, but does not confirm ownership."
            ]
        })

        if appearance_ratio is not None:
            result["signal_basis"].append(f"Appearance ratio: {appearance_ratio}")

        if provider_guess and provider_guess != "Unknown":
            result["signal_basis"].append(f"Provider hint: {provider_guess}")

        return result

    if provider_guess and provider_guess != "Unknown":
        result.update({
            "dac_infrastructure_signal": "Provider-backed Observation Signal",
            "signal_category": "provider_backed_observation",
            "signal_confidence": "LOW",
            "historical_registry_status": "Provider hint available, but no DAC-specific role signal matched.",
            "signal_basis": [
                f"Provider hint detected: {provider_guess}",
                "No DAC-specific identity, survivorship, or subnet signal matched this IP."
            ]
        })
        return result

    return result


def summarize_signal_counts(signal_rows: list[dict]) -> dict:
    summary = {}

    for row in signal_rows:
        signal = row.get("dac_infrastructure_signal") or "Unknown / No Signal"
        summary[signal] = summary.get(signal, 0) + 1

    return dict(sorted(summary.items(), key=lambda item: (-item[1], item[0])))
