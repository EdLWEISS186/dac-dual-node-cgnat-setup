#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Rank Data Engine

Purpose:
- Fetch blockchain transaction data from official DAC Explorer API.
- Store only normalized wallet metric deltas and accumulated wallet metrics.
- Do not store raw transaction dumps.
- Keep latest.json and timestamped snapshots updated for WIL v3 rank calculation scripts.

Data model:
- tx_count
- gas_used
- native_volume_wei
- first_seen_block
- last_seen_block
- checkpoint/cursor metadata
"""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


EXPLORER_API_V2 = "https://exptest.dachain.tech/api/v2"
TRANSACTIONS_ENDPOINT = f"{EXPLORER_API_V2}/transactions"
STATS_ENDPOINT = f"{EXPLORER_API_V2}/stats"
REQUEST_TIMEOUT_SECONDS = 30


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
            "User-Agent": "WIL-v3-rank-data-engine/1.0",
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


def add_delta(
    wallet_deltas: Dict[str, Dict[str, Any]],
    address: str,
    tx_count_delta: int,
    gas_used_delta: int,
    native_volume_delta_wei: int,
    block_number: int,
) -> None:
    if not address:
        return

    entry = wallet_deltas.setdefault(
        address,
        {
            "tx_count_delta": 0,
            "gas_used_delta": 0,
            "native_volume_delta_wei": "0",
            "first_seen_block": block_number,
            "last_seen_block": block_number,
        },
    )

    entry["tx_count_delta"] += tx_count_delta
    entry["gas_used_delta"] += gas_used_delta
    entry["native_volume_delta_wei"] = str(int(entry["native_volume_delta_wei"]) + native_volume_delta_wei)
    entry["first_seen_block"] = min(entry["first_seen_block"], block_number)
    entry["last_seen_block"] = max(entry["last_seen_block"], block_number)


def apply_deltas(latest: Dict[str, Any], wallet_deltas: Dict[str, Dict[str, Any]]) -> None:
    wallet_metrics = latest.setdefault("wallet_metrics", {})
    updated_at = now_utc()

    for address, delta in wallet_deltas.items():
        existing = wallet_metrics.setdefault(
            address,
            {
                "tx_count": 0,
                "gas_used": 0,
                "native_volume_wei": "0",
                "first_seen_block": delta["first_seen_block"],
                "last_seen_block": delta["last_seen_block"],
                "updated_at": updated_at,
            },
        )

        existing["tx_count"] = int(existing.get("tx_count", 0)) + int(delta.get("tx_count_delta", 0))
        existing["gas_used"] = int(existing.get("gas_used", 0)) + int(delta.get("gas_used_delta", 0))
        existing["native_volume_wei"] = str(
            int(existing.get("native_volume_wei", "0")) + int(delta.get("native_volume_delta_wei", "0"))
        )
        existing["first_seen_block"] = min(
            existing.get("first_seen_block") or delta["first_seen_block"],
            delta["first_seen_block"],
        )
        existing["last_seen_block"] = max(
            existing.get("last_seen_block") or delta["last_seen_block"],
            delta["last_seen_block"],
        )
        existing["updated_at"] = updated_at


def process_transaction(tx: Dict[str, Any], wallet_deltas: Dict[str, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    tx_hash = normalize_hash(tx.get("hash"))
    if not tx_hash:
        return None

    block_number = to_int(tx.get("block_number"))
    from_address = normalize_address(tx.get("from"))
    to_address = normalize_address(tx.get("to"))
    gas_used = to_int(tx.get("gas_used"))
    value_wei = to_int(tx.get("value"))

    add_delta(
        wallet_deltas,
        from_address,
        tx_count_delta=1,
        gas_used_delta=gas_used,
        native_volume_delta_wei=value_wei,
        block_number=block_number,
    )

    add_delta(
        wallet_deltas,
        to_address,
        tx_count_delta=0,
        gas_used_delta=0,
        native_volume_delta_wei=value_wei,
        block_number=block_number,
    )

    return {
        "hash": tx_hash,
        "block_number": block_number,
    }



def load_initial_backfill_anchor() -> Optional[str]:
    path = snapshots_dir() / "backfill-from-latest-to-genesis.json"

    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    audit = payload.get("minimal_audit") or {}
    tx_hash = normalize_hash(audit.get("first_transaction_hash"))
    return tx_hash or None


def run_sync(max_pages: int) -> Dict[str, Any]:
    latest = read_json(latest_path())
    checkpoint_before = deepcopy(latest.get("checkpoint", {}))

    historical_backfill_complete = bool(
        checkpoint_before.get("historical_backfill_complete")
    )

    mode = "INCREMENTAL_SYNC" if historical_backfill_complete else "HISTORICAL_BACKFILL"

    cursor = checkpoint_before.get("last_transaction_cursor")
    if mode == "INCREMENTAL_SYNC" and checkpoint_before.get("sync_phase") != "INCREMENTAL_SYNC_IN_PROGRESS":
        cursor = None

    incremental_anchor_hash = (
        checkpoint_before.get("incremental_anchor_hash")
        or checkpoint_before.get("latest_seen_transaction_hash")
        or load_initial_backfill_anchor()
    )

    wallet_deltas: Dict[str, Dict[str, Any]] = {}
    processed_transactions = 0
    first_tx_hash = None
    last_tx_hash = None
    first_block = None
    last_block = None
    next_cursor = cursor
    reached_incremental_anchor = False
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

            tx_hash = normalize_hash(tx.get("hash"))

            if mode == "INCREMENTAL_SYNC" and incremental_anchor_hash and tx_hash == incremental_anchor_hash:
                reached_incremental_anchor = True
                stop_reason = "REACHED_PREVIOUS_INCREMENTAL_ANCHOR"
                break

            audit = process_transaction(tx, wallet_deltas)
            if not audit:
                continue

            processed_transactions += 1
            first_tx_hash = first_tx_hash or audit["hash"]
            last_tx_hash = audit["hash"]
            first_block = audit["block_number"] if first_block is None else max(first_block, audit["block_number"])
            last_block = audit["block_number"] if last_block is None else min(last_block, audit["block_number"])

        if reached_incremental_anchor:
            next_cursor = None
            break

        next_cursor = payload.get("next_page_params")

        if not next_cursor:
            stop_reason = "NO_NEXT_PAGE_PARAMS_REACHED_GENESIS" if mode == "HISTORICAL_BACKFILL" else "NO_NEXT_PAGE_PARAMS"
            break

    if stop_reason is None:
        stop_reason = "MAX_PAGES_REACHED"

    apply_deltas(latest, wallet_deltas)

    if mode == "HISTORICAL_BACKFILL":
        historical_backfill_complete = next_cursor is None and stop_reason == "NO_NEXT_PAGE_PARAMS_REACHED_GENESIS"

        checkpoint_after = {
            "sync_phase": "BACKFILL_COMPLETE" if historical_backfill_complete else "HISTORICAL_BACKFILL_IN_PROGRESS",
            "historical_backfill_complete": historical_backfill_complete,
            "backfill_status": "COMPLETE" if historical_backfill_complete else "IN_PROGRESS",
            "backfill_stop_reason": stop_reason,
            "last_synced_block": last_block if last_block is not None else checkpoint_before.get("last_synced_block"),
            "last_transaction_cursor": None if historical_backfill_complete else next_cursor,
            "last_transaction_hash": last_tx_hash or checkpoint_before.get("last_transaction_hash"),
            "latest_seen_transaction_hash": checkpoint_before.get("latest_seen_transaction_hash") or load_initial_backfill_anchor() or first_tx_hash,
            "incremental_anchor_hash": checkpoint_before.get("incremental_anchor_hash") or load_initial_backfill_anchor() or first_tx_hash,
            "last_sync_at": now_utc(),
        }
    else:
        incremental_complete = reached_incremental_anchor or next_cursor is None

        checkpoint_after = {
            "sync_phase": "INCREMENTAL_SYNC" if incremental_complete else "INCREMENTAL_SYNC_IN_PROGRESS",
            "historical_backfill_complete": True,
            "backfill_status": "COMPLETE",
            "backfill_stop_reason": checkpoint_before.get("backfill_stop_reason"),
            "last_synced_block": last_block if last_block is not None else checkpoint_before.get("last_synced_block"),
            "last_transaction_cursor": None if incremental_complete else next_cursor,
            "last_transaction_hash": last_tx_hash or checkpoint_before.get("last_transaction_hash"),
            "latest_seen_transaction_hash": first_tx_hash or checkpoint_before.get("latest_seen_transaction_hash"),
            "incremental_anchor_hash": first_tx_hash or incremental_anchor_hash,
            "last_sync_at": now_utc(),
            "incremental_stop_reason": stop_reason,
        }

    latest["status"] = "SYNCED"
    latest["updated_at"] = now_utc()
    latest["checkpoint"] = checkpoint_after
    latest["counters"] = {
        "total_processed_transactions": int(latest.get("counters", {}).get("total_processed_transactions", 0)) + processed_transactions,
        "total_indexed_wallets": len(latest.get("wallet_metrics", {})),
        "last_sync_processed_transactions": processed_transactions,
        "last_sync_wallets_changed": len(wallet_deltas),
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
        "data_model": latest["data_model"],
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
        "latest_snapshot": snapshot_rel,
        "stop_reason": stop_reason,
        "historical_backfill_complete": checkpoint_after.get("historical_backfill_complete"),
        "checkpoint_after": checkpoint_after,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync WIL v3 rank-data-engine normalized wallet metrics.")
    parser.add_argument("--max-pages", type=int, default=5, help="Maximum transaction pages to process in this run.")
    args = parser.parse_args()

    if args.max_pages <= 0:
        raise SystemExit("--max-pages must be greater than 0")

    result = run_sync(args.max_pages)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
