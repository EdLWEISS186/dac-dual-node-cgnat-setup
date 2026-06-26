#!/usr/bin/env python3
"""
WIL v3.7.0 Estimated Current Stake gap repair scanner.

Repairs the block range processed before staking tracking was introduced.
The main WIL synchronization checkpoint is never modified.

The scanner is resumable and stores its own checkpoint in:
    staking_repair_state
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
    DACC_STAKING_CONTRACT,
    DEFAULT_FALLBACK_RPC,
    DEFAULT_PRIMARY_RPC,
    STAKE_FUNCTION_SELECTOR,
    UNSTAKE_FUNCTION_SELECTOR,
    hex_to_int,
    int_to_hex,
    normalize_address,
    normalize_input,
    process_staking_transaction,
    rpc_call,
)
from sqlite_rank_state import SQLiteRankState


DEFAULT_REPAIR_ID = "WIL_V3_3_0_PRE_STAKING_TRACKING_GAP"


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
        CREATE TABLE IF NOT EXISTS staking_repair_state (
            repair_id TEXT PRIMARY KEY,

            from_block INTEGER NOT NULL,
            to_block INTEGER NOT NULL,
            next_block INTEGER NOT NULL,

            status TEXT NOT NULL,

            processed_blocks INTEGER
                NOT NULL DEFAULT 0,

            candidate_transactions INTEGER
                NOT NULL DEFAULT 0,

            staking_events INTEGER
                NOT NULL DEFAULT 0,

            staking_rows_written INTEGER
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
            candidate_transactions,
            staking_events,
            staking_rows_written,
            last_processed_block,
            started_at,
            updated_at,
            completed_at
        FROM staking_repair_state
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
        "candidate_transactions",
        "staking_events",
        "staking_rows_written",
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

    connection.execute(
        """
        INSERT INTO staking_repair_state (
            repair_id,
            from_block,
            to_block,
            next_block,
            status,
            processed_blocks,
            candidate_transactions,
            staking_events,
            staking_rows_written,
            last_processed_block,
            started_at,
            updated_at,
            completed_at
        )
        VALUES (?, ?, ?, ?, ?, 0, 0, 0, 0, NULL, ?, ?, NULL)
        """,
        (
            repair_id,
            from_block,
            to_block,
            from_block,
            "IN_PROGRESS",
            timestamp,
            timestamp,
        ),
    )

    connection.commit()

    state = load_repair_state(
        connection,
        repair_id,
    )

    if state is None:
        raise RuntimeError(
            "Failed to initialize staking repair state"
        )

    return state


def save_repair_batch(
    rank_state: SQLiteRankState,
    repair: Dict[str, Any],
) -> int:
    dirty_before = set(
        rank_state.staking_metrics.dirty_addresses
    )

    last_written_before = (
        rank_state.last_staking_rows_written
    )

    try:
        rank_state.connection.execute(
            "BEGIN IMMEDIATE"
        )

        staking_rows_written = (
            rank_state.staking_metrics.flush()
        )

        repair["staking_rows_written"] = (
            int(repair["staking_rows_written"])
            + staking_rows_written
        )

        rank_state.connection.execute(
            """
            INSERT INTO staking_repair_state (
                repair_id,
                from_block,
                to_block,
                next_block,
                status,
                processed_blocks,
                candidate_transactions,
                staking_events,
                staking_rows_written,
                last_processed_block,
                started_at,
                updated_at,
                completed_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(repair_id) DO UPDATE SET
                from_block = excluded.from_block,
                to_block = excluded.to_block,
                next_block = excluded.next_block,
                status = excluded.status,
                processed_blocks =
                    excluded.processed_blocks,
                candidate_transactions =
                    excluded.candidate_transactions,
                staking_events =
                    excluded.staking_events,
                staking_rows_written =
                    excluded.staking_rows_written,
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
                repair["candidate_transactions"],
                repair["staking_events"],
                repair["staking_rows_written"],
                repair["last_processed_block"],
                repair["started_at"],
                repair["updated_at"],
                repair["completed_at"],
            ),
        )

        rank_state.connection.commit()

        rank_state.last_staking_rows_written = (
            staking_rows_written
        )

        rank_state.staking_metrics.clear_cache()

        return staking_rows_written

    except Exception:
        rank_state.connection.rollback()

        rank_state.staking_metrics.dirty_addresses = (
            dirty_before
        )

        rank_state.last_staking_rows_written = (
            last_written_before
        )

        raise


def is_staking_candidate(
    transaction: Dict[str, Any],
) -> bool:
    destination = normalize_address(
        transaction.get("to")
    )

    if destination != DACC_STAKING_CONTRACT:
        return False

    input_data = normalize_input(
        transaction.get("input")
        or transaction.get("data")
        or "0x"
    )

    return (
        input_data.startswith(
            STAKE_FUNCTION_SELECTOR
        )
        or input_data.startswith(
            UNSTAKE_FUNCTION_SELECTOR
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
        default=500,
        help="Maximum blocks processed in this invocation.",
    )

    parser.add_argument(
        "--commit-every",
        type=int,
        default=100,
        help="Persist progress every N blocks.",
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

    if args.commit_every < 1:
        raise SystemExit(
            "--commit-every must be greater than zero"
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
        else:
            if (
                int(repair["from_block"])
                != args.from_block
                or int(repair["to_block"])
                != args.to_block
            ):
                raise SystemExit(
                    "Existing repair range does not "
                    "match the requested range"
                )

        if repair["status"] == "COMPLETE":
            print(
                "[OK] staking repair is already complete"
            )
            print(
                json.dumps(
                    repair,
                    indent=2,
                    sort_keys=True,
                )
            )
            return

        next_block = int(repair["next_block"])

        if next_block < args.to_block:
            repair["status"] = "COMPLETE"
            repair["completed_at"] = now_utc()
            repair["updated_at"] = now_utc()

            save_repair_batch(
                rank_state,
                repair,
            )

            print(
                "[OK] staking repair marked complete"
            )
            return

        final_block_this_run = max(
            args.to_block,
            next_block - args.max_blocks + 1,
        )

        print(
            "[INFO] WIL v3.7.0 Estimated Current "
            "Stake repair"
        )
        print(f"[INFO] database={database}")
        print(
            f"[INFO] repair_id={args.repair_id}"
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
            f"[INFO] commit_every="
            f"{args.commit_every}"
        )

        blocks_since_commit = 0
        run_processed_blocks = 0
        run_candidates = 0
        run_staking_events = 0
        run_staking_rows_written = 0

        for block_number in range(
            next_block,
            final_block_this_run - 1,
            -1,
        ):
            block = rpc_call(
                rpc_urls,
                "eth_getBlockByNumber",
                [
                    int_to_hex(block_number),
                    True,
                ],
                timeout=45,
            )

            if not block:
                raise RuntimeError(
                    f"Block not returned: {block_number}"
                )

            block_timestamp = now_utc()

            for transaction in (
                block.get("transactions") or []
            ):
                if not is_staking_candidate(
                    transaction
                ):
                    continue

                run_candidates += 1
                repair["candidate_transactions"] = (
                    int(
                        repair[
                            "candidate_transactions"
                        ]
                    )
                    + 1
                )

                transaction_hash = (
                    transaction.get("hash")
                )

                if not transaction_hash:
                    continue

                receipt = rpc_call(
                    rpc_urls,
                    "eth_getTransactionReceipt",
                    [transaction_hash],
                    timeout=45,
                ) or {}

                staking_address = (
                    process_staking_transaction(
                        staking_metrics=(
                            rank_state.staking_metrics
                        ),
                        tx=transaction,
                        receipt=receipt,
                        block_number=block_number,
                        timestamp=block_timestamp,
                    )
                )

                if staking_address:
                    run_staking_events += 1

                    repair["staking_events"] = (
                        int(
                            repair[
                                "staking_events"
                            ]
                        )
                        + 1
                    )

            run_processed_blocks += 1
            blocks_since_commit += 1

            repair["processed_blocks"] = (
                int(repair["processed_blocks"])
                + 1
            )

            repair["last_processed_block"] = (
                block_number
            )

            repair["next_block"] = (
                block_number - 1
            )

            repair["updated_at"] = now_utc()

            if repair["next_block"] < args.to_block:
                repair["status"] = "COMPLETE"
                repair["completed_at"] = now_utc()

            should_commit = (
                blocks_since_commit
                >= args.commit_every
                or block_number
                == final_block_this_run
                or repair["status"] == "COMPLETE"
            )

            if should_commit:
                written = save_repair_batch(
                    rank_state,
                    repair,
                )

                run_staking_rows_written += (
                    written
                )

                blocks_since_commit = 0

                print(
                    "[PROGRESS] "
                    f"last_block={block_number} "
                    f"next_block="
                    f"{repair['next_block']} "
                    f"processed_blocks="
                    f"{repair['processed_blocks']} "
                    f"candidates="
                    f"{repair['candidate_transactions']} "
                    f"staking_events="
                    f"{repair['staking_events']} "
                    f"staking_rows_written="
                    f"{repair['staking_rows_written']}"
                )

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
            "run_candidate_transactions": (
                run_candidates
            ),
            "run_staking_events": (
                run_staking_events
            ),
            "run_staking_rows_written": (
                run_staking_rows_written
            ),
            "total_processed_blocks": (
                repair["processed_blocks"]
            ),
            "total_candidate_transactions": (
                repair["candidate_transactions"]
            ),
            "total_staking_events": (
                repair["staking_events"]
            ),
            "total_staking_rows_written": (
                repair["staking_rows_written"]
            ),
            "last_processed_block": (
                repair["last_processed_block"]
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
