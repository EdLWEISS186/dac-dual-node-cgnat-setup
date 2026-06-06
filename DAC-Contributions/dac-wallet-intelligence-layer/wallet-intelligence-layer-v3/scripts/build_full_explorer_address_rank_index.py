#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Full Explorer Address Rank Indexer

Final purpose:
- Build Native Funds Rank and Transactions Rank from the full Explorer-visible
  address population exposed by the official DAC Explorer API.
- Use /api/v2/stats for live network population.
- Use /api/v2/addresses pagination as the Explorer-visible address source.
- Never publish partial/manual validation runs as final rank data.

Public sources:
- Explorer: https://exptest.dachain.tech/
- Explorer API v2: https://exptest.dachain.tech/api/v2

Modes:
- --probe:
    Fetch stats and one address page only. Does not write public rank data.
- --full --publish:
    Paginate until the Explorer API ends, calculate full indexed ranks, and publish
    wallet-rank-summary.json plus rank-shards/*.json.
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
from typing import Any, Dict, Iterable, Optional


EXPLORER = "https://exptest.dachain.tech"
EXPLORER_API_V2 = f"{EXPLORER}/api/v2"
CHAIN_ID = 21894
NATIVE_TOKEN = "DACC"
REQUEST_TIMEOUT_SECONDS = 30
REQUEST_DELAY_SECONDS = 0.18
SHARD_PREFIX_LENGTH = 2


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def fetch_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Wallet-Intelligence-Layer-v3-Full-Explorer-Indexer/1.0",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def build_url(path: str, params: Optional[Dict[str, Any]] = None) -> str:
    url = f"{EXPLORER_API_V2}{path}"
    if params:
        clean_params = {k: v for k, v in params.items() if v is not None}
        if clean_params:
            url += "?" + urllib.parse.urlencode(clean_params)
    return url


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_address(value: Any) -> str:
    address = str(value or "").strip().lower()
    if address.startswith("0x") and len(address) == 42:
        return address
    return ""


def normalize_int_string(value: Any) -> str:
    raw = str(value or "0").strip()
    if not raw or not raw.isdigit():
        return "0"
    return raw.lstrip("0") or "0"


def to_int(value: Any) -> int:
    raw = str(value or "0").strip()
    if not raw or not raw.isdigit():
        return 0
    return int(raw)


def wei_to_native_string(wei: Any) -> str:
    amount = Decimal(normalize_int_string(wei)) / Decimal(10**18)
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


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=FILE")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS addresses (
            address TEXT PRIMARY KEY,
            native_funds_wei TEXT NOT NULL,
            native_funds_digits INTEGER NOT NULL,
            transactions_count INTEGER NOT NULL,
            is_contract INTEGER NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_native_funds ON addresses(native_funds_digits DESC, native_funds_wei DESC)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_transactions ON addresses(transactions_count DESC)")
    conn.commit()
    return conn


def insert_address_batch(conn: sqlite3.Connection, items: Iterable[Dict[str, Any]]) -> int:
    rows = []

    for item in items:
        address = normalize_address(item.get("hash"))
        if not address:
            continue

        native_wei = normalize_int_string(item.get("coin_balance"))
        tx_count = to_int(item.get("transactions_count"))
        is_contract = 1 if item.get("is_contract") else 0

        rows.append(
            (
                address,
                native_wei,
                len(native_wei),
                tx_count,
                is_contract,
            )
        )

    if not rows:
        return 0

    before_count = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]

    conn.executemany(
        """
        INSERT OR IGNORE INTO addresses (
            address,
            native_funds_wei,
            native_funds_digits,
            transactions_count,
            is_contract
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        rows,
    )
    conn.commit()

    after_count = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]
    return after_count - before_count



def read_checkpoint(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def write_checkpoint(path: Path, payload: Dict[str, Any]) -> None:
    write_json(path, payload)


def clear_checkpoint(path: Path) -> None:
    if path.exists():
        path.unlink()


def normalize_page_params(params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not isinstance(params, dict):
        return {}

    return {
        key: value
        for key, value in params.items()
        if value is not None
    }


def fetch_all_addresses(
    conn: sqlite3.Connection,
    max_pages: int = 0,
    page_size_hint: int = 50,
    checkpoint_path: Optional[Path] = None,
    resume: bool = True,
    reset: bool = False,
) -> Dict[str, Any]:
    checkpoint_path = checkpoint_path or Path("full-address-indexer-checkpoint.json")

    if reset:
        print("[INFO] Reset requested. Clearing checkpoint and indexed address table.")
        clear_checkpoint(checkpoint_path)
        conn.execute("DELETE FROM addresses")
        conn.commit()

    checkpoint = read_checkpoint(checkpoint_path) if resume else {}
    page = int(checkpoint.get("pages_fetched", 0))
    inserted = int(checkpoint.get("rows_inserted_or_replaced", 0))
    next_page_params = checkpoint.get("next_page_params")
    resumed_from_checkpoint = bool(checkpoint and next_page_params)

    if resumed_from_checkpoint:
        print(f"[INFO] Resuming from checkpoint after page {page}.")
    else:
        print("[INFO] Starting Explorer address pagination from the first page.")

    completed_full_pagination = False
    stop_reason = None

    while True:
        page += 1

        if max_pages and page > max_pages:
            completed_full_pagination = False
            stop_reason = "MAX_PAGES_REACHED_VALIDATION_ONLY"
            break

        params = normalize_page_params(next_page_params)
        if page_size_hint and not params:
            params.setdefault("items_count", page_size_hint)

        url = build_url("/addresses", params)
        print(f"[INFO] Fetching Explorer address page {page}: {url}")

        payload = fetch_json(url)
        items = payload.get("items", [])

        if not isinstance(items, list) or not items:
            completed_full_pagination = True
            stop_reason = "NO_MORE_ITEMS"
            print("[INFO] Explorer returned no more address items.")
            break

        inserted_this_page = insert_address_batch(conn, items)
        inserted += inserted_this_page

        previous_page_params = normalize_page_params(next_page_params)
        next_page_params = normalize_page_params(payload.get("next_page_params"))
        total_rows = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]

        if inserted_this_page == 0:
            completed_full_pagination = False
            stop_reason = "STALLED_PAGINATION_DUPLICATE_PAGE"
            print("[WARN] Pagination appears stalled: page returned no new unique addresses.")
            print("[WARN] Refusing to continue because full rank output requires reliable full pagination.")
            break

        if next_page_params and next_page_params == previous_page_params:
            completed_full_pagination = False
            stop_reason = "STALLED_PAGINATION_REPEATED_NEXT_PAGE_PARAMS"
            print("[WARN] Pagination appears stalled: next_page_params repeated.")
            print("[WARN] Refusing to continue because full rank output requires reliable full pagination.")
            break

        checkpoint_payload = {
            "project": "Wallet Intelligence Layer v3.0.0",
            "feature": "Wallet Rank Intelligence",
            "status": "IN_PROGRESS",
            "updated_at": now_utc(),
            "pages_fetched": page,
            "rows_inserted_or_replaced": inserted,
            "total_rows": total_rows,
            "last_page_item_count": len(items),
            "last_page_inserted_new_unique_rows": inserted_this_page,
            "next_page_params": next_page_params,
            "source_endpoint": f"{EXPLORER_API_V2}/addresses",
            "integrity_note": "This checkpoint is for resume safety only. It is not final rank data."
        }
        write_checkpoint(checkpoint_path, checkpoint_payload)

        if not next_page_params:
            completed_full_pagination = True
            stop_reason = "NO_NEXT_PAGE_PARAMS"
            print("[INFO] Explorer pagination completed. No next_page_params returned.")
            break

        time.sleep(REQUEST_DELAY_SECONDS)

    total_rows = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]

    final_checkpoint = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "status": "FULL_PAGINATION_COMPLETE" if completed_full_pagination else "VALIDATION_OR_INCOMPLETE_RUN",
        "updated_at": now_utc(),
        "pages_fetched": page if not (max_pages and page > max_pages) else max_pages,
        "rows_inserted_or_replaced": inserted,
        "total_rows": total_rows,
        "next_page_params": None if completed_full_pagination else next_page_params,
        "completed_full_pagination": completed_full_pagination,
        "stop_reason": stop_reason,
        "source_endpoint": f"{EXPLORER_API_V2}/addresses",
        "integrity_note": "Capped/incomplete runs are validation only and must not be published as final rank data."
    }
    write_checkpoint(checkpoint_path, final_checkpoint)

    return {
        "pages_fetched": final_checkpoint["pages_fetched"],
        "rows_inserted_or_replaced": inserted,
        "total_rows": total_rows,
        "completed_full_pagination": completed_full_pagination,
        "resumed_from_checkpoint": resumed_from_checkpoint,
        "checkpoint_path": str(checkpoint_path),
        "stop_reason": stop_reason,
    }


def calculate_and_export_shards(conn: sqlite3.Connection, out_dir: Path, stats: Dict[str, Any]) -> Dict[str, Any]:
    shards_dir = out_dir / "rank-shards"
    shards_dir.mkdir(parents=True, exist_ok=True)

    total_ranked = conn.execute("SELECT COUNT(*) FROM addresses").fetchone()[0]

    if total_ranked == 0:
        raise RuntimeError("No addresses indexed. Cannot export rank shards.")

    print("[INFO] Building ranked temporary table...")
    conn.execute("DROP TABLE IF EXISTS ranked_addresses")
    conn.execute(
        """
        CREATE TABLE ranked_addresses AS
        WITH ranked AS (
            SELECT
                address,
                native_funds_wei,
                transactions_count,
                is_contract,
                RANK() OVER (
                    ORDER BY native_funds_digits DESC, native_funds_wei DESC
                ) AS native_funds_rank,
                RANK() OVER (
                    ORDER BY transactions_count DESC
                ) AS transactions_rank
            FROM addresses
        ),
        scored AS (
            SELECT
                *,
                CAST(native_funds_rank AS REAL) / ? AS native_funds_percent,
                CAST(transactions_rank AS REAL) / ? AS transactions_percent,
                (
                    (CAST(native_funds_rank AS REAL) / ?) +
                    (CAST(transactions_rank AS REAL) / ?)
                ) AS overall_seed
            FROM ranked
        )
        SELECT
            *,
            RANK() OVER (
                ORDER BY overall_seed ASC
            ) AS overall_rank
        FROM scored
        """,
        (total_ranked, total_ranked, total_ranked, total_ranked),
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_ranked_address ON ranked_addresses(address)")
    conn.commit()

    print("[INFO] Exporting rank shards...")
    shard_payloads: Dict[str, Dict[str, Any]] = {}

    cursor = conn.execute(
        """
        SELECT
            address,
            native_funds_wei,
            transactions_count,
            is_contract,
            native_funds_rank,
            transactions_rank,
            overall_rank
        FROM ranked_addresses
        ORDER BY address ASC
        """
    )

    for row in cursor:
        (
            address,
            native_funds_wei,
            transactions_count,
            is_contract,
            native_funds_rank,
            transactions_rank,
            overall_rank,
        ) = row

        shard = shard_for_address(address)
        payload = shard_payloads.setdefault(shard, {})

        payload[address] = {
            "address": address,
            "metrics": {
                "native_funds": wei_to_native_string(native_funds_wei),
                "transactions": transactions_count,
                "gas_used": None,
                "native_volume": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None
            },
            "ranks": {
                "native_funds": native_funds_rank,
                "transactions": transactions_rank,
                "gas_used": None,
                "native_volume": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None,
                "overall_rank": overall_rank
            },
            "percentiles": {
                "native_funds": rank_percent(native_funds_rank, total_ranked),
                "transactions": rank_percent(transactions_rank, total_ranked),
                "gas_used": None,
                "native_volume": None,
                "nft_holdings": None,
                "collection_diversity": None,
                "reputation_score": None,
                "low_sybil_risk": None,
                "overall_rank": rank_percent(overall_rank, total_ranked)
            },
            "total_ranked_wallets": total_ranked,
            "rank_tier": "INDEXED",
            "available_rank_variables": [
                "native_funds",
                "transactions",
                "overall_rank"
            ],
            "pending_rank_variables": [
                "gas_used",
                "native_volume",
                "nft_holdings",
                "collection_diversity",
                "reputation_score",
                "low_sybil_risk"
            ],
            "is_contract": bool(is_contract)
        }

        if len(payload) >= 25000:
            write_shard(shards_dir, shard, payload)
            shard_payloads[shard] = {}

    shard_count = 0
    for shard, payload in shard_payloads.items():
        if payload:
            write_shard(shards_dir, shard, payload)
            shard_count += 1

    return {
        "total_ranked_wallets": total_ranked,
        "shard_count": shard_count,
        "shard_prefix_length": SHARD_PREFIX_LENGTH,
        "network_snapshot": {
            "total_addresses": stats.get("total_addresses"),
            "total_transactions": stats.get("total_transactions"),
            "transactions_today": stats.get("transactions_today"),
            "gas_used_today": stats.get("gas_used_today"),
            "total_blocks": stats.get("total_blocks"),
            "network_utilization_percentage": stats.get("network_utilization_percentage"),
        },
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_shard(shards_dir: Path, shard: str, payload: Dict[str, Any]) -> None:
    path = shards_dir / f"{shard}.json"
    existing: Dict[str, Any] = {}

    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    existing.update(payload)
    write_json(path, existing)


def run_probe() -> None:
    stats = fetch_json(build_url("/stats"))
    first_page = fetch_json(build_url("/addresses", {"items_count": 5}))

    print("[PROBE] Explorer API stats fields:")
    for key in [
        "total_addresses",
        "total_transactions",
        "transactions_today",
        "gas_used_today",
        "total_blocks",
        "network_utilization_percentage",
    ]:
        print(f"  {key}: {stats.get(key)}")

    items = first_page.get("items", [])
    print(f"[PROBE] First address page item count: {len(items) if isinstance(items, list) else 0}")
    if isinstance(items, list) and items:
        sample = items[0]
        print("[PROBE] First address item fields:")
        for key in ["hash", "coin_balance", "transactions_count", "is_contract"]:
            print(f"  {key}: {sample.get(key)}")

    print("[PROBE] No public rank data was written.")


def main() -> None:
    root = project_root()

    parser = argparse.ArgumentParser(description="Build full Explorer-visible address rank index.")
    parser.add_argument("--probe", action="store_true", help="Fetch stats and one small page only. Writes no public rank data.")
    parser.add_argument("--full", action="store_true", help="Run full Explorer address pagination.")
    parser.add_argument("--publish", action="store_true", help="Publish wallet-rank-summary.json and rank-shards output after a completed full run.")
    parser.add_argument("--max-pages", type=int, default=0, help="Development-only page cap. Must not be used for final published rank data.")
    parser.add_argument("--page-size-hint", type=int, default=50, help="Explorer pagination items_count hint.")
    parser.add_argument("--resume", action="store_true", help="Resume from the last checkpoint when available.")
    parser.add_argument("--reset", action="store_true", help="Clear checkpoint and local work DB before running.")
    parser.add_argument("--work-dir", default=str(root / "data" / "indexer-work"), help="Local work/cache directory.")
    parser.add_argument("--out-dir", default=str(root / "data"), help="Output data directory.")
    args = parser.parse_args()

    if args.probe:
        run_probe()
        return

    if not args.full:
        raise SystemExit("Use --probe for verification or --full for full Explorer-visible indexing.")

    if args.publish and args.max_pages:
        raise SystemExit("Refusing to publish a capped run. Final publish requires --full without --max-pages.")

    work_dir = Path(args.work_dir)
    out_dir = Path(args.out_dir)
    db_path = work_dir / "explorer-address-rank.sqlite"

    stats = fetch_json(build_url("/stats"))
    conn = init_db(db_path)

    checkpoint_path = work_dir / "full-address-indexer-checkpoint.json"
    fetch_result = fetch_all_addresses(
        conn,
        max_pages=args.max_pages,
        page_size_hint=args.page_size_hint,
        checkpoint_path=checkpoint_path,
        resume=args.resume,
        reset=args.reset,
    )

    work_summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "status": "FULL_PAGINATION_COMPLETE" if fetch_result["completed_full_pagination"] else "VALIDATION_OR_INCOMPLETE_RUN",
        "generated_at": now_utc(),
        "explorer_api_v2": EXPLORER_API_V2,
        "fetch_result": fetch_result,
        "network_snapshot": {
            "total_addresses": stats.get("total_addresses"),
            "total_transactions": stats.get("total_transactions"),
            "transactions_today": stats.get("transactions_today"),
            "gas_used_today": stats.get("gas_used_today"),
            "total_blocks": stats.get("total_blocks"),
            "network_utilization_percentage": stats.get("network_utilization_percentage"),
        },
        "integrity_note": "Capped/incomplete runs are validation only and must not be published as final rank data."
    }

    write_json(work_dir / "full-address-indexer-work-summary.json", work_summary)

    if not args.publish:
        print("[OK] Address indexing completed for work DB only.")
        print(f"[OK] Work DB: {db_path}")
        print(f"[OK] Work summary: {work_dir / 'full-address-indexer-work-summary.json'}")
        print("[INFO] No public rank data was published because --publish was not used.")
        return

    if not fetch_result["completed_full_pagination"]:
        raise SystemExit("Refusing to publish because full Explorer pagination did not complete.")

    export_result = calculate_and_export_shards(conn, out_dir, stats)

    summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "core_statement": "v3 turns every verified wallet variable into a comparative public rank signal.",
        "network": "DAC Testnet",
        "chain_id": CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "rank_model": "wallet-rank-intelligence-v3.0.0-full-explorer-address-index",
        "status": "GENERATED_FROM_FULL_EXPLORER_ADDRESS_INDEX",
        "generated_at": now_utc(),
        "public_sources": {
            "rpc": "https://rpctest.dachain.tech/",
            "explorer": EXPLORER,
            "explorer_api": "https://exptest.dachain.tech/api",
            "explorer_api_v2": EXPLORER_API_V2
        },
        "network_snapshot_source": f"{EXPLORER_API_V2}/stats",
        "network_snapshot": export_result["network_snapshot"],
        "total_ranked_wallets": export_result["total_ranked_wallets"],
        "latest_indexed_block": stats.get("total_blocks"),
        "ranking_variables": [
            "native_funds",
            "transactions",
            "overall_rank"
        ],
        "pending_ranking_variables": [
            "gas_used",
            "native_volume",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk"
        ],
        "rank_shards": {
            "directory": "data/rank-shards",
            "prefix_length": SHARD_PREFIX_LENGTH,
            "shard_count": export_result["shard_count"]
        },
        "index_scope": {
            "source_endpoint": f"{EXPLORER_API_V2}/addresses",
            "pagination": "completed_until_no_next_page_params",
            "manual_limited_run": false
        },
        "note": "Full Explorer-visible address index. Native funds, transactions, and preliminary overall rank are active. Other rank metrics require additional custom indexer logic."
    }

    write_json(out_dir / "wallet-rank-summary.json", summary)
    write_json(out_dir / "wallet-rank-index.json", {
        "mode": "SHARDED",
        "directory": "data/rank-shards",
        "summary": "Use rank-shards/{address_prefix}.json for wallet rank lookup."
    })

    print("[OK] Published full Explorer address rank index.")
    print(f"[OK] Ranked wallets: {export_result['total_ranked_wallets']}")
    print(f"[OK] Shards: {export_result['shard_count']}")
    print(f"[OK] Summary: {out_dir / 'wallet-rank-summary.json'}")


if __name__ == "__main__":
    main()
