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

from sqlite_rank_state import SQLiteRankState


CHAIN_ID = 21894
NETWORK = "DAC Testnet"
PROJECT = "Wallet Intelligence Layer v3.3.0"

DEFAULT_PRIMARY_RPC = "http://127.0.0.1:8546"
DEFAULT_FALLBACK_RPC = "http://192.168.100.7:8545"

TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

OFFICIAL_INCEPTION_NFT_CONTRACT = (
    "0xb36ab4c2bd6acfc36e9d6c53f39f4301901bd647"
)

DACC_STAKING_CONTRACT = (
    "0x3691a78be270db1f3b1a86177a8f23f89a8cef24"
)

STAKE_FUNCTION_SELECTOR = "0x3a4b66f1"
UNSTAKE_FUNCTION_SELECTOR = "0x2e17de78"


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


def public_run_status_path() -> Path:
    return engine_dir() / "data" / "public-run-status.json"


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


def normalize_input(value: Any) -> str:
    raw = str(value or "").strip().lower()

    if not raw:
        return "0x"

    return raw if raw.startswith("0x") else f"0x{raw}"


def decode_first_uint256_from_input(
    input_data: Any,
) -> Optional[int]:
    normalized = normalize_input(input_data)
    raw = normalized.removeprefix("0x")

    if len(raw) < 8 + 64:
        return None

    first_argument = raw[8:8 + 64]

    try:
        return int(first_argument, 16)
    except ValueError:
        return None


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

    existing = wallet.get("counterparty_addresses") or []

    if counterparty in existing:
        wallet["repeated_counterparty_count"] = (
            int(wallet.get("repeated_counterparty_count") or 0) + 1
        )
        wallet["unique_counterparty_count"] = len(existing)
        return

    existing = list(existing)
    existing.append(counterparty)
    existing.sort()

    wallet["counterparty_addresses"] = existing
    wallet["unique_counterparty_count"] = len(existing)


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


def decode_address_topic(value: Any) -> Optional[str]:
    raw = str(value or "").lower()

    if raw.startswith("0x"):
        raw = raw[2:]

    if len(raw) != 64:
        return None

    return normalize_address(f"0x{raw[-40:]}")


def process_official_inception_nft_receipt(
    official_inception_nft_tokens: Any,
    tx: Dict[str, Any],
    receipt: Dict[str, Any],
    block_number: int,
    timestamp: str,
) -> tuple[Set[str], int]:
    """Track latest owners from official ERC-721 Transfer logs."""

    changed_token_ids: Set[str] = set()
    matched_events = 0

    if official_inception_nft_tokens is None:
        return changed_token_ids, matched_events

    try:
        succeeded = (
            hex_to_int(receipt.get("status")) == 1
        )
    except Exception:
        succeeded = False

    if not succeeded:
        return changed_token_ids, matched_events

    tx_hash = str(
        tx.get("hash")
        or receipt.get("transactionHash")
        or ""
    )

    transaction_index = hex_to_int(
        receipt.get("transactionIndex")
        if receipt.get("transactionIndex") is not None
        else tx.get("transactionIndex")
    )

    for log in receipt.get("logs") or []:
        contract = normalize_address(log.get("address"))
        topics = log.get("topics") or []

        if contract != OFFICIAL_INCEPTION_NFT_CONTRACT:
            continue

        if len(topics) < 4:
            continue

        if str(topics[0]).lower() != TRANSFER_TOPIC:
            continue

        from_address = decode_address_topic(topics[1])
        to_address = decode_address_topic(topics[2])

        try:
            token_id = str(hex_to_int(topics[3]))
            log_index = hex_to_int(log.get("logIndex"))
        except (TypeError, ValueError):
            continue

        matched_events += 1

        if official_inception_nft_tokens.observe_transfer(
            token_id=token_id,
            from_address=from_address,
            to_address=to_address,
            block_number=block_number,
            transaction_index=transaction_index,
            log_index=log_index,
            tx_hash=tx_hash,
            timestamp=timestamp,
        ):
            changed_token_ids.add(token_id)

    return changed_token_ids, matched_events


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


def process_staking_transaction(
    staking_metrics: Any,
    tx: Dict[str, Any],
    receipt: Dict[str, Any],
    block_number: int,
    timestamp: str,
) -> Optional[str]:
    """Accumulate flow-derived Estimated Current Stake."""

    if staking_metrics is None:
        return None

    try:
        succeeded = hex_to_int(receipt.get("status")) == 1
    except Exception:
        succeeded = False

    if not succeeded:
        return None

    from_address = normalize_address(tx.get("from"))
    to_address = normalize_address(tx.get("to"))

    if (
        not from_address
        or to_address != DACC_STAKING_CONTRACT
    ):
        return None

    input_data = normalize_input(
        tx.get("input") or tx.get("data") or "0x"
    )

    tx_hash = str(
        tx.get("hash")
        or tx.get("transactionHash")
        or ""
    )

    value_wei = hex_to_int(tx.get("value"))

    event_type: Optional[str] = None
    event_amount = 0

    if (
        input_data.startswith(STAKE_FUNCTION_SELECTOR)
        and value_wei > 0
    ):
        event_type = "STAKE"
        event_amount = value_wei

    elif input_data.startswith(
        UNSTAKE_FUNCTION_SELECTOR
    ):
        decoded_amount = (
            decode_first_uint256_from_input(input_data)
        )

        if decoded_amount is None:
            return None

        event_type = "UNSTAKE"
        event_amount = decoded_amount

    else:
        return None

    record = staking_metrics.setdefault(from_address)

    if event_type == "STAKE":
        record["stake_in_wei"] = add_int_string(
            record.get("stake_in_wei"),
            event_amount,
        )

        record["stake_tx_count"] = (
            int(record.get("stake_tx_count") or 0)
            + 1
        )

    else:
        record["unstake_out_wei"] = add_int_string(
            record.get("unstake_out_wei"),
            event_amount,
        )

        record["unstake_tx_count"] = (
            int(record.get("unstake_tx_count") or 0)
            + 1
        )

    stake_in_wei = int(
        str(record.get("stake_in_wei") or "0")
    )

    unstake_out_wei = int(
        str(record.get("unstake_out_wei") or "0")
    )

    record["estimated_current_stake_wei"] = str(
        max(stake_in_wei - unstake_out_wei, 0)
    )

    record["flow_tx_count"] = (
        int(record.get("stake_tx_count") or 0)
        + int(record.get("unstake_tx_count") or 0)
    )

    record["source"] = (
        "DAC_STAKE_UNSTAKE_TRANSACTION_FLOW"
    )

    record["confidence"] = "MEDIUM_HIGH"

    previous_last_block = record.get(
        "last_event_block"
    )

    if (
        previous_last_block is None
        or block_number > int(previous_last_block)
    ):
        record["last_event_block"] = block_number
        record["last_event_tx_hash"] = tx_hash

    record["updated_at"] = timestamp

    return from_address


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
    parser.add_argument(
        "--sqlite-state",
        help=(
            "Use a SQLite rank-state database instead of the legacy "
            "monolithic JSON state."
        ),
    )
    args = parser.parse_args()

    if args.sqlite_state and not args.no_snapshot_archive:
        raise SystemExit(
            "--sqlite-state currently requires --no-snapshot-archive"
        )

    rpc_urls = [args.primary_rpc, args.fallback_rpc]

    sqlite_state = None
    staking_metrics = None
    official_inception_nft_tokens = None

    if args.sqlite_state:
        sqlite_state = SQLiteRankState(
            Path(args.sqlite_state).expanduser().resolve()
        )

        checkpoint = sqlite_state.checkpoint()
        counters = sqlite_state.counters()
        working = sqlite_state.state_meta()

        working["checkpoint"] = checkpoint
        working["counters"] = counters

        wallet_metrics = sqlite_state.wallet_metrics
        staking_metrics = sqlite_state.staking_metrics
        official_inception_nft_tokens = (
            sqlite_state.official_inception_nft_tokens
        )
        state_backend = "SQLITE"

        try:
            relative_state_path = sqlite_state.database.relative_to(
                Path.home()
            )
            heavy_state_local_path = (
                f"~/{relative_state_path.as_posix()}"
            )
        except ValueError:
            heavy_state_local_path = str(sqlite_state.database)
    else:
        latest = load_latest()
        working = deepcopy(latest)

        checkpoint = working.setdefault("checkpoint", {})
        counters = working.setdefault("counters", {})
        wallet_metrics = working.setdefault("wallet_metrics", {})

        state_backend = "LEGACY_JSON"
        heavy_state_local_path = str(latest_path())

    chain_id = hex_to_int(rpc_call(rpc_urls, "eth_chainId", []))

    if chain_id != CHAIN_ID:
        raise SystemExit(f"Wrong chain_id: {chain_id}. Expected {CHAIN_ID}.")

    latest_block = hex_to_int(rpc_call(rpc_urls, "eth_blockNumber", []))
    run_started_at = now_utc()

    sync_phase = checkpoint.get("sync_phase") or "HISTORICAL_BACKFILL_IN_PROGRESS"
    historical_complete = checkpoint.get("historical_backfill_complete") is True

    # Anchor = highest block that belongs to the historical backfill boundary.
    # It must remain stable so that post-backfill catch-up can fill the gap:
    # anchor + 1 -> latest chain head.
    anchor_block = checkpoint.get("historical_backfill_anchor_block")

    if anchor_block is None:
        anchor_block = checkpoint.get("last_synced_block")

    if anchor_block is None:
        anchor_block = latest_block

    anchor_block = int(anchor_block)
    checkpoint["historical_backfill_anchor_block"] = anchor_block
    checkpoint.setdefault("historical_backfill_anchor_source", "INITIAL_LOCAL_RPC_BACKFILL_ANCHOR")
    checkpoint.setdefault("post_backfill_catch_up_from_block", anchor_block + 1)

    processed_blocks = 0
    processed_transactions = 0
    processed_staking_events = 0
    processed_official_inception_nft_events = 0

    changed_wallets: Set[str] = set()
    changed_staking_wallets: Set[str] = set()
    changed_official_inception_token_ids: Set[str] = set()

    last_tx_hash = None
    last_synced_block = checkpoint.get("last_synced_block")
    mode = "UNKNOWN"
    direction = "none"
    start_block = None
    end_block = None
    stop_reason = "NO_BLOCKS_TO_PROCESS"

    def process_block(block_number: int) -> None:
        nonlocal processed_blocks
        nonlocal processed_transactions
        nonlocal processed_staking_events
        nonlocal processed_official_inception_nft_events
        nonlocal last_tx_hash
        nonlocal last_synced_block

        block = rpc_call(rpc_urls, "eth_getBlockByNumber", [int_to_hex(block_number), True], timeout=45)

        if not block:
            return

        block_timestamp = now_utc()
        txs = block.get("transactions") or []

        for tx in txs:
            tx_hash = tx.get("hash")

            if not tx_hash:
                continue

            receipt = rpc_call(
                rpc_urls,
                "eth_getTransactionReceipt",
                [tx_hash],
                timeout=45,
            ) or {}

            staking_address = process_staking_transaction(
                staking_metrics=staking_metrics,
                tx=tx,
                receipt=receipt,
                block_number=block_number,
                timestamp=block_timestamp,
            )

            if staking_address:
                changed_staking_wallets.add(
                    staking_address
                )
                processed_staking_events += 1

            (
                changed_token_ids,
                official_inception_event_count,
            ) = process_official_inception_nft_receipt(
                official_inception_nft_tokens=(
                    official_inception_nft_tokens
                ),
                tx=tx,
                receipt=receipt,
                block_number=block_number,
                timestamp=block_timestamp,
            )

            processed_official_inception_nft_events += (
                official_inception_event_count
            )

            if changed_token_ids:
                changed_official_inception_token_ids.update(
                    changed_token_ids
                )

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

    if not historical_complete and sync_phase != "POST_BACKFILL_CATCH_UP":
        mode = "LOCAL_RPC_HISTORICAL_BACKFILL"
        direction = "latest_to_genesis"

        backfill_next_block = checkpoint.get("local_rpc_backfill_next_block")

        if backfill_next_block is None:
            backfill_next_block = checkpoint.get("last_synced_block")

        if backfill_next_block is None:
            backfill_next_block = anchor_block

        start_block = int(backfill_next_block)

        if start_block <= 0:
            end_block = 0
            checkpoint.update({
                "sync_phase": "POST_BACKFILL_CATCH_UP",
                "backfill_status": "COMPLETE",
                "backfill_stop_reason": "GENESIS_REACHED",
                "historical_backfill_complete": True,
                "post_backfill_catch_up_from_block": anchor_block + 1,
                "catch_up_next_block": anchor_block + 1,
            })
            stop_reason = "GENESIS_ALREADY_REACHED"
        else:
            end_block = max(start_block - args.max_blocks + 1, 0)

            for block_number in range(start_block, end_block - 1, -1):
                process_block(block_number)

            next_backfill_block = max(int(last_synced_block or end_block) - 1, 0)

            if end_block == 0 or next_backfill_block == 0:
                checkpoint.update({
                    "sync_phase": "POST_BACKFILL_CATCH_UP",
                    "backfill_status": "COMPLETE",
                    "backfill_stop_reason": "GENESIS_REACHED",
                    "historical_backfill_complete": True,
                    "local_rpc_backfill_next_block": 0,
                    "post_backfill_catch_up_from_block": anchor_block + 1,
                    "catch_up_next_block": anchor_block + 1,
                })
                stop_reason = "GENESIS_REACHED"
            else:
                checkpoint.update({
                    "sync_phase": "HISTORICAL_BACKFILL_IN_PROGRESS",
                    "backfill_status": "IN_PROGRESS",
                    "backfill_stop_reason": "MAX_BLOCKS_REACHED",
                    "historical_backfill_complete": False,
                    "local_rpc_backfill_next_block": next_backfill_block,
                })
                stop_reason = "MAX_BLOCKS_REACHED"

    elif sync_phase == "POST_BACKFILL_CATCH_UP":
        mode = "LOCAL_RPC_POST_BACKFILL_CATCH_UP"
        direction = "anchor_to_latest"

        catch_up_next_block = checkpoint.get("catch_up_next_block")
        if catch_up_next_block is None:
            catch_up_next_block = checkpoint.get("post_backfill_catch_up_from_block")
        if catch_up_next_block is None:
            catch_up_next_block = anchor_block + 1

        start_block = int(catch_up_next_block)

        if start_block > latest_block:
            end_block = latest_block
            checkpoint.update({
                "sync_phase": "INCREMENTAL",
                "backfill_status": "COMPLETE",
                "catch_up_status": "CAUGHT_UP",
                "historical_backfill_complete": True,
                "incremental_next_block": latest_block + 1,
                "incremental_last_synced_block": latest_block,
            })
            stop_reason = "ALREADY_CAUGHT_UP"
        else:
            end_block = min(start_block + args.max_blocks - 1, latest_block)

            for block_number in range(start_block, end_block + 1):
                process_block(block_number)

            next_catch_up_block = int(end_block) + 1

            if next_catch_up_block > latest_block:
                checkpoint.update({
                    "sync_phase": "INCREMENTAL",
                    "backfill_status": "COMPLETE",
                    "catch_up_status": "CAUGHT_UP",
                    "historical_backfill_complete": True,
                    "catch_up_next_block": next_catch_up_block,
                    "incremental_next_block": latest_block + 1,
                    "incremental_last_synced_block": latest_block,
                })
                stop_reason = "CAUGHT_UP_TO_LATEST"
            else:
                checkpoint.update({
                    "sync_phase": "POST_BACKFILL_CATCH_UP",
                    "backfill_status": "COMPLETE",
                    "catch_up_status": "IN_PROGRESS",
                    "historical_backfill_complete": True,
                    "catch_up_next_block": next_catch_up_block,
                })
                stop_reason = "MAX_BLOCKS_REACHED"

    else:
        mode = "LOCAL_RPC_INCREMENTAL"
        direction = "new_blocks_forward"

        incremental_next_block = checkpoint.get("incremental_next_block")
        if incremental_next_block is None:
            incremental_next_block = (checkpoint.get("incremental_last_synced_block") or latest_block) + 1

        start_block = int(incremental_next_block)

        if start_block > latest_block:
            end_block = latest_block
            checkpoint.update({
                "sync_phase": "INCREMENTAL",
                "backfill_status": "COMPLETE",
                "historical_backfill_complete": True,
                "incremental_next_block": start_block,
                "incremental_last_synced_block": latest_block,
            })
            stop_reason = "NO_NEW_BLOCKS"
        else:
            end_block = min(start_block + args.max_blocks - 1, latest_block)

            for block_number in range(start_block, end_block + 1):
                process_block(block_number)

            next_incremental_block = int(end_block) + 1

            checkpoint.update({
                "sync_phase": "INCREMENTAL",
                "backfill_status": "COMPLETE",
                "historical_backfill_complete": True,
                "incremental_next_block": next_incremental_block,
                "incremental_last_synced_block": end_block,
            })

            stop_reason = "CAUGHT_UP_TO_LATEST" if next_incremental_block > latest_block else "MAX_BLOCKS_REACHED"

    enriched_balances = enrich_balances(
        wallet_metrics=wallet_metrics,
        changed_wallets=changed_wallets,
        rpc_urls=rpc_urls,
        limit=args.balance_enrich_limit,
    )

    previous_processed = int(
        counters.get("total_processed_transactions") or 0
    )

    previous_staking_events = int(
        counters.get("total_staking_events") or 0
    )

    previous_balance_snapshots = int(
        counters.get("native_balance_snapshots") or 0
    )

    previous_official_inception_nft_events = int(
        counters.get(
            "total_official_inception_nft_events"
        )
        or 0
    )

    counters["last_sync_processed_blocks"] = processed_blocks
    counters["last_sync_processed_transactions"] = processed_transactions
    counters["last_sync_wallets_changed"] = len(changed_wallets)

    counters["last_sync_staking_events"] = (
        processed_staking_events
    )

    counters["last_sync_staking_wallets_changed"] = (
        len(changed_staking_wallets)
    )

    counters[
        "last_sync_official_inception_nft_events"
    ] = processed_official_inception_nft_events

    counters[
        "last_sync_official_inception_nft_tokens_changed"
    ] = len(changed_official_inception_token_ids)

    counters["total_processed_transactions"] = (
        previous_processed + processed_transactions
    )

    counters["total_staking_events"] = (
        previous_staking_events
        + processed_staking_events
    )

    counters["total_official_inception_nft_events"] = (
        previous_official_inception_nft_events
        + processed_official_inception_nft_events
    )

    counters["total_indexed_wallets"] = len(wallet_metrics)

    counters["native_balance_snapshots"] = (
        previous_balance_snapshots + enriched_balances
    )

    counters["asset_holding_snapshots"] = int(
        counters.get("asset_holding_snapshots") or 0
    )

    checkpoint.update({
        "last_sync_at": run_started_at,
        "last_synced_block": last_synced_block,
        "local_rpc_latest_block_at_sync": latest_block,
        "last_transaction_hash": last_tx_hash,
        "primary_rpc": args.primary_rpc,
        "fallback_rpc": args.fallback_rpc,
        "last_run_mode": mode,
        "last_run_direction": direction,
        "last_run_stop_reason": stop_reason,
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
            "staking_contract": DACC_STAKING_CONTRACT,
            "staking_metric": "ESTIMATED_CURRENT_STAKE",
            "staking_source": (
                "DAC_STAKE_UNSTAKE_TRANSACTION_FLOW"
            ),
            "stake_selector": STAKE_FUNCTION_SELECTOR,
            "unstake_selector": UNSTAKE_FUNCTION_SELECTOR,
            "official_inception_nft_contract": (
                OFFICIAL_INCEPTION_NFT_CONTRACT
            ),
            "official_inception_nft_source": (
                "ERC721_TRANSFER_EVENT_LATEST_OWNER"
            ),
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
        "mode": mode,
        "direction": direction,
        "dry_run": args.dry_run,
        "state_backend": state_backend,
        "primary_rpc": args.primary_rpc,
        "fallback_rpc": args.fallback_rpc,
        "start_block": start_block,
        "end_block": end_block,
        "latest_block": latest_block,
        "historical_backfill_anchor_block": checkpoint.get("historical_backfill_anchor_block"),
        "processed_blocks": processed_blocks,
        "processed_transactions": processed_transactions,
        "wallets_changed": len(changed_wallets),

        "processed_staking_events": (
            processed_staking_events
        ),

        "staking_wallets_changed": (
            len(changed_staking_wallets)
        ),

        "estimated_current_stake_enabled": (
            staking_metrics is not None
        ),

        "official_inception_nft_enabled": (
            official_inception_nft_tokens is not None
        ),

        "processed_official_inception_nft_events": (
            processed_official_inception_nft_events
        ),

        "official_inception_nft_tokens_changed": (
            len(changed_official_inception_token_ids)
        ),

        "enriched_balances": enriched_balances,
        "total_indexed_wallets": len(wallet_metrics),
        "total_processed_transactions_after": counters["total_processed_transactions"],
        "sync_phase_after": checkpoint.get("sync_phase"),
        "local_rpc_backfill_next_block": checkpoint.get("local_rpc_backfill_next_block"),
        "catch_up_next_block": checkpoint.get("catch_up_next_block"),
        "incremental_next_block": checkpoint.get("incremental_next_block"),
        "stop_reason": stop_reason,
        "latest_snapshot": working["latest_snapshot"],
        "snapshot_archive_written": snapshot_archive_written,
    }

    public_status = {
        "schema": "WIL_V3_PUBLIC_RUN_STATUS",
        "version": "v3.3.0",
        "project": PROJECT,
        "engine": "rank-data-engine",
        "network": NETWORK,
        "chain_id": CHAIN_ID,
        "updated_at": now_utc(),
        "externalized_state": True,
        "heavy_state_storage": (
            "LOCAL_SQLITE_STATE_WITH_OPTIONAL_GOOGLE_DRIVE_BACKUP"
            if sqlite_state is not None
            else "LOCAL_EXTERNAL_STATE_WITH_OPTIONAL_GOOGLE_DRIVE_BACKUP"
        ),
        "heavy_state_local_path": heavy_state_local_path,
        "state_backend": state_backend,
        "github_storage_role": "PUBLIC_MANIFEST_ONLY",
        "rank_lookup_enabled": False,
        "rank_shards_published": False,

        "estimated_current_stake_enabled": (
            staking_metrics is not None
        ),

        "estimated_current_stake": {
            "label": "Estimated Current Stake",
            "contract": DACC_STAKING_CONTRACT,
            "source": (
                "DAC_STAKE_UNSTAKE_TRANSACTION_FLOW"
            ),
            "stake_selector": STAKE_FUNCTION_SELECTOR,
            "unstake_selector": UNSTAKE_FUNCTION_SELECTOR,
            "direct_contract_read_role": "CROSS_CHECK",
        },

        "official_inception_nft_enabled": (
            official_inception_nft_tokens is not None
        ),

        "official_inception_nft": {
            "label": "Official Testnet Inception NFTs",
            "contract": OFFICIAL_INCEPTION_NFT_CONTRACT,
            "standard": "ERC-721",
            "source": (
                "ERC721_TRANSFER_EVENT_LATEST_OWNER"
            ),
        },

        "snapshot_archive_written": snapshot_archive_written,
        "latest_snapshot": "externalized-local-state",
        "sync_status": {
            "phase": checkpoint.get("sync_phase"),
            "historical_backfill_complete": checkpoint.get("historical_backfill_complete") is True,
            "catch_up_status": checkpoint.get("catch_up_status"),
            "historical_backfill_anchor_block": checkpoint.get("historical_backfill_anchor_block"),
            "last_synced_block": checkpoint.get("last_synced_block"),
            "local_rpc_backfill_next_block": checkpoint.get("local_rpc_backfill_next_block"),
            "catch_up_next_block": checkpoint.get("catch_up_next_block"),
            "incremental_next_block": checkpoint.get("incremental_next_block"),
            "local_rpc_latest_block_at_sync": checkpoint.get("local_rpc_latest_block_at_sync"),
            "last_sync_at": checkpoint.get("last_sync_at"),
        },
        "counters": {
            "total_indexed_wallets": counters.get(
                "total_indexed_wallets"
            ),
            "total_processed_transactions": counters.get(
                "total_processed_transactions"
            ),
            "native_balance_snapshots": counters.get(
                "native_balance_snapshots"
            ),
            "last_sync_processed_blocks": counters.get(
                "last_sync_processed_blocks"
            ),
            "last_sync_processed_transactions": counters.get(
                "last_sync_processed_transactions"
            ),
            "last_sync_wallets_changed": counters.get(
                "last_sync_wallets_changed"
            ),
            "total_staking_events": counters.get(
                "total_staking_events"
            ),
            "last_sync_staking_events": counters.get(
                "last_sync_staking_events"
            ),
            "last_sync_staking_wallets_changed": counters.get(
                "last_sync_staking_wallets_changed"
            ),
            "total_official_inception_nft_events": (
                counters.get(
                    "total_official_inception_nft_events"
                )
            ),
            "last_sync_official_inception_nft_events": (
                counters.get(
                    "last_sync_official_inception_nft_events"
                )
            ),
            "last_sync_official_inception_nft_tokens_changed": (
                counters.get(
                    "last_sync_official_inception_nft_tokens_changed"
                )
            ),
        },
        "last_run": result,
        "note": "v3.3.0 lightweight publish status. Heavy wallet metrics remain externalized and are not loaded again by the publish layer during backfill."
    }

    if not args.dry_run:
        if sqlite_state is not None:
            state_meta = {
                key: value
                for key, value in working.items()
                if key not in {
                    "checkpoint",
                    "counters",
                    "wallet_metrics",
                    "enrichment_queue",
                }
            }

            wallets_written = sqlite_state.commit_state(
                checkpoint=checkpoint,
                counters=counters,
                state_meta=state_meta,
            )

            result["wallet_rows_written"] = wallets_written

            result["staking_rows_written"] = (
                sqlite_state.last_staking_rows_written
            )

            result[
                "official_inception_nft_rows_written"
            ] = (
                sqlite_state
                .last_official_inception_nft_rows_written
            )

            public_status["last_run"] = result
        else:
            write_json(latest_path(), working)

        write_json(public_run_status_path(), public_status)

        if snapshot_archive_written:
            write_json(snapshots_dir() / snapshot_name, working)

    if sqlite_state is not None:
        sqlite_state.close()

    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
