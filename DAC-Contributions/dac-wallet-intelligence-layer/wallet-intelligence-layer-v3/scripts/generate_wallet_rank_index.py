#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Wallet Rank Intelligence

Core statement:
v3 turns every verified wallet variable into a comparative public rank signal.

This script generates wallet rank JSON artifacts from a source wallet metrics file.

Current phase:
- Local/static rank generation skeleton.
- Uses data/source-wallet-metrics.sample.json as input by default.
- Produces data/wallet-rank-summary.json and data/wallet-rank-index.json.

Future phase:
- Replace or extend the local input with Explorer API/RPC-derived wallet metrics.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


PROJECT = "Wallet Intelligence Layer v3.0.0"
FEATURE = "Wallet Rank Intelligence"
CORE_STATEMENT = "v3 turns every verified wallet variable into a comparative public rank signal."
NETWORK = "DAC Testnet"
CHAIN_ID = 21894
NATIVE_TOKEN = "DACC"
RANK_MODEL = "wallet-rank-intelligence-v3.0.0"

RANKING_VARIABLES = [
    "tx_count",
    "gas_used",
    "native_volume",
    "native_balance",
    "estimated_stake",
    "nft_holdings",
    "collection_diversity",
    "reputation_score",
    "low_sybil_risk",
]

METRIC_DEFINITIONS = {
    "tx_count": {
        "source_key": "tx_count",
        "higher_is_better": True,
    },
    "gas_used": {
        "source_key": "gas_used",
        "higher_is_better": True,
    },
    "native_volume": {
        "source_key": "native_volume",
        "higher_is_better": True,
    },
    "native_balance": {
        "source_key": "native_balance",
        "higher_is_better": True,
    },
    "estimated_stake": {
        "source_key": "estimated_stake",
        "higher_is_better": True,
    },
    "nft_holdings": {
        "source_key": "nft_holdings",
        "higher_is_better": True,
    },
    "collection_diversity": {
        "source_key": "collection_diversity",
        "higher_is_better": True,
    },
    "reputation_score": {
        "source_key": "reputation_score",
        "higher_is_better": True,
    },
    "low_sybil_risk": {
        "source_key": "sybil_risk_score",
        "higher_is_better": False,
    },
}


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_address(address: str) -> str:
    value = str(address or "").strip().lower()
    if not value.startswith("0x") or len(value) != 42:
        raise ValueError(f"Invalid EVM address: {address}")
    return value


def decimal_value(value: Any) -> Decimal:
    if value is None or value == "":
        return Decimal("0")

    try:
        return Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid numeric value: {value}") from exc


def json_value(value: Decimal) -> Any:
    if value == value.to_integral_value():
        try:
            return int(value)
        except OverflowError:
            return str(value)

    normalized = value.normalize()
    return format(normalized, "f")


def load_source_wallets(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"Source wallet metrics file not found: {path}")

    payload = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(payload, dict) and "wallets" in payload:
        wallets = payload["wallets"]
    elif isinstance(payload, list):
        wallets = payload
    else:
        raise ValueError("Source metrics must be a list or an object with a 'wallets' list.")

    if not isinstance(wallets, list):
        raise ValueError("'wallets' must be a list.")

    normalized_wallets = []
    seen = set()

    for wallet in wallets:
        if not isinstance(wallet, dict):
            raise ValueError("Each wallet entry must be an object.")

        address = normalize_address(wallet.get("address", ""))
        if address in seen:
            raise ValueError(f"Duplicate wallet address in source data: {address}")

        seen.add(address)

        metrics = wallet.get("metrics", {})
        if not isinstance(metrics, dict):
            raise ValueError(f"Wallet metrics must be an object: {address}")

        normalized_wallets.append(
            {
                "address": address,
                "metrics": metrics,
            }
        )

    return normalized_wallets


def rank_metric(wallets: Iterable[Dict[str, Any]], metric_key: str) -> Dict[str, int]:
    definition = METRIC_DEFINITIONS[metric_key]
    source_key = definition["source_key"]
    higher_is_better = definition["higher_is_better"]

    values: List[Tuple[str, Decimal]] = []

    for wallet in wallets:
        address = wallet["address"]
        metrics = wallet.get("metrics", {})
        value = decimal_value(metrics.get(source_key, 0))
        values.append((address, value))

    sorted_values = sorted(
        values,
        key=lambda item: (item[1], item[0]),
        reverse=higher_is_better,
    )

    ranks: Dict[str, int] = {}
    previous_value = None
    previous_rank = 0

    for index, (address, value) in enumerate(sorted_values, start=1):
        if previous_value is not None and value == previous_value:
            ranks[address] = previous_rank
        else:
            ranks[address] = index
            previous_rank = index
            previous_value = value

    return ranks


def percentile(rank: int, total: int) -> Decimal:
    if not total or not rank:
        return Decimal("0")
    return (Decimal(rank) / Decimal(total) * Decimal("100")).quantize(Decimal("0.01"))


def rank_tier(best_percentile: Decimal) -> str:
    if best_percentile <= Decimal("1"):
        return "TOP_1_PERCENT"
    if best_percentile <= Decimal("5"):
        return "TOP_5_PERCENT"
    if best_percentile <= Decimal("10"):
        return "TOP_10_PERCENT"
    if best_percentile <= Decimal("25"):
        return "TOP_25_PERCENT"
    if best_percentile <= Decimal("50"):
        return "TOP_50_PERCENT"
    return "INDEXED"


def build_rank_index(wallets: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    total = len(wallets)

    ranks_by_metric = {
        metric_key: rank_metric(wallets, metric_key)
        for metric_key in RANKING_VARIABLES
    }

    rank_index: Dict[str, Dict[str, Any]] = {}

    for wallet in wallets:
        address = wallet["address"]
        source_metrics = wallet.get("metrics", {})

        metrics: Dict[str, Any] = {}
        ranks: Dict[str, int] = {}
        percentiles: Dict[str, Any] = {}

        for metric_key in RANKING_VARIABLES:
            source_key = METRIC_DEFINITIONS[metric_key]["source_key"]
            value = decimal_value(source_metrics.get(source_key, 0))
            rank = ranks_by_metric[metric_key][address]
            metric_percentile = percentile(rank, total)

            if metric_key == "low_sybil_risk":
                metrics["sybil_risk_score"] = json_value(value)
            else:
                metrics[metric_key] = json_value(value)

            ranks[metric_key] = rank
            percentiles[metric_key] = json_value(metric_percentile)

        best_metric = min(percentiles.items(), key=lambda item: decimal_value(item[1]))[0]
        weakest_metric = max(percentiles.items(), key=lambda item: decimal_value(item[1]))[0]
        best_percentile = decimal_value(percentiles[best_metric])

        rank_index[address] = {
            "address": address,
            "metrics": metrics,
            "ranks": ranks,
            "percentiles": percentiles,
            "total_ranked_wallets": total,
            "rank_tier": rank_tier(best_percentile),
            "strongest_metric": best_metric,
            "weakest_metric": weakest_metric,
        }

    return rank_index


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_summary(total_wallets: int, source_path: Path) -> Dict[str, Any]:
    source_name = source_path.name

    if source_name == "source-wallet-metrics.generated.json":
        status = "GENERATED_FROM_EXPLORER_RPC_COLLECTOR"
        note = "Generated from Wallet Intelligence Layer v3 Explorer/RPC collector output."
    else:
        status = "GENERATED_FROM_LOCAL_SOURCE"
        note = "Generated by local Wallet Rank Intelligence skeleton. Explorer/RPC indexing is planned next."

    return {
        "project": PROJECT,
        "feature": FEATURE,
        "core_statement": CORE_STATEMENT,
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "rank_model": RANK_MODEL,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": status,
        "total_ranked_wallets": total_wallets,
        "latest_indexed_block": None,
        "ranking_variables": RANKING_VARIABLES,
        "source": str(source_path),
        "note": note,
    }


def main() -> None:
    root = project_root()
    parser = argparse.ArgumentParser(description="Generate Wallet Intelligence Layer v3 rank artifacts.")
    parser.add_argument(
        "--source",
        default=str(root / "data" / "source-wallet-metrics.sample.json"),
        help="Source wallet metrics JSON file.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(root / "data"),
        help="Output data directory.",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    out_dir = Path(args.out_dir)

    wallets = load_source_wallets(source_path)
    rank_index = build_rank_index(wallets)
    summary = build_summary(len(wallets), source_path)

    write_json(out_dir / "wallet-rank-index.json", rank_index)
    write_json(out_dir / "wallet-rank-summary.json", summary)

    print(f"[OK] Loaded wallets: {len(wallets)}")
    print(f"[OK] Wrote: {out_dir / 'wallet-rank-index.json'}")
    print(f"[OK] Wrote: {out_dir / 'wallet-rank-summary.json'}")


if __name__ == "__main__":
    main()
