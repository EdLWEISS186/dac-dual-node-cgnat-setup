#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.2.0 — Generate Rank From Externalized Rank Data Engine

Reads:
- rank-data-engine/data/latest.json

Writes:
- data/wallet-rank-summary.json
- data/wallet-rank-index.json
- data/rank-shards/{prefix}.json

This script calculates comparative rank signals from variable-aware wallet metrics.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List


CHAIN_ID = 21894
NATIVE_TOKEN = "DACC"
SHARD_PREFIX_LENGTH = 2


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def to_int(value: Any) -> int:
    if value is None:
        return 0
    raw = str(value).strip()
    if raw.startswith("0x"):
        return int(raw, 16)
    if raw.isdigit():
        return int(raw)
    try:
        return int(Decimal(raw))
    except Exception:
        return 0


def wei_to_native_string(wei: Any) -> str:
    amount = Decimal(str(wei or "0")) / Decimal(10**18)
    normalized = amount.normalize()

    if normalized == normalized.to_integral_value():
        return str(int(normalized))

    return format(normalized, "f")


def rank_percent(rank: int, total: int) -> str:
    if not rank or not total:
        return "NaN"

    value = Decimal(rank) / Decimal(total) * Decimal("100")
    return format(value.quantize(Decimal("0.000001")), "f")


def safe_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value or "0"))
    except Exception:
        return Decimal("0")


def shard_for_address(address: str) -> str:
    return address[2:4].lower()


def rank_tier(best_percent: Decimal) -> str:
    if best_percent <= Decimal("1"):
        return "TOP_1_PERCENT"
    if best_percent <= Decimal("5"):
        return "TOP_5_PERCENT"
    if best_percent <= Decimal("10"):
        return "TOP_10_PERCENT"
    if best_percent <= Decimal("25"):
        return "TOP_25_PERCENT"
    if best_percent <= Decimal("50"):
        return "TOP_50_PERCENT"
    return "INDEXED"


def dense_rank(records: List[Dict[str, Any]], key_func):
    sorted_records = sorted(records, key=key_func)
    ranks = {}
    previous_value = None
    previous_rank = 0

    for index, record in enumerate(sorted_records, start=1):
        value = key_func(record)
        address = record["address"]

        if previous_value is not None and value == previous_value:
            ranks[address] = previous_rank
        else:
            ranks[address] = index
            previous_rank = index
            previous_value = value

    return ranks


def calculate_reputation_score(record: Dict[str, Any]) -> int:
    tx_count = record["transactions"]
    gas_used = record["gas_used"]
    native_balance = record["native_balance_wei"]
    native_volume = record["native_volume_wei"]
    nft_holdings = record["nft_holdings"]
    collection_diversity = record["collection_diversity"]
    successful_tx = record["successful_tx_count"]
    failed_tx = record["failed_tx_count"]
    unique_counterparties = record["unique_counterparty_count"]
    contract_interactions = record["contract_interaction_count"]

    score = 0

    score += min(tx_count, 100)
    score += min(gas_used // 21000, 100)
    score += min(native_volume // 10**15, 100)
    score += min(native_balance // 10**15, 100)
    score += min(nft_holdings * 2, 100)
    score += min(collection_diversity * 5, 100)
    score += min(unique_counterparties * 3, 100)
    score += min(contract_interactions * 2, 100)

    if successful_tx + failed_tx > 0:
        success_ratio = Decimal(successful_tx) / Decimal(successful_tx + failed_tx)
        score += int(success_ratio * Decimal(100))

    return int(score)


def calculate_low_sybil_risk_score(record: Dict[str, Any]) -> int:
    tx_count = record["transactions"]
    native_balance = record["native_balance_wei"]
    native_volume = record["native_volume_wei"]
    nft_holdings = record["nft_holdings"]
    collection_diversity = record["collection_diversity"]
    successful_tx = record["successful_tx_count"]
    failed_tx = record["failed_tx_count"]
    unique_counterparties = record["unique_counterparty_count"]

    score = 0

    score += min(tx_count * 2, 120)
    score += min(unique_counterparties * 5, 120)
    score += min(native_balance // 10**15, 120)
    score += min(native_volume // 10**15, 120)
    score += min(nft_holdings * 2, 80)
    score += min(collection_diversity * 8, 80)

    if failed_tx > successful_tx and failed_tx > 0:
        score -= min(failed_tx * 5, 80)

    if tx_count <= 1 and native_balance == 0 and nft_holdings == 0:
        score -= 80

    return max(int(score), 0)


def main() -> None:
    root = project_root()
    engine_latest = root / "rank-data-engine" / "data" / "latest.json"
    out_dir = root / "data"
    shards_dir = out_dir / "rank-shards"

    latest = read_json(engine_latest)
    wallet_metrics = latest.get("wallet_metrics", {})
    checkpoint = latest.get("checkpoint", {})
    counters = latest.get("counters", {})

    sync_phase = checkpoint.get("sync_phase")
    historical_complete = checkpoint.get("historical_backfill_complete") is True
    catch_up_status = checkpoint.get("catch_up_status")
    publish_ready = (
        sync_phase == "INCREMENTAL"
        and historical_complete
        and catch_up_status in ("CAUGHT_UP", None)
    )

    if not publish_ready:
        if shards_dir.exists():
            shutil.rmtree(shards_dir)

        summary = {
            "schema": "WIL_V3_RANK_SUMMARY",
            "version": "v3.2.0",
            "status": "EXTERNALIZED_STATE_BACKFILL_IN_PROGRESS",
            "has_valid_rank_index": False,
            "rank_lookup_enabled": False,
            "generated_at": now_utc(),
            "rank_data_source": "externalized-local-state",
            "externalized_state": True,
            "external_state_file": "~/wil-v3-rank-state/latest-state.json",
            "total_ranked_wallets": int(counters.get("total_indexed_wallets") or len(wallet_metrics)),
            "total_indexed_wallets": int(counters.get("total_indexed_wallets") or len(wallet_metrics)),
            "total_processed_transactions": int(counters.get("total_processed_transactions") or 0),
            "rank_shards": {
                "status": "DISABLED_DURING_BACKFILL",
                "directory": None,
                "reason": "Rank shards are not published while historical backfill uses externalized state storage."
            },
            "sync_status": {
                "phase": sync_phase,
                "historical_backfill_complete": historical_complete,
                "catch_up_status": catch_up_status,
                "historical_backfill_anchor_block": checkpoint.get("historical_backfill_anchor_block"),
                "last_synced_block": checkpoint.get("last_synced_block"),
                "local_rpc_backfill_next_block": checkpoint.get("local_rpc_backfill_next_block"),
                "catch_up_next_block": checkpoint.get("catch_up_next_block"),
                "incremental_next_block": checkpoint.get("incremental_next_block"),
                "local_rpc_latest_block_at_sync": checkpoint.get("local_rpc_latest_block_at_sync"),
                "last_sync_at": checkpoint.get("last_sync_at"),
            },
            "metrics": [
                "native_funds",
                "transactions",
                "gas_used",
                "native_volume",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk",
                "overall_rank"
            ],
            "note": "Rank lookup is temporarily disabled while the v3.2.0 externalized rank state architecture continues historical backfill."
        }

        index = {
            "schema": "WIL_V3_RANK_INDEX",
            "version": "v3.2.0",
            "status": "EXTERNALIZED_STATE_PENDING_VALID_PUBLISH",
            "mode": "EXTERNALIZED_STATE",
            "has_valid_rank_index": False,
            "directory": None,
            "summary": "Rank shards are intentionally not published during externalized historical backfill.",
            "externalized_state": True
        }

        write_json(out_dir / "wallet-rank-summary.json", summary)
        write_json(out_dir / "wallet-rank-index.json", index)

        print("[OK] WIL v3.2.0 externalized state summary generated")
        print("[OK] Rank shard publishing disabled during backfill")
        print(f"[OK] Summary: {out_dir / 'wallet-rank-summary.json'}")
        return

    if not wallet_metrics:
        raise SystemExit("rank-data-engine latest.json has no wallet_metrics yet.")

    records = []

    for address, metrics in wallet_metrics.items():
        address = address.lower()

        nft_collection_contracts = metrics.get("nft_collection_contract_addresses") or []
        asset_contracts = metrics.get("asset_contract_addresses") or []

        record = {
            "address": address,
            "native_balance_wei": to_int(metrics.get("native_balance_wei")),
            "transactions": to_int(metrics.get("tx_count")),
            "gas_used": to_int(metrics.get("gas_used_total", metrics.get("gas_used"))),
            "native_volume_wei": to_int(metrics.get("native_volume_wei")),
            "nft_holdings": to_int(metrics.get("nft_holdings_count")),
            "collection_diversity": len(set(nft_collection_contracts)),
            "asset_contract_count": len(set(asset_contracts)),
            "successful_tx_count": to_int(metrics.get("successful_tx_count")),
            "failed_tx_count": to_int(metrics.get("failed_tx_count")),
            "unique_counterparty_count": to_int(metrics.get("unique_counterparty_count")),
            "contract_interaction_count": to_int(metrics.get("contract_interaction_count")),
            "first_seen_block": metrics.get("first_seen_block"),
            "last_seen_block": metrics.get("last_seen_block"),
            "updated_at": metrics.get("updated_at"),
        }

        record["reputation_score"] = calculate_reputation_score(record)
        record["low_sybil_risk"] = calculate_low_sybil_risk_score(record)

        records.append(record)

    total_ranked = len(records)

    rank_specs = {
        "native_funds": lambda r: (-r["native_balance_wei"], r["address"]),
        "transactions": lambda r: (-r["transactions"], r["address"]),
        "gas_used": lambda r: (-r["gas_used"], r["address"]),
        "native_volume": lambda r: (-r["native_volume_wei"], r["address"]),
        "nft_holdings": lambda r: (-r["nft_holdings"], r["address"]),
        "collection_diversity": lambda r: (-r["collection_diversity"], r["address"]),
        "reputation_score": lambda r: (-r["reputation_score"], r["address"]),
        "low_sybil_risk": lambda r: (-r["low_sybil_risk"], r["address"]),
    }

    ranks = {name: dense_rank(records, key_func) for name, key_func in rank_specs.items()}

    overall_seed = {}
    for record in records:
        address = record["address"]
        rank_values = [Decimal(ranks[name][address]) / Decimal(total_ranked) for name in rank_specs]
        overall_seed[address] = sum(rank_values) / Decimal(len(rank_values))

    overall_ranks = dense_rank(records, lambda r: (overall_seed[r["address"]], r["address"]))

    if shards_dir.exists():
        shutil.rmtree(shards_dir)

    shards_dir.mkdir(parents=True, exist_ok=True)
    shard_payloads: Dict[str, Dict[str, Any]] = {}

    for record in records:
        address = record["address"]

        rank_values = {name: ranks[name][address] for name in rank_specs}
        rank_values["overall_rank"] = overall_ranks[address]

        percentiles = {
            name: rank_percent(rank, total_ranked)
            for name, rank in rank_values.items()
        }

        available_percents = [
            safe_decimal(percentiles[name])
            for name in [
                "native_funds",
                "transactions",
                "gas_used",
                "native_volume",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk",
            ]
            if percentiles.get(name) != "NaN"
        ]

        best_percent = min(available_percents) if available_percents else Decimal("100")

        strongest_metric = min(
            [
                ("native_funds", safe_decimal(percentiles["native_funds"])),
                ("transactions", safe_decimal(percentiles["transactions"])),
                ("gas_used", safe_decimal(percentiles["gas_used"])),
                ("native_volume", safe_decimal(percentiles["native_volume"])),
                ("nft_holdings", safe_decimal(percentiles["nft_holdings"])),
                ("collection_diversity", safe_decimal(percentiles["collection_diversity"])),
                ("reputation_score", safe_decimal(percentiles["reputation_score"])),
                ("low_sybil_risk", safe_decimal(percentiles["low_sybil_risk"])),
            ],
            key=lambda item: item[1],
        )[0]

        shard = shard_for_address(address)
        shard_payload = shard_payloads.setdefault(shard, {})

        shard_payload[address] = {
            "address": address,
            "metrics": {
                "native_funds": wei_to_native_string(record["native_balance_wei"]),
                "transactions": record["transactions"],
                "gas_used": record["gas_used"],
                "native_volume": wei_to_native_string(record["native_volume_wei"]),
                "nft_holdings": record["nft_holdings"],
                "collection_diversity": record["collection_diversity"],
                "reputation_score": record["reputation_score"],
                "low_sybil_risk": record["low_sybil_risk"],
            },
            "ranks": rank_values,
            "percentiles": percentiles,
            "total_ranked_wallets": total_ranked,
            "rank_tier": rank_tier(best_percent),
            "strongest_metric": strongest_metric,
            "available_rank_variables": [
                "native_funds",
                "transactions",
                "gas_used",
                "native_volume",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk",
                "overall_rank",
            ],
            "pending_rank_variables": [],
            "first_seen_block": record["first_seen_block"],
            "last_seen_block": record["last_seen_block"],
            "updated_at": record["updated_at"],
        }

    for shard, payload in shard_payloads.items():
        write_json(shards_dir / f"{shard}.json", payload)

    checkpoint = latest.get("checkpoint") or {}

    summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "core_statement": "v3 turns every verified wallet variable into a comparative public rank signal.",
        "network": "DAC Testnet",
        "chain_id": CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "rank_model": "wallet-rank-intelligence-v3.0.0-variable-aware-rank-engine",
        "status": "GENERATED_FROM_VARIABLE_AWARE_RANK_DATA_ENGINE",
        "generated_at": now_utc(),
        "rank_data_source": "rank-data-engine/data/latest.json",
        "engine_status": latest.get("status"),
        "engine_updated_at": latest.get("updated_at"),
        "engine_latest_snapshot": latest.get("latest_snapshot"),
        "engine_checkpoint": checkpoint,
        "sync_status": {
            "historical_backfill_complete": bool(checkpoint.get("historical_backfill_complete")),
            "backfill_status": checkpoint.get("backfill_status"),
            "sync_phase": checkpoint.get("sync_phase"),
            "last_sync_at": checkpoint.get("last_sync_at"),
            "latest_snapshot": latest.get("latest_snapshot"),
            "latest_snapshot_time": latest.get("updated_at"),
        },
        "total_ranked_wallets": total_ranked,
        "total_processed_transactions": latest.get("counters", {}).get("total_processed_transactions"),
        "ranking_variables": [
            "native_funds",
            "transactions",
            "gas_used",
            "native_volume",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk",
            "overall_rank",
        ],
        "pending_ranking_variables": [],
        "rank_shards": {
            "directory": "data/rank-shards",
            "prefix_length": SHARD_PREFIX_LENGTH,
            "shard_count": len(shard_payloads),
        },
        "index_scope": {
            "source": "rank-data-engine variable-aware wallet_metrics",
            "raw_transaction_dump": False,
            "note": "Ranks are calculated from normalized blockchain-derived wallet metrics collected by rank-data-engine.",
        },
    }

    write_json(out_dir / "wallet-rank-summary.json", summary)
    write_json(
        out_dir / "wallet-rank-index.json",
        {
            "mode": "SHARDED",
            "directory": "data/rank-shards",
            "summary": "Use rank-shards/{address_prefix}.json for wallet rank lookup.",
        },
    )

    print("[OK] Generated WIL v3 variable-aware rank data")
    print(f"[OK] Ranked wallets: {total_ranked}")
    print(f"[OK] Shards: {len(shard_payloads)}")
    print(f"[OK] Summary: {out_dir / 'wallet-rank-summary.json'}")


if __name__ == "__main__":
    main()
