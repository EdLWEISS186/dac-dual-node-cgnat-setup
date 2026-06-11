#!/usr/bin/env python3
"""
WIL v3.3.0 Official Testnet Inception NFT gap repair scanner.

Repairs the block range processed before Official Inception NFT ownership
tracking was introduced.

The main WIL synchronization checkpoint is never modified.

The scanner is resumable and stores its own checkpoint in:
    official_inception_nft_repair_state

Only ERC-721 Transfer logs from the official contract are requested.
Temporary query results remain in memory only and are discarded after
each persisted query batch.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from local_rpc_rank_data_worker import (
    CHAIN_ID,
    DEFAULT_FALLBACK_RPC,
    DEFAULT_PRIMARY_RPC,
    OFFICIAL_INCEPTION_NFT_CONTRACT,
    TRANSFER_TOPIC,
    decode_address_topic,
    hex_to_int,
    int_to_hex,
    normalize_address,
    rpc_call,
)
from sqlite_rank_state import SQLiteRankState


DEFAULT_REPAIR_ID = (
    "WIL_V3_3_0_PRE_OFFICIAL_INCEPTION_NFT_TRACKING_GAP"
)


def now_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )


def ensure_repair_schema(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS
            official_inception_nft_repair_state (
                repair_id TEXT PRIMARY KEY,

                from_block INTEGER NOT NULL,
                to_block INTEGER NOT NULL,
                next_block INTEGER NOT NULL,

                status TEXT NOT NULL,

                processed_blocks INTEGER
                    NOT NULL DEFAULT 0,

                query_batches INTEGER
                    NOT NULL DEFAULT 0,

                transfer_logs INTEGER
                    NOT NULL DEFAULT 0,

                applied_transfers INTEGER
                    NOT NULL DEFAULT 0,

                token_rows_written INTEGER
                    NOT NULL DEFAULT 0,

                last_processed_block INTEGER,

                started_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                completed_at TEXT
            );
        """
    )

    connection.commit()


def load_repair_state(
    connection: sqlite3.Connection,
    repair_id: str,
) -> Optional[Dict[str, Any]]:
    row = connection.execute(
        """
        SELECT
            repair_id,
            from_block,
            to_block,
            next_block,
            status,
            processed_blocks,
            query_batches,
            transfer_logs,
            applied_transfers,
            token_rows_written,
            last_processed_block,
            started_at,
            updated_at,
            completed_at
        FROM official_inception_nft_repair_state
        WHERE repair_id = ?
        """,
        (repair_id,),
    ).fetchone()

    if row is None:
        return None

    keys = [
        "repair_id",
        "from_block",
        "to_block",
        "next_block",
        "status",
        "processed_blocks",
        "query_batches",
        "transfer_logs",
        "applied_transfers",
        "token_rows_written",
        "last_processed_block",
        "started_at",
        "updated_at",
        "completed_at",
    ]

    return dict(zip(keys, row))


def initialize_repair_state(
    connection: sqlite3.Connection,
    repair_id: str,
    from_block: int,
    to_block: int,
) -> Dict[str, Any]:
    timestamp = now_utc()

    repair = {
        "repair_id": repair_id,
        "from_block": from_block,
        "to_block": to_block,
        "next_block": from_block,
        "status": "IN_PROGRESS",
        "processed_blocks": 0,
        "query_batches": 0,
        "transfer_logs": 0,
        "applied_transfers": 0,
        "token_rows_written": 0,
        "last_processed_block": None,
        "started_at": timestamp,
        "updated_at": timestamp,
        "completed_at": None,
    }

    connection.execute(
        """
        INSERT INTO official_inception_nft_repair_state (
            repair_id,
            from_block,
            to_block,
            next_block,
            status,
            processed_blocks,
            query_batches,
            transfer_logs,
            applied_transfers,
            token_rows_written,
            last_processed_block,
            started_at,
            updated_at,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            repair["repair_id"],
            repair["from_block"],
            repair["to_block"],
            repair["next_block"],
            repair["status"],
            repair["processed_blocks"],
            repair["query_batches"],
            repair["transfer_logs"],
            repair["applied_transfers"],
            repair["token_rows_written"],
            repair["last_processed_block"],
            repair["started_at"],
            repair["updated_at"],
            repair["completed_at"],
        ),
    )

    connection.commit()
    return repair


def save_repair_batch(
    rank_state: SQLiteRankState,
    repair: Dict[str, Any],
) -> int:
    tracker = rank_state.official_inception_nft_tokens

    dirty_before = set(
        tracker.dirty_token_ids
    )

    last_written_before = (
        rank_state
        .last_official_inception_nft_rows_written
    )

    try:
        rank_state.connection.execute(
            "BEGIN IMMEDIATE"
        )

        rows_written = tracker.flush()

        repair["token_rows_written"] = (
            int(repair["token_rows_written"])
            + rows_written
        )

        rank_state.connection.execute(
            """
            INSERT INTO official_inception_nft_repair_state (
                repair_id,
                from_block,
                to_block,
                next_block,
                status,
                processed_blocks,
                query_batches,
                transfer_logs,
                applied_transfers,
                token_rows_written,
                last_processed_block,
                started_at,
                updated_at,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(repair_id) DO UPDATE SET
                from_block = excluded.from_block,
                to_block = excluded.to_block,
                next_block = excluded.next_block,
                status = excluded.status,
                processed_blocks =
                    excluded.processed_blocks,
                query_batches =
                    excluded.query_batches,
                transfer_logs =
                    excluded.transfer_logs,
                applied_transfers =
                    excluded.applied_transfers,
                token_rows_written =
                    excluded.token_rows_written,
                last_processed_block =
                    excluded.last_processed_block,
                started_at =
                    excluded.started_at,
                updated_at =
                    excluded.updated_at,
                completed_at =
                    excluded.completed_at
            """,
            (
                repair["repair_id"],
                repair["from_block"],
                repair["to_block"],
                repair["next_block"],
                repair["status"],
                repair["processed_blocks"],
                repair["query_batches"],
                repair["transfer_logs"],
                repair["applied_transfers"],
                repair["token_rows_written"],
                repair["last_processed_block"],
                repair["started_at"],
                repair["updated_at"],
                repair["completed_at"],
            ),
        )

        rank_state.connection.commit()

        rank_state.last_official_inception_nft_rows_written = (
            rows_written
        )

        # Data cache query yang sudah selesai tidak dipertahankan.
        tracker.clear_cache()

        return rows_written

    except Exception:
        rank_state.connection.rollback()

        tracker.dirty_token_ids = dirty_before

        rank_state.last_official_inception_nft_rows_written = (
            last_written_before
        )

        raise


def fetch_transfer_logs(
    rpc_urls: list[str],
    low_block: int,
    high_block: int,
) -> list[Dict[str, Any]]:
    result = rpc_call(
        rpc_urls,
        "eth_getLogs",
        [
            {
                "fromBlock": int_to_hex(low_block),
                "toBlock": int_to_hex(high_block),
                "address": (
                    OFFICIAL_INCEPTION_NFT_CONTRACT
                ),
                "topics": [TRANSFER_TOPIC],
            }
        ],
        timeout=60,
    )

    return result or []


def log_position(
    log: Dict[str, Any],
) -> tuple[int, int, int]:
    return (
        hex_to_int(log.get("blockNumber")),
        hex_to_int(log.get("transactionIndex")),
        hex_to_int(log.get("logIndex")),
    )


def apply_transfer_log(
    rank_state: SQLiteRankState,
    log: Dict[str, Any],
    timestamp: str,
) -> Optional[bool]:
    contract = normalize_address(
        log.get("address")
    )

    topics = log.get("topics") or []

    if contract != OFFICIAL_INCEPTION_NFT_CONTRACT:
        return None

    if len(topics) < 4:
        return None

    if str(topics[0]).lower() != TRANSFER_TOPIC:
        return None

    try:
        token_id = str(
            hex_to_int(topics[3])
        )

        block_number = hex_to_int(
            log.get("blockNumber")
        )

        transaction_index = hex_to_int(
            log.get("transactionIndex")
        )

        log_index = hex_to_int(
            log.get("logIndex")
        )
    except (TypeError, ValueError):
        return None

    from_address = decode_address_topic(
        topics[1]
    )

    to_address = decode_address_topic(
        topics[2]
    )

    return (
        rank_state
        .official_inception_nft_tokens
        .observe_transfer(
            token_id=token_id,
            from_address=from_address,
            to_address=to_address,
            block_number=block_number,
            transaction_index=transaction_index,
            log_index=log_index,
            tx_hash=str(
                log.get("transactionHash")
                or ""
            ),
            timestamp=timestamp,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--sqlite-state",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--primary-rpc",
        default=DEFAULT_PRIMARY_RPC,
    )

    parser.add_argument(
        "--fallback-rpc",
        default=DEFAULT_FALLBACK_RPC,
    )

    parser.add_argument(
        "--from-block",
        required=True,
        type=int,
        help="Highest block in the repair range.",
    )

    parser.add_argument(
        "--to-block",
        required=True,
        type=int,
        help="Lowest block in the repair range.",
    )

    parser.add_argument(
        "--max-blocks",
        type=int,
        default=2000,
        help=(
            "Maximum blocks processed in this "
            "invocation."
        ),
    )

    parser.add_argument(
        "--query-blocks",
        type=int,
        default=250,
        help=(
            "Maximum block span requested by each "
            "eth_getLogs query."
        ),
    )

    parser.add_argument(
        "--repair-id",
        default=DEFAULT_REPAIR_ID,
    )

    args = parser.parse_args()

    if args.from_block < args.to_block:
        raise SystemExit(
            "--from-block must be greater than or "
            "equal to --to-block"
        )

    if args.to_block < 0:
        raise SystemExit(
            "--to-block must not be negative"
        )

    if args.max_blocks < 1:
        raise SystemExit(
            "--max-blocks must be greater than zero"
        )

    if args.query_blocks < 1:
        raise SystemExit(
            "--query-blocks must be greater than zero"
        )

    database = (
        args.sqlite_state
        .expanduser()
        .resolve()
    )

    if not database.is_file():
        raise SystemExit(
            f"SQLite state not found: {database}"
        )

    rpc_urls = [
        args.primary_rpc,
        args.fallback_rpc,
    ]

    rank_state = SQLiteRankState(database)

    try:
        ensure_repair_schema(
            rank_state.connection
        )

        chain_id = hex_to_int(
            rpc_call(
                rpc_urls,
                "eth_chainId",
                [],
            )
        )

        if chain_id != CHAIN_ID:
            raise SystemExit(
                f"Wrong chain ID: {chain_id}; "
                f"expected {CHAIN_ID}"
            )

        repair = load_repair_state(
            rank_state.connection,
            args.repair_id,
        )

        if repair is None:
            repair = initialize_repair_state(
                rank_state.connection,
                args.repair_id,
                args.from_block,
                args.to_block,
            )
        elif (
            int(repair["from_block"])
            != args.from_block
            or int(repair["to_block"])
            != args.to_block
        ):
            raise SystemExit(
                "Existing repair range does not match "
                "the requested range"
            )

        if repair["status"] == "COMPLETE":
            print(
                "[OK] Official Inception NFT repair "
                "is already complete"
            )

            print(
                json.dumps(
                    repair,
                    indent=2,
                    sort_keys=True,
                )
            )

            return

        next_block = int(
            repair["next_block"]
        )

        if next_block < args.to_block:
            repair["status"] = "COMPLETE"
            repair["completed_at"] = now_utc()
            repair["updated_at"] = now_utc()

            save_repair_batch(
                rank_state,
                repair,
            )

            print(
                "[OK] Official Inception NFT repair "
                "marked complete"
            )

            return

        final_block_this_run = max(
            args.to_block,
            next_block - args.max_blocks + 1,
        )

        print(
            "[INFO] WIL v3.3.0 Official Testnet "
            "Inception NFT repair"
        )
        print(f"[INFO] database={database}")
        print(
            f"[INFO] contract="
            f"{OFFICIAL_INCEPTION_NFT_CONTRACT}"
        )
        print(
            f"[INFO] repair_id="
            f"{args.repair_id}"
        )
        print(
            f"[INFO] full_range="
            f"{args.from_block}->{args.to_block}"
        )
        print(
            f"[INFO] run_range="
            f"{next_block}->{final_block_this_run}"
        )
        print(
            f"[INFO] query_blocks="
            f"{args.query_blocks}"
        )

        run_processed_blocks = 0
        run_query_batches = 0
        run_transfer_logs = 0
        run_applied_transfers = 0
        run_token_rows_written = 0

        query_high = next_block

        while query_high >= final_block_this_run:
            query_low = max(
                final_block_this_run,
                query_high - args.query_blocks + 1,
            )

            logs = fetch_transfer_logs(
                rpc_urls=rpc_urls,
                low_block=query_low,
                high_block=query_high,
            )

            # RPC returns logs in ascending order.
            # Reverse event order so the newest owner is
            # observed first during latest-to-genesis repair.
            logs = sorted(
                logs,
                key=log_position,
                reverse=True,
            )

            batch_transfer_logs = 0
            batch_applied_transfers = 0
            batch_timestamp = now_utc()

            for log in logs:
                applied = apply_transfer_log(
                    rank_state=rank_state,
                    log=log,
                    timestamp=batch_timestamp,
                )

                if applied is None:
                    continue

                batch_transfer_logs += 1

                if applied:
                    batch_applied_transfers += 1

            processed_in_batch = (
                query_high - query_low + 1
            )

            run_processed_blocks += (
                processed_in_batch
            )
            run_query_batches += 1
            run_transfer_logs += (
                batch_transfer_logs
            )
            run_applied_transfers += (
                batch_applied_transfers
            )

            repair["processed_blocks"] = (
                int(repair["processed_blocks"])
                + processed_in_batch
            )

            repair["query_batches"] = (
                int(repair["query_batches"])
                + 1
            )

            repair["transfer_logs"] = (
                int(repair["transfer_logs"])
                + batch_transfer_logs
            )

            repair["applied_transfers"] = (
                int(repair["applied_transfers"])
                + batch_applied_transfers
            )

            repair["last_processed_block"] = (
                query_low
            )

            repair["next_block"] = (
                query_low - 1
            )

            repair["updated_at"] = now_utc()

            if repair["next_block"] < args.to_block:
                repair["status"] = "COMPLETE"
                repair["completed_at"] = now_utc()

            written = save_repair_batch(
                rank_state,
                repair,
            )

            run_token_rows_written += written

            print(
                "[PROGRESS] "
                f"query={query_high}->{query_low} "
                f"next_block={repair['next_block']} "
                f"processed_blocks="
                f"{repair['processed_blocks']} "
                f"transfer_logs="
                f"{repair['transfer_logs']} "
                f"applied_transfers="
                f"{repair['applied_transfers']} "
                f"token_rows_written="
                f"{repair['token_rows_written']}"
            )

            query_high = query_low - 1

        integrity = rank_state.integrity_check()

        if integrity != "ok":
            raise RuntimeError(
                "SQLite integrity check failed: "
                f"{integrity}"
            )

        result = {
            "repair_id": args.repair_id,
            "status": repair["status"],
            "from_block": repair["from_block"],
            "to_block": repair["to_block"],
            "next_block": repair["next_block"],
            "run_processed_blocks": (
                run_processed_blocks
            ),
            "run_query_batches": (
                run_query_batches
            ),
            "run_transfer_logs": (
                run_transfer_logs
            ),
            "run_applied_transfers": (
                run_applied_transfers
            ),
            "run_token_rows_written": (
                run_token_rows_written
            ),
            "total_processed_blocks": (
                repair["processed_blocks"]
            ),
            "total_query_batches": (
                repair["query_batches"]
            ),
            "total_transfer_logs": (
                repair["transfer_logs"]
            ),
            "total_applied_transfers": (
                repair["applied_transfers"]
            ),
            "total_token_rows_written": (
                repair["token_rows_written"]
            ),
            "last_processed_block": (
                repair["last_processed_block"]
            ),
            "tracked_token_rows": (
                rank_state
                .official_inception_nft_tokens
                .count()
            ),
            "integrity_check": integrity,
        }

        print(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
            )
        )

    finally:
        rank_state.close()


if __name__ == "__main__":
    main()
