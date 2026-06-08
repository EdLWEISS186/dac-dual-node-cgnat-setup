#!/usr/bin/env python3
"""
WIL v3 Local RPC Rank Data Worker

Purpose:
- Replace GitHub Actions as the main backfill/incremental data engine.
- Read DAC blocks directly from local RPC.
- Use primary + fallback local nodes.
- Preserve the public output model used by WIL v3.

Initial mode:
- Backfill from the current checkpoint toward genesis.
- Store normalized wallet metrics only.
- Do not store raw transaction dumps.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Optional, Set


CHAIN_ID = 21894
NETWORK = "DAC Testnet"
PROJECT = "Wallet Intelligence Layer v3.0.0"

DEFAULT_PRIMARY_RPC = "http://127.0.0.1:8546"
DEFAULT_FALLBACK_RPC = "http://192.168.100.7:8545"

TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def snapshot_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace(":", "-").replace(".", "-")


def root_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def engine_dir() -> Path:
    return Path(__file__).resolve().parents[1]


def latest_path() -> Path:
    return engine_dir() / "data" / "latest.json"


def snapshots_dir() -> Path:
    return engine_dir() / "data" / "snapshots"


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def rpc_call(rpc_urls: Iterable[str], method: str, params: list[Any], timeout: int = 30) -> Any:
    body = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1,
    }).encode("utf-8")

    last_error: Optional[Exception] = None

    for url in rpc_urls:
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )

            with urllib.request.urlopen(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))

            if "error" in payload:
                raise RuntimeError(f"{method} RPC error from {url}: {payload['error']}")

            return payload.get("result")

        except Exception as error:
            last_error = error
            continue

    raise RuntimeError(f"All RPC endpoints failed for {method}: {last_error}")


def hex_to_int(value: Any) -> int:
    if value is None:
        return 0

    if isinstance(value, int):
        return value

    raw = str(value)

    if raw.startswith("0x"):
        return int(raw, 16)

    return int(raw)


def int_to_hex(value: int) -> str:
    return hex(int(value))


def normalize_address(address: Any) -> Optional[str]:
    if not address:
        return None

    raw = str(address).lower()

    if not raw.startswith("0x") or len(raw) != 42:
        return None

    return raw


def empty_latest() -> Dict[str, Any]:
    return {
        "project": PROJECT,
        "engine": "rank-data-engine",
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "data_model": "NORMALIZED_WALLET_METRIC_DELTAS",
        "raw_transaction_dump": False,
        "status": "SYNCED",
        "updated_at": now_utc(),
        "sources": {},
        "checkpoint": {},
        "counters": {},
        "wallet_metrics": {},
    }


def load_latest() -> Dict[str, Any]:
    if latest_path().exists():
        return read_json(latest_path())

    return empty_latest()


def ensure_wallet(wallet_metrics: Dict[str, Any], address: str, block_number: int, tx_hash: str, timestamp: str) -> Dict[str, Any]:
    wallet = wallet_metrics.setdefault(address, {
        "address": address,
        "first_seen_block": block_number,
        "last_seen_block": block_number,
        "first_seen_tx": tx_hash,
        "last_seen_tx": tx_hash,
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
        "contract_interaction_count": 0,
        "unique_counterparty_count": 0,
        "repeated_counterparty_count": 0,
        "counterparty_addresses": [],
        "asset_contract_addresses": [],
        "nft_collection_contract_addresses": [],
        "token_holdings_count": 0,
        "nft_holdings_count": 0,
        "has_tokens": False,
        "has_token_transfers": False,
        "is_contract": False,
        "updated_at": timestamp,
    })

    first_seen = wallet.get("first_seen_block")
    last_seen = wallet.get("last_seen_block")

    if first_seen is None or block_number < int(first_seen):
        wallet["first_seen_block"] = block_number
        wallet["first_seen_tx"] = tx_hash

    if last_seen is None or block_number > int(last_seen):
        wallet["last_seen_block"] = block_number
        wallet["last_seen_tx"] = tx_hash

    wallet["updated_at"] = timestamp

    return wallet


def add_counterparty(wallet: Dict[str, Any], counterparty: Optional[str]) -> None:
    if not counterparty:
        return

    existing = set(wallet.get("counterparty_addresses") or [])
    before = len(existing)
    existing.add(counterparty)

    wallet["counterparty_addresses"] = sorted(existing)
    wallet["unique_counterparty_count"] = len(existing)

    if len(existing) == before:
        wallet["repeated_counterparty_count"] = int(wallet.get("repeated_counterparty_count") or 0) + 1


def add_asset_contract(wallet: Dict[str, Any], contract: Optional[str]) -> None:
    contract = normalize_address(contract)

    if not contract:
        return

    existing = set(wallet.get("asset_contract_addresses") or [])
    existing.add(contract)

    wallet["asset_contract_addresses"] = sorted(existing)
    wallet["has_token_transfers"] = True


def add_int_string(value: Any, delta: int) -> str:
    return str(int(str(value or "0")) + int(delta))


def process_transaction(
    wallet_metrics: Dict[str, Any],
    tx: Dict[str, Any],
    receipt: Dict[str, Any],
    block_number: int,
    timestamp: str,
) -> Set[str]:
    changed: Set[str] = set()

    tx_hash = tx.get("hash") or ""
    from_addr = normalize_address(tx.get("from"))
    to_addr = normalize_address(tx.get("to"))

    value_wei = hex_to_int(tx.get("value"))
    gas_used = hex_to_int(receipt.get("gasUsed"))
    status = receipt.get("status")
    input_data = tx.get("input") or "0x"

    if from_addr:
        sender = ensure_wallet(wallet_metrics, from_addr, block_number, tx_hash, timestamp)

        sender["tx_count"] = int(sender.get("tx_count") or 0) + 1
        sender["outgoing_tx_count"] = int(sender.get("outgoing_tx_count") or 0) + 1
        sender["gas_used_total"] = int(sender.get("gas_used_total") or 0) + gas_used
        sender["gas_used_outgoing"] = int(sender.get("gas_used_outgoing") or 0) + gas_used
        sender["native_volume_wei"] = add_int_string(sender.get("native_volume_wei"), value_wei)
        sender["outgoing_native_volume_wei"] = add_int_string(sender.get("outgoing_native_volume_wei"), value_wei)

        if status == "0x1":
            sender["successful_tx_count"] = int(sender.get("successful_tx_count") or 0) + 1
        elif status == "0x0":
            sender["failed_tx_count"] = int(sender.get("failed_tx_count") or 0) + 1

        if to_addr:
            add_counterparty(sender, to_addr)

        if input_data and input_data != "0x":
            sender["contract_interaction_count"] = int(sender.get("contract_interaction_count") or 0) + 1

        changed.add(from_addr)

    if to_addr:
        receiver = ensure_wallet(wallet_metrics, to_addr, block_number, tx_hash, timestamp)

        receiver["incoming_tx_count"] = int(receiver.get("incoming_tx_count") or 0) + 1
        receiver["native_volume_wei"] = add_int_string(receiver.get("native_volume_wei"), value_wei)
        receiver["incoming_native_volume_wei"] = add_int_string(receiver.get("incoming_native_volume_wei"), value_wei)

        if from_addr:
            add_counterparty(receiver, from_addr)

        if input_data and input_data != "0x":
            receiver["is_contract"] = True

        changed.add(to_addr)

    for log in receipt.get("logs") or []:
        topics = log.get("topics") or []
        contract = normalize_address(log.get("address"))

        if topics and str(topics[0]).lower() == TRANSFER_TOPIC:
            for address in [from_addr, to_addr]:
                if address:
                    wallet = ensure_wallet(wallet_metrics, address, block_number, tx_hash, timestamp)
                    add_asset_contract(wallet, contract)
                    changed.add(address)

    return changed


def enrich_balances(wallet_metrics: Dict[str, Any], changed_wallets: Iterable[str], rpc_urls: list[str], limit: int) -> int:
    count = 0

    for address in sorted(set(changed_wallets)):
        if count >= limit:
            break

        try:
            balance_hex = rpc_call(rpc_urls, "eth_getBalance", [address, "latest"], timeout=20)
            wallet = wallet_metrics.get(address)

            if not wallet:
                continue

            wallet["native_balance_wei"] = str(hex_to_int(balance_hex))
            wallet["balance_snapshot_time"] = now_utc()
            count += 1

        except Exception:
            continue

    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--primary-rpc", default=DEFAULT_PRIMARY_RPC)
    parser.add_argument("--fallback-rpc", default=DEFAULT_FALLBACK_RPC)
    parser.add_argument("--max-blocks", type=int, default=20)
    parser.add_argument("--balance-enrich-limit", type=int, default=100)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-snapshot-archive", action="store_true")
    args = parser.parse_args()

    rpc_urls = [args.primary_rpc, args.fallback_rpc]

    latest = load_latest()
    working = deepcopy(latest)

    checkpoint = working.setdefault("checkpoint", {})
    wallet_metrics = working.setdefault("wallet_metrics", {})

    chain_id = hex_to_int(rpc_call(rpc_urls, "eth_chainId", []))

    if chain_id != CHAIN_ID:
        raise SystemExit(f"Wrong chain_id: {chain_id}. Expected {CHAIN_ID}.")

    latest_block = hex_to_int(rpc_call(rpc_urls, "eth_blockNumber", []))

    backfill_next_block = checkpoint.get("local_rpc_backfill_next_block")

    if backfill_next_block is None:
        backfill_next_block = checkpoint.get("last_synced_block")

    if backfill_next_block is None:
        backfill_next_block = latest_block

    start_block = int(backfill_next_block)
    end_block = max(start_block - args.max_blocks + 1, 0)

    processed_blocks = 0
    processed_transactions = 0
    changed_wallets: Set[str] = set()
    last_tx_hash = None
    last_synced_block = start_block

    run_started_at = now_utc()

    for block_number in range(start_block, end_block - 1, -1):
        block = rpc_call(rpc_urls, "eth_getBlockByNumber", [int_to_hex(block_number), True], timeout=45)

        if not block:
            continue

        block_timestamp = now_utc()
        txs = block.get("transactions") or []

        for tx in txs:
            tx_hash = tx.get("hash")

            if not tx_hash:
                continue

            receipt = rpc_call(rpc_urls, "eth_getTransactionReceipt", [tx_hash], timeout=45) or {}

            changed = process_transaction(
                wallet_metrics=wallet_metrics,
                tx=tx,
                receipt=receipt,
                block_number=block_number,
                timestamp=block_timestamp,
            )

            changed_wallets.update(changed)
            processed_transactions += 1
            last_tx_hash = tx_hash

        processed_blocks += 1
        last_synced_block = block_number

    enriched_balances = enrich_balances(
        wallet_metrics=wallet_metrics,
        changed_wallets=changed_wallets,
        rpc_urls=rpc_urls,
        limit=args.balance_enrich_limit,
    )

    counters = working.setdefault("counters", {})
    previous_processed = int(counters.get("total_processed_transactions") or 0)
    previous_balance_snapshots = int(counters.get("native_balance_snapshots") or 0)

    counters["last_sync_processed_blocks"] = processed_blocks
    counters["last_sync_processed_transactions"] = processed_transactions
    counters["last_sync_wallets_changed"] = len(changed_wallets)
    counters["total_processed_transactions"] = previous_processed + processed_transactions
    counters["total_indexed_wallets"] = len(wallet_metrics)
    counters["native_balance_snapshots"] = previous_balance_snapshots + enriched_balances
    counters["asset_holding_snapshots"] = int(counters.get("asset_holding_snapshots") or 0)

    checkpoint.update({
        "sync_phase": "HISTORICAL_BACKFILL_IN_PROGRESS",
        "backfill_status": "IN_PROGRESS",
        "historical_backfill_complete": False,
        "backfill_direction": "latest_to_genesis",
        "backfill_stop_reason": "MAX_BLOCKS_REACHED",
        "last_sync_at": run_started_at,
        "last_synced_block": last_synced_block,
        "local_rpc_backfill_next_block": max(last_synced_block - 1, 0),
        "local_rpc_latest_block_at_sync": latest_block,
        "last_transaction_hash": last_tx_hash,
        "primary_rpc": args.primary_rpc,
        "fallback_rpc": args.fallback_rpc,
    })

    working.update({
        "project": PROJECT,
        "engine": "rank-data-engine",
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "data_model": "NORMALIZED_WALLET_METRIC_DELTAS",
        "raw_transaction_dump": False,
        "status": "SYNCED",
        "updated_at": run_started_at,
        "sources": {
            "primary_rpc": args.primary_rpc,
            "fallback_rpc": args.fallback_rpc,
            "mode": "LOCAL_RPC_PRIMARY_WITH_FALLBACK",
        },
    })

    snapshot_name = f"backfill-{snapshot_timestamp()}-changed.json"
    snapshot_archive_written = not args.no_snapshot_archive

    if snapshot_archive_written:
        working["latest_snapshot"] = f"data/snapshots/{snapshot_name}"
    else:
        working["latest_snapshot"] = "data/latest.json"
        working["latest_snapshot_name"] = snapshot_name

    working["snapshot_archive_written"] = snapshot_archive_written

    result = {
        "mode": "LOCAL_RPC_HISTORICAL_BACKFILL",
        "dry_run": args.dry_run,
        "primary_rpc": args.primary_rpc,
        "fallback_rpc": args.fallback_rpc,
        "start_block": start_block,
        "end_block": end_block,
        "processed_blocks": processed_blocks,
        "processed_transactions": processed_transactions,
        "wallets_changed": len(changed_wallets),
        "enriched_balances": enriched_balances,
        "total_indexed_wallets": len(wallet_metrics),
        "total_processed_transactions_after": counters["total_processed_transactions"],
        "local_rpc_backfill_next_block": checkpoint["local_rpc_backfill_next_block"],
        "latest_snapshot": working["latest_snapshot"],
        "snapshot_archive_written": snapshot_archive_written,
    }

    if not args.dry_run:
        write_json(latest_path(), working)
        if snapshot_archive_written:
            write_json(snapshots_dir() / snapshot_name, working)

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
