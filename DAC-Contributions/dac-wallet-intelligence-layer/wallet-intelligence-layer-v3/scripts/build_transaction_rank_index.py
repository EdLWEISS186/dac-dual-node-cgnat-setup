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
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Optional


EXPLORER = "https://exptest.dachain.tech"
EXPLORER_API_V2 = f"{EXPLORER}/api/v2"
CHAIN_ID = 21894
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 0.18
SHARD_PREFIX_LENGTH = 2
NATIVE_TOKEN = "DACC"


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


def shard_for_address(address: str) -> str:
    return address[2 : 2 + SHARD_PREFIX_LENGTH].lower()


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


def safe_decimal(value: Any) -> Decimal:
    try:
        return Decimal(str(value or "0"))
    except Exception:
        return Decimal("0")


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



def export_rank_shards(conn: sqlite3.Connection, out_dir: Path, stats: Dict[str, Any]) -> Dict[str, Any]:
    total_ranked = conn.execute("SELECT COUNT(*) FROM wallet_metrics").fetchone()[0]
    if total_ranked <= 0:
        raise RuntimeError("No wallet metrics available for rank export.")

    shards_dir = out_dir / "rank-shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    conn.execute("DROP TABLE IF EXISTS ranked_wallets")
    conn.execute(
        """
        CREATE TABLE ranked_wallets AS
        WITH ranked AS (
            SELECT
                address,
                transactions_count,
                gas_used,
                native_volume_wei,
                first_seen_block,
                last_seen_block,
                RANK() OVER (ORDER BY transactions_count DESC) AS transactions_rank,
                RANK() OVER (ORDER BY gas_used DESC) AS gas_used_rank,
                RANK() OVER (
                    ORDER BY LENGTH(native_volume_wei) DESC, native_volume_wei DESC
                ) AS native_volume_rank
            FROM wallet_metrics
        ),
        scored AS (
            SELECT
                *,
                (
                    (CAST(transactions_rank AS REAL) / ?) +
                    (CAST(gas_used_rank AS REAL) / ?) +
                    (CAST(native_volume_rank AS REAL) / ?)
                ) AS overall_seed
            FROM ranked
        )
        SELECT
            *,
            RANK() OVER (ORDER BY overall_seed ASC) AS overall_rank
        FROM scored
        """,
        (total_ranked, total_ranked, total_ranked),
    )
    conn.commit()

    shard_payloads: Dict[str, Dict[str, Any]] = {}
    cursor = conn.execute(
        """
        SELECT
            address,
            transactions_count,
            gas_used,
            native_volume_wei,
            first_seen_block,
            last_seen_block,
            transactions_rank,
            gas_used_rank,
            native_volume_rank,
            overall_rank
        FROM ranked_wallets
        ORDER BY address ASC
        """
    )

    for row in cursor:
        (
            address,
            transactions_count,
            gas_used,
            native_volume_wei,
            first_seen_block,
            last_seen_block,
            transactions_rank,
            gas_used_rank,
            native_volume_rank,
            overall_rank,
        ) = row

        tx_percent = safe_decimal(rank_percent(transactions_rank, total_ranked))
        gas_percent = safe_decimal(rank_percent(gas_used_rank, total_ranked))
        volume_percent = safe_decimal(rank_percent(native_volume_rank, total_ranked))
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
        payload = shard_payloads.setdefault(shard, {})
        payload[address] = {
            "address": address,
            "metrics": {
                "transactions": transactions_count,
                "gas_used": gas_used,
                "native_volume": wei_to_native_string(native_volume_wei),
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None
            },
            "ranks": {
                "transactions": transactions_rank,
                "gas_used": gas_used_rank,
                "native_volume": native_volume_rank,
                "overall_rank": overall_rank,
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None
            },
            "percentiles": {
                "transactions": rank_percent(transactions_rank, total_ranked),
                "gas_used": rank_percent(gas_used_rank, total_ranked),
                "native_volume": rank_percent(native_volume_rank, total_ranked),
                "overall_rank": rank_percent(overall_rank, total_ranked),
                "native_funds": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None
            },
            "total_ranked_wallets": total_ranked,
            "rank_tier": rank_tier(best_percent),
            "strongest_metric": strongest_metric,
            "available_rank_variables": [
                "transactions",
                "gas_used",
                "native_volume",
                "overall_rank"
            ],
            "pending_rank_variables": [
                "native_funds",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk"
            ],
            "first_seen_block": first_seen_block,
            "last_seen_block": last_seen_block
        }

    shard_count = 0
    for shard, payload in shard_payloads.items():
        if not payload:
            continue
        write_json(shards_dir / f"{shard}.json", payload)
        shard_count += 1

    summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "core_statement": "v3 turns every verified wallet variable into a comparative public rank signal.",
        "network": "DAC Testnet",
        "chain_id": CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "rank_model": "wallet-rank-intelligence-v3.0.0-transaction-stream-index",
        "status": "GENERATED_FROM_TRANSACTION_STREAM_INDEX",
        "generated_at": now_utc(),
        "public_sources": {
            "rpc": "https://rpctest.dachain.tech/",
            "explorer": EXPLORER,
            "explorer_api": "https://exptest.dachain.tech/api",
            "explorer_api_v2": EXPLORER_API_V2
        },
        "network_snapshot_source": f"{EXPLORER_API_V2}/stats",
        "network_snapshot": {
            "total_addresses": stats.get("total_addresses"),
            "total_transactions": stats.get("total_transactions"),
            "transactions_today": stats.get("transactions_today"),
            "gas_used_today": stats.get("gas_used_today"),
            "total_blocks": stats.get("total_blocks"),
            "network_utilization_percentage": stats.get("network_utilization_percentage")
        },
        "total_ranked_wallets": total_ranked,
        "latest_indexed_block": conn.execute("SELECT MAX(last_seen_block) FROM wallet_metrics").fetchone()[0],
        "earliest_indexed_block": conn.execute("SELECT MIN(first_seen_block) FROM wallet_metrics").fetchone()[0],
        "ranking_variables": [
            "transactions",
            "gas_used",
            "native_volume",
            "overall_rank"
        ],
        "pending_ranking_variables": [
            "native_funds",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk"
        ],
        "rank_shards": {
            "directory": "data/rank-shards",
            "prefix_length": SHARD_PREFIX_LENGTH,
            "shard_count": shard_count
        },
        "index_scope": {
            "source_endpoint": f"{EXPLORER_API_V2}/transactions",
            "note": "Ranks are generated from the completed transaction-stream index state. Validation/capped runs must not be published as final rank data."
        },
        "note": "Transaction-stream rank index. Transactions, gas_used, native_volume, and preliminary overall rank are active."
    }

    write_json(out_dir / "wallet-rank-summary.json", summary)
    write_json(out_dir / "wallet-rank-index.json", {
        "mode": "SHARDED",
        "directory": "data/rank-shards",
        "summary": "Use rank-shards/{address_prefix}.json for wallet rank lookup."
    })

    return {
        "total_ranked_wallets": total_ranked,
        "shard_count": shard_count,
        "summary": str(out_dir / "wallet-rank-summary.json")
    }


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


def run_indexing(
    conn: sqlite3.Connection,
    checkpoint_path: Path,
    max_pages: int = 0,
    reset: bool = False,
    full: bool = False,
) -> Dict[str, Any]:
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

    stop_reason = None

    while True:
        if max_pages and pages_fetched >= max_pages:
            stop_reason = "MAX_PAGES_VALIDATION_ONLY"
            break

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
                "status": "FULL_INDEX_IN_PROGRESS" if full else "VALIDATION_OR_INCOMPLETE_RUN",
                "updated_at": now_utc(),
                "source_endpoint": f"{EXPLORER_API_V2}/transactions",
                "pages_fetched": pages_fetched,
                "processed_transactions": processed_total,
                "last_page_processed_transactions": processed_this_page,
                "wallets_seen": wallet_count,
                "next_page_params": next_page_params,
                "integrity_note": "No public rank data is published unless full mode completes and publish is explicitly requested."
            },
        )

        if processed_this_page == 0:
            stop_reason = "STALLED_OR_DUPLICATE_TRANSACTIONS"
            break

        if not next_page_params:
            stop_reason = "NO_NEXT_PAGE_PARAMS_FULL_STREAM_COMPLETE"
            break

        time.sleep(REQUEST_DELAY_SECONDS)

    completed_full_stream = stop_reason == "NO_NEXT_PAGE_PARAMS_FULL_STREAM_COMPLETE"
    wallet_count = conn.execute("SELECT COUNT(*) FROM wallet_metrics").fetchone()[0]

    result = {
        "status": "FULL_STREAM_COMPLETE" if completed_full_stream else "VALIDATION_OR_INCOMPLETE_RUN",
        "pages_fetched": pages_fetched,
        "processed_transactions": processed_total,
        "wallets_seen": wallet_count,
        "stop_reason": stop_reason,
        "completed_full_stream": completed_full_stream,
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
    parser.add_argument("--full", action="store_true", help="Run until transaction stream pagination ends.")
    parser.add_argument("--publish", action="store_true", help="Publish rank summary and shards only after a completed full stream.")
    parser.add_argument("--reset", action="store_true", help="Reset local transaction indexer work state.")
    parser.add_argument("--work-dir", default=str(root / "data" / "indexer-work"), help="Local work/cache directory.")
    parser.add_argument("--out-dir", default=str(root / "data"), help="Public output directory.")
    args = parser.parse_args()

    if args.probe:
        probe()
        return

    if not args.validate_pages and not args.full:
        raise SystemExit("Use --probe, --validate-pages N, or --full. Publishing requires --full --publish.")

    if args.publish and not args.full:
        raise SystemExit("Refusing to publish without --full.")

    if args.publish and args.validate_pages:
        raise SystemExit("Refusing to publish a capped validation run.")

    work_dir = Path(args.work_dir)
    out_dir = Path(args.out_dir)
    conn = init_db(work_dir / "transaction-rank-index.sqlite")
    result = run_indexing(
        conn,
        checkpoint_path=work_dir / "transaction-rank-index-checkpoint.json",
        max_pages=args.validate_pages,
        reset=args.reset,
        full=args.full,
    )

    if args.publish:
        if not result.get("completed_full_stream"):
            raise SystemExit("Refusing to publish because the full transaction stream did not complete.")
        stats = fetch_json(build_url("/stats"))
        export_result = export_rank_shards(conn, out_dir, stats)
        result["public_rank_data_written"] = True
        result["export_result"] = export_result
        write_json(work_dir / "transaction-rank-index-checkpoint.json", {**read_json(work_dir / "transaction-rank-index-checkpoint.json"), **result, "updated_at": now_utc()})

    print("[OK] Transaction indexer run completed.")
    for key, value in result.items():
        print(f"[OK] {key}: {value}")
    if not result.get("public_rank_data_written"):
        print("[INFO] No public rank data was published.")


if __name__ == "__main__":
    main()
