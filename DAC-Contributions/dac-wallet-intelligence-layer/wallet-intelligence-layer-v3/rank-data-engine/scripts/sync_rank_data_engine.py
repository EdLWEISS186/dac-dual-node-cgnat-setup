#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Rank Data Engine

Variable-aware blockchain data engine.

This engine stores normalized wallet metrics only.
It does not store raw transaction dumps and does not calculate final ranks.

Collected data:
- wallet identity
- tx activity
- gas usage
- native volume
- native balance snapshot
- token/NFT holdings snapshot
- NFT collection contract set
- counterparty / contract interaction signals
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


EXPLORER_API_V2 = "https://exptest.dachain.tech/api/v2"
TRANSACTIONS_ENDPOINT = f"{EXPLORER_API_V2}/transactions"
STATS_ENDPOINT = f"{EXPLORER_API_V2}/stats"

REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 0.12


def engine_root() -> Path:
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    return engine_root() / "data"


def latest_path() -> Path:
    return data_dir() / "latest.json"


def snapshots_dir() -> Path:
    return data_dir() / "snapshots"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def snapshot_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace(":", "-").replace(".", "-").replace("+", "+").replace("Z", "")


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required JSON file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if params:
        clean = {key: value for key, value in params.items() if value is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "WIL-v3-rank-data-engine/2.0",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_address(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("hash")

    address = str(value or "").strip().lower()
    if address.startswith("0x") and len(address) == 42:
        return address
    return ""


def normalize_hash(value: Any) -> str:
    tx_hash = str(value or "").strip().lower()
    if tx_hash.startswith("0x") and len(tx_hash) == 66:
        return tx_hash
    return ""


def to_int(value: Any) -> int:
    raw = str(value or "0").strip()
    if raw.startswith("0x"):
        return int(raw, 16)
    if raw.isdigit():
        return int(raw)
    return 0


def tx_success(tx: Dict[str, Any]) -> bool:
    status = str(tx.get("status") or tx.get("result") or "").lower()
    return status in {"ok", "success", "1", "true"}


def ensure_metric(wallet_metrics: Dict[str, Any], address: str) -> Dict[str, Any]:
    return wallet_metrics.setdefault(
        address,
        {
            "address": address,
            "is_contract": None,

            "tx_count": 0,
            "incoming_tx_count": 0,
            "outgoing_tx_count": 0,
            "successful_tx_count": 0,
            "failed_tx_count": 0,

            "gas_used_total": 0,
            "gas_used_outgoing": 0,

            "native_volume_wei": "0",
            "incoming_native_volume_wei": "0",
            "outgoing_native_volume_wei": "0",

            "native_balance_wei": None,
            "balance_snapshot_block": None,
            "balance_snapshot_time": None,

            "has_tokens": None,
            "has_token_transfers": None,
            "token_holdings_count": None,
            "nft_holdings_count": None,
            "asset_contract_addresses": [],
            "nft_collection_contract_addresses": [],
            "asset_snapshot_time": None,

            "unique_counterparty_count": 0,
            "counterparty_addresses": [],
            "contract_interaction_count": 0,
            "repeated_counterparty_count": 0,

            "first_seen_block": None,
            "last_seen_block": None,
            "first_seen_tx": None,
            "last_seen_tx": None,
            "last_activity_time": None,
            "updated_at": now_utc(),
        },
    )


def bump_block_range(metric: Dict[str, Any], block_number: int, tx_hash: str, timestamp: Optional[str]) -> None:
    if block_number:
        if metric.get("first_seen_block") is None or block_number < int(metric["first_seen_block"]):
            metric["first_seen_block"] = block_number
            metric["first_seen_tx"] = tx_hash

        if metric.get("last_seen_block") is None or block_number > int(metric["last_seen_block"]):
            metric["last_seen_block"] = block_number
            metric["last_seen_tx"] = tx_hash

    if timestamp:
        metric["last_activity_time"] = timestamp

    metric["updated_at"] = now_utc()


def add_counterparty(metric: Dict[str, Any], counterparty: str) -> None:
    if not counterparty:
        return

    addresses: List[str] = metric.setdefault("counterparty_addresses", [])
    if counterparty in addresses:
        metric["repeated_counterparty_count"] = int(metric.get("repeated_counterparty_count") or 0) + 1
    else:
        addresses.append(counterparty)
        addresses.sort()

    metric["unique_counterparty_count"] = len(addresses)


def process_transaction(
    tx: Dict[str, Any],
    wallet_metrics: Dict[str, Any],
    wallet_deltas: Dict[str, Any],
    enrichment_queue: Set[str],
) -> Optional[Dict[str, Any]]:
    tx_hash = normalize_hash(tx.get("hash"))
    if not tx_hash:
        return None

    block_number = to_int(tx.get("block_number"))
    timestamp = tx.get("timestamp")

    from_address = normalize_address(tx.get("from"))
    to_address = normalize_address(tx.get("to"))

    gas_used = to_int(tx.get("gas_used"))
    value_wei = to_int(tx.get("value"))
    success = tx_success(tx)

    to_is_contract = bool((tx.get("to") or {}).get("is_contract")) if isinstance(tx.get("to"), dict) else False
    from_is_contract = bool((tx.get("from") or {}).get("is_contract")) if isinstance(tx.get("from"), dict) else False

    touched: Set[str] = set()

    if from_address:
        metric = ensure_metric(wallet_metrics, from_address)
        metric["is_contract"] = from_is_contract
        metric["tx_count"] += 1
        metric["outgoing_tx_count"] += 1
        metric["gas_used_total"] += gas_used
        metric["gas_used_outgoing"] += gas_used
        metric["outgoing_native_volume_wei"] = str(int(metric["outgoing_native_volume_wei"]) + value_wei)
        metric["native_volume_wei"] = str(int(metric["native_volume_wei"]) + value_wei)

        if success:
            metric["successful_tx_count"] += 1
        else:
            metric["failed_tx_count"] += 1

        if to_is_contract:
            metric["contract_interaction_count"] += 1

        add_counterparty(metric, to_address)
        bump_block_range(metric, block_number, tx_hash, timestamp)
        touched.add(from_address)

    if to_address and to_address != from_address:
        metric = ensure_metric(wallet_metrics, to_address)
        metric["is_contract"] = to_is_contract
        metric["tx_count"] += 1
        metric["incoming_tx_count"] += 1
        metric["incoming_native_volume_wei"] = str(int(metric["incoming_native_volume_wei"]) + value_wei)
        metric["native_volume_wei"] = str(int(metric["native_volume_wei"]) + value_wei)
        add_counterparty(metric, from_address)
        bump_block_range(metric, block_number, tx_hash, timestamp)
        touched.add(to_address)

    for address in touched:
        enrichment_queue.add(address)
        wallet_deltas[address] = deepcopy(wallet_metrics[address])

    return {
        "hash": tx_hash,
        "block_number": block_number,
    }


def fetch_address_detail(address: str) -> Dict[str, Any]:
    return fetch_json(f"{EXPLORER_API_V2}/addresses/{address}")


def fetch_address_tokens(address: str) -> Dict[str, Any]:
    return fetch_json(f"{EXPLORER_API_V2}/addresses/{address}/tokens")


def summarize_tokens(payload: Dict[str, Any]) -> Dict[str, Any]:
    items = payload.get("items") or []

    asset_contracts: Set[str] = set()
    nft_contracts: Set[str] = set()
    token_holdings_count = 0
    nft_holdings_count = 0

    for item in items:
        if not isinstance(item, dict):
            continue

        token = item.get("token") or {}
        contract = normalize_address(token.get("address_hash"))
        token_type = str(token.get("type") or "").upper()
        value = to_int(item.get("value"))

        if contract:
            asset_contracts.add(contract)

        if token_type in {"ERC-721", "ERC-1155"}:
            if contract:
                nft_contracts.add(contract)
            nft_holdings_count += value
        else:
            token_holdings_count += 1

    return {
        "token_holdings_count": token_holdings_count,
        "nft_holdings_count": nft_holdings_count,
        "asset_contract_addresses": sorted(asset_contracts),
        "nft_collection_contract_addresses": sorted(nft_contracts),
    }


def enrich_wallet(address: str, wallet_metrics: Dict[str, Any]) -> bool:
    metric = ensure_metric(wallet_metrics, address)
    updated = False

    try:
        detail = fetch_address_detail(address)
        metric["native_balance_wei"] = str(detail.get("coin_balance") or "0")
        metric["balance_snapshot_block"] = detail.get("block_number_balance_updated_at")
        metric["balance_snapshot_time"] = now_utc()
        metric["has_tokens"] = bool(detail.get("has_tokens"))
        metric["has_token_transfers"] = bool(detail.get("has_token_transfers"))
        metric["is_contract"] = bool(detail.get("is_contract"))
        updated = True
    except Exception as error:
        print(f"[WARN] address detail failed for {address}: {error}")

    time.sleep(REQUEST_DELAY_SECONDS)

    try:
        tokens = fetch_address_tokens(address)
        token_summary = summarize_tokens(tokens)

        metric["token_holdings_count"] = token_summary["token_holdings_count"]
        metric["nft_holdings_count"] = token_summary["nft_holdings_count"]
        metric["asset_contract_addresses"] = token_summary["asset_contract_addresses"]
        metric["nft_collection_contract_addresses"] = token_summary["nft_collection_contract_addresses"]
        metric["asset_snapshot_time"] = now_utc()
        updated = True
    except Exception as error:
        print(f"[WARN] address tokens failed for {address}: {error}")

    metric["updated_at"] = now_utc()
    return updated


def run_sync(max_pages: int, enrich_limit: int) -> Dict[str, Any]:
    latest = read_json(latest_path())
    checkpoint_before = deepcopy(latest.get("checkpoint", {}))

    wallet_metrics = latest.setdefault("wallet_metrics", {})
    enrichment_queue: Set[str] = set(latest.get("enrichment_queue", []))

    historical_backfill_complete = bool(checkpoint_before.get("historical_backfill_complete"))
    mode = "INCREMENTAL_SYNC" if historical_backfill_complete else "HISTORICAL_BACKFILL"

    cursor = checkpoint_before.get("last_transaction_cursor")
    if mode == "INCREMENTAL_SYNC":
        cursor = None

    wallet_deltas: Dict[str, Any] = {}
    processed_transactions = 0
    first_tx_hash = None
    last_tx_hash = None
    first_block = None
    last_block = None
    next_cursor = cursor
    stop_reason = None

    for _page_index in range(max_pages):
        payload = fetch_json(TRANSACTIONS_ENDPOINT, next_cursor)
        items = payload.get("items", [])

        if not isinstance(items, list) or not items:
            stop_reason = "NO_MORE_ITEMS"
            next_cursor = None
            break

        for tx in items:
            if not isinstance(tx, dict):
                continue

            audit = process_transaction(tx, wallet_metrics, wallet_deltas, enrichment_queue)
            if not audit:
                continue

            processed_transactions += 1
            first_tx_hash = first_tx_hash or audit["hash"]
            last_tx_hash = audit["hash"]
            first_block = audit["block_number"] if first_block is None else max(first_block, audit["block_number"])
            last_block = audit["block_number"] if last_block is None else min(last_block, audit["block_number"])

        next_cursor = payload.get("next_page_params")
        if not next_cursor:
            stop_reason = "NO_NEXT_PAGE_PARAMS_REACHED_GENESIS" if mode == "HISTORICAL_BACKFILL" else "NO_NEXT_PAGE_PARAMS"
            break

        time.sleep(REQUEST_DELAY_SECONDS)

    if stop_reason is None:
        stop_reason = "MAX_PAGES_REACHED"

    enriched_count = 0
    for address in list(enrichment_queue)[:enrich_limit]:
        if enrich_wallet(address, wallet_metrics):
            wallet_deltas[address] = deepcopy(wallet_metrics[address])
            enriched_count += 1
        enrichment_queue.discard(address)
        time.sleep(REQUEST_DELAY_SECONDS)

    if mode == "HISTORICAL_BACKFILL":
        historical_backfill_complete = next_cursor is None and stop_reason == "NO_NEXT_PAGE_PARAMS_REACHED_GENESIS"
        checkpoint_after = {
            "sync_phase": "BACKFILL_COMPLETE" if historical_backfill_complete else "HISTORICAL_BACKFILL_IN_PROGRESS",
            "historical_backfill_complete": historical_backfill_complete,
            "backfill_status": "COMPLETE" if historical_backfill_complete else "IN_PROGRESS",
            "backfill_direction": "latest_to_genesis",
            "backfill_stop_reason": stop_reason,
            "last_synced_block": last_block if last_block is not None else checkpoint_before.get("last_synced_block"),
            "last_transaction_cursor": None if historical_backfill_complete else next_cursor,
            "last_transaction_hash": last_tx_hash or checkpoint_before.get("last_transaction_hash"),
            "latest_seen_transaction_hash": checkpoint_before.get("latest_seen_transaction_hash") or first_tx_hash,
            "incremental_anchor_hash": checkpoint_before.get("incremental_anchor_hash") or first_tx_hash,
            "last_sync_at": now_utc(),
        }
    else:
        checkpoint_after = {
            "sync_phase": "INCREMENTAL_SYNC",
            "historical_backfill_complete": True,
            "backfill_status": "COMPLETE",
            "backfill_direction": "latest_to_genesis",
            "backfill_stop_reason": checkpoint_before.get("backfill_stop_reason"),
            "last_synced_block": last_block if last_block is not None else checkpoint_before.get("last_synced_block"),
            "last_transaction_cursor": None,
            "last_transaction_hash": last_tx_hash or checkpoint_before.get("last_transaction_hash"),
            "latest_seen_transaction_hash": first_tx_hash or checkpoint_before.get("latest_seen_transaction_hash"),
            "incremental_anchor_hash": first_tx_hash or checkpoint_before.get("incremental_anchor_hash"),
            "last_sync_at": now_utc(),
            "incremental_stop_reason": stop_reason,
        }

    latest["status"] = "SYNCED"
    latest["updated_at"] = now_utc()
    latest["checkpoint"] = checkpoint_after
    latest["enrichment_queue"] = sorted(enrichment_queue)

    latest["counters"] = {
        "total_processed_transactions": int(latest.get("counters", {}).get("total_processed_transactions", 0)) + processed_transactions,
        "total_indexed_wallets": len(wallet_metrics),
        "last_sync_processed_transactions": processed_transactions,
        "last_sync_wallets_changed": len(wallet_deltas),
        "native_balance_snapshots": sum(1 for m in wallet_metrics.values() if m.get("native_balance_wei") is not None),
        "asset_holding_snapshots": sum(1 for m in wallet_metrics.values() if m.get("asset_snapshot_time")),
        "enriched_wallets_this_sync": enriched_count,
        "enrichment_queue_remaining": len(enrichment_queue),
    }

    if checkpoint_before.get("sync_phase") == "NOT_STARTED":
        snapshot_name = "backfill-from-latest-to-genesis.json"
        snapshot_type = "historical_backfill_from_latest_to_genesis"
    elif mode == "HISTORICAL_BACKFILL":
        snapshot_name = f"backfill-{snapshot_timestamp()}-changed.json"
        snapshot_type = "historical_backfill_changed"
    else:
        snapshot_name = f"incremental-{snapshot_timestamp()}-changed.json"
        snapshot_type = "incremental_changed"

    snapshot_rel = f"data/snapshots/{snapshot_name}"

    snapshot = {
        "project": latest["project"],
        "engine": latest["engine"],
        "network": latest["network"],
        "chain_id": latest["chain_id"],
        "schema_version": latest.get("schema_version", "2.0.0"),
        "data_model": latest.get("data_model", "VARIABLE_AWARE_NORMALIZED_WALLET_METRICS"),
        "raw_transaction_dump": False,
        "snapshot_type": snapshot_type,
        "status": "SYNCED",
        "created_at": now_utc(),
        "sync_mode": mode,
        "stop_reason": stop_reason,
        "checkpoint_before": checkpoint_before,
        "checkpoint_after": checkpoint_after,
        "processed_transactions_this_sync": processed_transactions,
        "wallets_changed_this_sync": len(wallet_deltas),
        "enriched_wallets_this_sync": enriched_count,
        "enrichment_queue_remaining": len(enrichment_queue),
        "wallet_deltas": wallet_deltas,
        "minimal_audit": {
            "first_transaction_hash": first_tx_hash,
            "last_transaction_hash": last_tx_hash,
            "first_block": first_block,
            "last_block": last_block,
        },
    }

    latest["latest_snapshot"] = snapshot_rel

    write_json(snapshots_dir() / snapshot_name, snapshot)
    write_json(latest_path(), latest)

    return {
        "mode": mode,
        "processed_transactions": processed_transactions,
        "wallets_changed": len(wallet_deltas),
        "enriched_wallets": enriched_count,
        "enrichment_queue_remaining": len(enrichment_queue),
        "latest_snapshot": snapshot_rel,
        "stop_reason": stop_reason,
        "historical_backfill_complete": checkpoint_after.get("historical_backfill_complete"),
        "checkpoint_after": checkpoint_after,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync WIL v3 variable-aware rank data engine.")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum transaction pages to process in this run.")
    parser.add_argument("--enrich-limit", type=int, default=100, help="Maximum wallets to enrich with address/token data in this run.")
    args = parser.parse_args()

    if args.max_pages <= 0:
        raise SystemExit("--max-pages must be greater than 0")

    if args.enrich_limit < 0:
        raise SystemExit("--enrich-limit must be >= 0")

    result = run_sync(args.max_pages, args.enrich_limit)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
