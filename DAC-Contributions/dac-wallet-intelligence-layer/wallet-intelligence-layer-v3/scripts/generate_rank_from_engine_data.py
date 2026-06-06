#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Generate Rank From Rank Data Engine

Reads:
- rank-data-engine/data/latest.json

Writes:
- data/wallet-rank-summary.json
- data/wallet-rank-index.json
- data/rank-shards/{prefix}.json

This script calculates rank from the current normalized wallet_metrics produced by rank-data-engine.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict


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


def wei_to_native_string(wei: Any) -> str:
    amount = Decimal(str(wei or "0")) / Decimal(10**18)
    normalized = amount.normalize()

    if normalized == normalized.to_integral_value():
        return str(int(normalized))

    return format(normalized, "f")


def rank_percent(rank: int, total: int) -> str:
    if not rank or not total:
        return "0"

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


def dense_rank(records, key_func):
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


def main() -> None:
    root = project_root()
    engine_latest = root / "rank-data-engine" / "data" / "latest.json"
    out_dir = root / "data"
    shards_dir = out_dir / "rank-shards"

    latest = read_json(engine_latest)
    wallet_metrics = latest.get("wallet_metrics", {})

    if not wallet_metrics:
        raise SystemExit("rank-data-engine latest.json has no wallet_metrics yet.")

    records = []

    for address, metrics in wallet_metrics.items():
        records.append(
            {
                "address": address.lower(),
                "tx_count": int(metrics.get("tx_count", 0)),
                "gas_used": int(metrics.get("gas_used", 0)),
                "native_volume_wei": str(metrics.get("native_volume_wei", "0")),
                "first_seen_block": metrics.get("first_seen_block"),
                "last_seen_block": metrics.get("last_seen_block"),
                "updated_at": metrics.get("updated_at"),
            }
        )

    total_ranked = len(records)

    tx_ranks = dense_rank(records, lambda r: (-r["tx_count"], r["address"]))
    gas_ranks = dense_rank(records, lambda r: (-r["gas_used"], r["address"]))
    volume_ranks = dense_rank(
        records,
        lambda r: (-len(r["native_volume_wei"]), -int(r["native_volume_wei"]), r["address"]),
    )

    overall_seed = {}
    for record in records:
        address = record["address"]
        overall_seed[address] = (
            Decimal(tx_ranks[address]) / Decimal(total_ranked)
            + Decimal(gas_ranks[address]) / Decimal(total_ranked)
            + Decimal(volume_ranks[address]) / Decimal(total_ranked)
        )

    overall_ranks = dense_rank(records, lambda r: (overall_seed[r["address"]], r["address"]))

    if shards_dir.exists():
        shutil.rmtree(shards_dir)

    shards_dir.mkdir(parents=True, exist_ok=True)
    shard_payloads: Dict[str, Dict[str, Any]] = {}

    for record in records:
        address = record["address"]

        tx_rank = tx_ranks[address]
        gas_rank = gas_ranks[address]
        volume_rank = volume_ranks[address]
        overall_rank = overall_ranks[address]

        tx_percent = safe_decimal(rank_percent(tx_rank, total_ranked))
        gas_percent = safe_decimal(rank_percent(gas_rank, total_ranked))
        volume_percent = safe_decimal(rank_percent(volume_rank, total_ranked))
        best_percent = min(tx_percent, gas_percent, volume_percent)

        strongest_metric = min(
            [
                ("transactions", tx_percent),
                ("gas_used", gas_percent),
                ("native_volume", volume_percent),
            ],
            key=lambda item: item[1],
        )[0]

        shard = shard_for_address(address)
        shard_payload = shard_payloads.setdefault(shard, {})

        shard_payload[address] = {
            "address": address,
            "metrics": {
                "transactions": record["tx_count"],
                "gas_used": record["gas_used"],
                "native_volume": wei_to_native_string(record["native_volume_wei"]),
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None,
            },
            "ranks": {
                "transactions": tx_rank,
                "gas_used": gas_rank,
                "native_volume": volume_rank,
                "overall_rank": overall_rank,
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None,
            },
            "percentiles": {
                "transactions": rank_percent(tx_rank, total_ranked),
                "gas_used": rank_percent(gas_rank, total_ranked),
                "native_volume": rank_percent(volume_rank, total_ranked),
                "overall_rank": rank_percent(overall_rank, total_ranked),
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None,
            },
            "total_ranked_wallets": total_ranked,
            "rank_tier": rank_tier(best_percent),
            "strongest_metric": strongest_metric,
            "available_rank_variables": [
                "transactions",
                "gas_used",
                "native_volume",
                "overall_rank",
            ],
            "pending_rank_variables": [
                "native_funds",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk",
            ],
            "first_seen_block": record["first_seen_block"],
            "last_seen_block": record["last_seen_block"],
            "updated_at": record["updated_at"],
        }

    for shard, payload in shard_payloads.items():
        write_json(shards_dir / f"{shard}.json", payload)

    summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "core_statement": "v3 turns every verified wallet variable into a comparative public rank signal.",
        "network": "DAC Testnet",
        "chain_id": CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "rank_model": "wallet-rank-intelligence-v3.0.0-from-rank-data-engine",
        "status": "GENERATED_FROM_RANK_DATA_ENGINE",
        "generated_at": now_utc(),
        "rank_data_source": "rank-data-engine/data/latest.json",
        "engine_status": latest.get("status"),
        "engine_updated_at": latest.get("updated_at"),
        "engine_latest_snapshot": latest.get("latest_snapshot"),
        "engine_checkpoint": latest.get("checkpoint"),
        "sync_status": {
            "historical_backfill_complete": bool((latest.get("checkpoint") or {}).get("historical_backfill_complete")),
            "backfill_status": (latest.get("checkpoint") or {}).get("backfill_status"),
            "sync_phase": (latest.get("checkpoint") or {}).get("sync_phase"),
            "last_sync_at": (latest.get("checkpoint") or {}).get("last_sync_at"),
            "latest_snapshot": latest.get("latest_snapshot"),
            "latest_snapshot_time": latest.get("updated_at")
        },
        "total_ranked_wallets": total_ranked,
        "total_processed_transactions": latest.get("counters", {}).get("total_processed_transactions"),
        "ranking_variables": [
            "transactions",
            "gas_used",
            "native_volume",
            "overall_rank",
        ],
        "pending_ranking_variables": [
            "native_funds",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk",
        ],
        "rank_shards": {
            "directory": "data/rank-shards",
            "prefix_length": SHARD_PREFIX_LENGTH,
            "shard_count": len(shard_payloads),
        },
        "index_scope": {
            "source": "rank-data-engine normalized wallet_metrics",
            "raw_transaction_dump": False,
            "note": "Ranks are calculated from currently synced rank-data-engine wallet metrics.",
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

    print("[OK] Generated WIL v3 rank data from rank-data-engine")
    print(f"[OK] Ranked wallets: {total_ranked}")
    print(f"[OK] Shards: {len(shard_payloads)}")
    print(f"[OK] Summary: {out_dir / 'wallet-rank-summary.json'}")


if __name__ == "__main__":
    main()
