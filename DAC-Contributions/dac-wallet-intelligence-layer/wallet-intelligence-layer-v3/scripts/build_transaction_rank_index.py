#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Transaction Rank Indexer

Purpose:
- Use official DAC Explorer API /api/v2/transactions as the custom index source.
- Aggregate wallet-level metrics from transaction stream:
  - transactions
  - gas_used
  - native_volume
- Keep public rank data unpublished unless a full/integrity-safe indexing mode is completed.

This script is the correct custom-indexer direction after /api/v2/addresses pagination
was found to be stalled/duplicated.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


EXPLORER = "https://exptest.dachain.tech"
EXPLORER_API_V2 = f"{EXPLORER}/api/v2"
CHAIN_ID = 21894
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 0.18


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_url(path: str, params: Optional[Dict[str, Any]] = None) -> str:
    url = f"{EXPLORER_API_V2}{path}"
    if params:
        clean = {k: v for k, v in params.items() if v is not None}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)
    return url


def fetch_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Wallet-Intelligence-Layer-v3-Transaction-Rank-Indexer/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_address(value: Any) -> str:
    if isinstance(value, dict):
        value = value.get("hash")
    address = str(value or "").strip().lower()
    if address.startswith("0x") and len(address) == 42:
        return address
    return ""


def normalize_hash(value: Any) -> str:
    h = str(value or "").strip().lower()
    if h.startswith("0x") and len(h) == 66:
        return h
    return ""


def to_int(value: Any) -> int:
    raw = str(value or "0").strip()
    if raw.startswith("0x"):
        return int(raw, 16)
    if raw.isdigit():
        return int(raw)
    return 0


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_transactions (
            tx_hash TEXT PRIMARY KEY,
            block_number INTEGER,
            tx_position INTEGER
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS wallet_metrics (
            address TEXT PRIMARY KEY,
            transactions_count INTEGER NOT NULL DEFAULT 0,
            gas_used INTEGER NOT NULL DEFAULT 0,
            native_volume_wei TEXT NOT NULL DEFAULT '0',
            first_seen_block INTEGER,
            last_seen_block INTEGER
        )
        """
    )
    conn.commit()
    return conn


def add_wallet_metric(
    conn: sqlite3.Connection,
    address: str,
    tx_count_delta: int,
    gas_delta: int,
    volume_delta_wei: int,
    block_number: int,
) -> None:
    if not address:
        return

    existing = conn.execute(
        "SELECT transactions_count, gas_used, native_volume_wei, first_seen_block, last_seen_block FROM wallet_metrics WHERE address = ?",
        (address,),
    ).fetchone()

    if existing:
        tx_count, gas_used, native_volume_wei, first_seen, last_seen = existing
        new_volume = int(native_volume_wei or "0") + volume_delta_wei
        conn.execute(
            """
            UPDATE wallet_metrics
            SET transactions_count = ?,
                gas_used = ?,
                native_volume_wei = ?,
                first_seen_block = ?,
                last_seen_block = ?
            WHERE address = ?
            """,
            (
                int(tx_count) + tx_count_delta,
                int(gas_used) + gas_delta,
                str(new_volume),
                min(first_seen or block_number, block_number),
                max(last_seen or block_number, block_number),
                address,
            ),
        )
    else:
        conn.execute(
            """
            INSERT INTO wallet_metrics (
                address,
                transactions_count,
                gas_used,
                native_volume_wei,
                first_seen_block,
                last_seen_block
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                address,
                tx_count_delta,
                gas_delta,
                str(volume_delta_wei),
                block_number,
                block_number,
            ),
        )


def process_transaction(conn: sqlite3.Connection, tx: Dict[str, Any]) -> bool:
    tx_hash = normalize_hash(tx.get("hash"))
    if not tx_hash:
        return False

    exists = conn.execute("SELECT 1 FROM processed_transactions WHERE tx_hash = ?", (tx_hash,)).fetchone()
    if exists:
        return False

    block_number = to_int(tx.get("block_number"))
    tx_position = to_int(tx.get("position"))
    from_address = normalize_address(tx.get("from"))
    to_address = normalize_address(tx.get("to"))
    gas_used = to_int(tx.get("gas_used"))
    value_wei = to_int(tx.get("value"))

    # Sender gets tx_count, gas_used, and native volume contribution.
    add_wallet_metric(
        conn,
        from_address,
        tx_count_delta=1,
        gas_delta=gas_used,
        volume_delta_wei=value_wei,
        block_number=block_number,
    )

    # Receiver gets volume contribution only. This can later be split into sent/received volume.
    add_wallet_metric(
        conn,
        to_address,
        tx_count_delta=0,
        gas_delta=0,
        volume_delta_wei=value_wei,
        block_number=block_number,
    )

    conn.execute(
        """
        INSERT INTO processed_transactions (tx_hash, block_number, tx_position)
        VALUES (?, ?, ?)
        """,
        (tx_hash, block_number, tx_position),
    )

    return True


def probe() -> None:
    stats = fetch_json(build_url("/stats"))
    first_page = fetch_json(build_url("/transactions"))
    items = first_page.get("items", [])
    next_params = first_page.get("next_page_params") or {}

    second_page = fetch_json(build_url("/transactions", next_params))
    first_hashes = {normalize_hash(item.get("hash")) for item in items if isinstance(item, dict)}
    second_hashes = {
        normalize_hash(item.get("hash"))
        for item in second_page.get("items", [])
        if isinstance(item, dict)
    }

    overlap = len(first_hashes.intersection(second_hashes))
    new_second = len([h for h in second_hashes if h and h not in first_hashes])

    print("[PROBE] Explorer API stats:")
    for key in ["total_addresses", "total_transactions", "transactions_today", "gas_used_today", "total_blocks"]:
        print(f"  {key}: {stats.get(key)}")

    print("[PROBE] Transactions pagination:")
    print(f"  page_1_count: {len(first_hashes)}")
    print(f"  page_2_count: {len(second_hashes)}")
    print(f"  overlap: {overlap}")
    print(f"  new_page_2: {new_second}")
    print(f"  result: {'OK_ADVANCES' if new_second else 'STUCK_OR_DUPLICATE'}")

    if items:
        sample = items[0]
        print("[PROBE] Confirmed transaction fields:")
        for key in ["hash", "block_number", "position", "from", "to", "gas_used", "value", "timestamp", "status"]:
            print(f"  {key}: {'present' if key in sample else 'missing'}")

    print("[PROBE] No public rank data was written.")


def run_validation(conn: sqlite3.Connection, max_pages: int, checkpoint_path: Path, reset: bool = False) -> Dict[str, Any]:
    if reset:
        conn.execute("DELETE FROM processed_transactions")
        conn.execute("DELETE FROM wallet_metrics")
        conn.commit()
        if checkpoint_path.exists():
            checkpoint_path.unlink()

    checkpoint = read_json(checkpoint_path)
    next_page_params = checkpoint.get("next_page_params") if checkpoint else None
    pages_fetched = int(checkpoint.get("pages_fetched", 0)) if checkpoint else 0
    processed_total = int(checkpoint.get("processed_transactions", 0)) if checkpoint else 0

    for _ in range(max_pages):
        page_number = pages_fetched + 1
        url = build_url("/transactions", next_page_params)
        print(f"[INFO] Fetching transaction page {page_number}: {url}")

        payload = fetch_json(url)
        items = payload.get("items", [])

        if not isinstance(items, list) or not items:
            stop_reason = "NO_MORE_ITEMS"
            break

        processed_this_page = 0
        for tx in items:
            if isinstance(tx, dict) and process_transaction(conn, tx):
                processed_this_page += 1

        conn.commit()
        processed_total += processed_this_page
        pages_fetched += 1

        next_page_params = payload.get("next_page_params")

        wallet_count = conn.execute("SELECT COUNT(*) FROM wallet_metrics").fetchone()[0]

        write_json(
            checkpoint_path,
            {
                "project": "Wallet Intelligence Layer v3.0.0",
                "feature": "Wallet Rank Intelligence",
                "status": "VALIDATION_OR_INCOMPLETE_RUN",
                "updated_at": now_utc(),
                "source_endpoint": f"{EXPLORER_API_V2}/transactions",
                "pages_fetched": pages_fetched,
                "processed_transactions": processed_total,
                "last_page_processed_transactions": processed_this_page,
                "wallets_seen": wallet_count,
                "next_page_params": next_page_params,
                "integrity_note": "Validation run only. No public rank data is published."
            },
        )

        if processed_this_page == 0:
            stop_reason = "STALLED_OR_DUPLICATE_TRANSACTIONS"
            break

        if not next_page_params:
            stop_reason = "NO_NEXT_PAGE_PARAMS"
            break

        time.sleep(REQUEST_DELAY_SECONDS)
    else:
        stop_reason = "MAX_PAGES_VALIDATION_ONLY"

    wallet_count = conn.execute("SELECT COUNT(*) FROM wallet_metrics").fetchone()[0]

    result = {
        "status": "VALIDATION_OR_INCOMPLETE_RUN",
        "pages_fetched": pages_fetched,
        "processed_transactions": processed_total,
        "wallets_seen": wallet_count,
        "stop_reason": stop_reason,
        "checkpoint": str(checkpoint_path),
        "public_rank_data_written": False,
    }

    write_json(checkpoint_path, {**read_json(checkpoint_path), **result, "updated_at": now_utc()})
    return result


def main() -> None:
    root = project_root()

    parser = argparse.ArgumentParser(description="Build Wallet Intelligence Layer v3 rank metrics from Explorer transaction stream.")
    parser.add_argument("--probe", action="store_true", help="Probe transaction pagination and fields only.")
    parser.add_argument("--validate-pages", type=int, default=0, help="Validation-only page count. Does not publish rank data.")
    parser.add_argument("--reset", action="store_true", help="Reset local transaction indexer work state.")
    parser.add_argument("--work-dir", default=str(root / "data" / "indexer-work"), help="Local work/cache directory.")
    args = parser.parse_args()

    if args.probe:
        probe()
        return

    if not args.validate_pages:
        raise SystemExit("Use --probe or --validate-pages N. Full publish mode will be added after validation.")

    work_dir = Path(args.work_dir)
    conn = init_db(work_dir / "transaction-rank-index.sqlite")
    result = run_validation(
        conn,
        max_pages=args.validate_pages,
        checkpoint_path=work_dir / "transaction-rank-index-checkpoint.json",
        reset=args.reset,
    )

    print("[OK] Transaction indexer validation completed.")
    for key, value in result.items():
        print(f"[OK] {key}: {value}")
    print("[INFO] No public rank data was published.")


if __name__ == "__main__":
    main()
