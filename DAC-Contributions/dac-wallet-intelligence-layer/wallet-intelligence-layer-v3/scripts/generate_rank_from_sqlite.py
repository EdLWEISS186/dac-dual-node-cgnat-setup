#!/usr/bin/env python3
"""
WIL v3.7.0 — SQLite Global Rank Publisher

Reads the complete SQLite wallet population, calculates all comparative
ranks globally with SQLite window functions, and emits compact browser
lookup shards.

The source SQLite database is never modified.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Iterable


VERSION = "v3.7.0"
CHAIN_ID = 21894
NETWORK = "DAC Testnet"
NATIVE_TOKEN = "DACC"

COMPACT_SCHEMA = "WIL_V3_COMPACT_ARRAY_V3"
INDEX_MODE = "SHARDED_COMPACT_V3"
SHARD_PREFIX_LENGTH = 2

SMALL_METRIC_ORDER = [
    "native_funds",
    "estimated_stake_before_conviction",
    "transactions",
    "native_volume",
    "gas_used",
    "nft_holdings",
    "collection_diversity",
    "reputation_score",
    "low_sybil_risk",
]

OFFICIAL_SIGNAL_KEY = "official_inception_nfts"
CONVICTION_SIGNAL_KEY = "conviction_locked"
CONVICTION_CONTRACT = "0xfc416635e3b7330404766bd8ea9e5227800937c1"
CONVICTION_CUTOVER_BLOCK = 15021664
CONVICTION_CUTOVER_UTC = "2026-06-16T07:50:29Z"
CONVICTION_CUTOVER_LOCAL = "2026-06-16 14:50:29 +07:00"

METRIC_ORDER = (
    SMALL_METRIC_ORDER
    + [OFFICIAL_SIGNAL_KEY]
)

# Final Composite Rank tetap menggunakan delapan
# variabel lama. Estimated Stake dan Official NFT
# tidak memengaruhi Overall Wallet Rank.
COMPOSITE_METRIC_ORDER = [
    "native_funds",
    "transactions",
    "gas_used",
    "native_volume",
    "nft_holdings",
    "collection_diversity",
    "reputation_score",
    "low_sybil_risk",
]

RANK_ORDER = METRIC_ORDER + ["overall_rank"]

OFFICIAL_INCEPTION_NFT_CONTRACT = (
    "0xb36ab4c2bd6acfc36e9d6c53f39f4301901bd647"
)

OFFICIAL_RANK_TIERS = [
    [13, "CROWN"],
    [12, "CIPHER"],
    [11, "PHANTOM"],
    [10, "INTERCEPTOR"],
    [9, "ARCHITECT"],
    [8, "WARRIOR"],
    [7, "SOVEREIGN"],
    [6, "SENTINEL"],
    [5, "VANGUARD"],
    [4, "SHADOW UNIT"],
    [3, "SEAL"],
    [2, "COMMANDO"],
    [1, "CADET"],
    [0, "NONE"],
]


def now_utc() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def read_key_value_table(
    connection: sqlite3.Connection,
    table: str,
) -> Dict[str, Any]:
    return {
        key: json.loads(value_json)
        for key, value_json in connection.execute(
            f"SELECT key, value_json FROM {table}"
        )
    }


def to_int(value: Any) -> int:
    if value is None:
        return 0

    raw = str(value).strip()

    if not raw:
        return 0

    if raw.startswith("0x"):
        try:
            return int(raw, 16)
        except ValueError:
            return 0

    try:
        return int(Decimal(raw))
    except Exception:
        return 0


def integer_string(value: Any) -> str:
    return str(max(to_int(value), 0))


def wei_to_native_string(value: Any) -> str:
    amount = Decimal(str(value or "0")) / Decimal(10**18)
    normalized = amount.normalize()

    if normalized == normalized.to_integral_value():
        return str(int(normalized))

    return format(normalized, "f")


def calculate_reputation_score(record: Dict[str, Any]) -> int:
    tx_count = record["transactions"]
    gas_used = record["gas_used"]
    native_balance = record["native_balance_wei"]
    native_volume = record["native_volume_wei"]
    nft_holdings = record["nft_holdings"]
    collection_diversity = record["collection_diversity"]
    successful_tx = record["successful_tx_count"]
    failed_tx = record["failed_tx_count"]
    unique_counterparties = record["unique_counterparty_count"]
    contract_interactions = record["contract_interaction_count"]

    score = 0

    score += min(tx_count, 100)
    score += min(gas_used // 21000, 100)
    score += min(native_volume // 10**15, 100)
    score += min(native_balance // 10**15, 100)
    score += min(nft_holdings * 2, 100)
    score += min(collection_diversity * 5, 100)
    score += min(unique_counterparties * 3, 100)
    score += min(contract_interactions * 2, 100)

    if successful_tx + failed_tx > 0:
        success_ratio = (
            Decimal(successful_tx)
            / Decimal(successful_tx + failed_tx)
        )
        score += int(success_ratio * Decimal(100))

    return int(score)


def calculate_low_sybil_risk_score(
    record: Dict[str, Any],
) -> int:
    tx_count = record["transactions"]
    native_balance = record["native_balance_wei"]
    native_volume = record["native_volume_wei"]
    nft_holdings = record["nft_holdings"]
    collection_diversity = record["collection_diversity"]
    successful_tx = record["successful_tx_count"]
    failed_tx = record["failed_tx_count"]
    unique_counterparties = record["unique_counterparty_count"]

    score = 0

    score += min(tx_count * 2, 120)
    score += min(unique_counterparties * 5, 120)
    score += min(native_balance // 10**15, 120)
    score += min(native_volume // 10**15, 120)
    score += min(nft_holdings * 2, 80)
    score += min(collection_diversity * 8, 80)

    if failed_tx > successful_tx and failed_tx > 0:
        score -= min(failed_tx * 5, 80)

    if (
        tx_count <= 1
        and native_balance == 0
        and nft_holdings == 0
    ):
        score -= 80

    return max(int(score), 0)


def write_json(
    path: Path,
    payload: Any,
    *,
    compact: bool,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_name(
        f"{path.name}.tmp.{os.getpid()}"
    )

    if compact:
        body = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    else:
        body = json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )

    temporary.write_text(
        body + "\n",
        encoding="utf-8",
    )

    os.replace(temporary, path)


def create_consistent_snapshot(
    source_database: Path,
    snapshot_database: Path,
) -> None:
    source = sqlite3.connect(source_database)
    snapshot = sqlite3.connect(snapshot_database)

    try:
        source.backup(
            snapshot,
            pages=4096,
            sleep=0.05,
        )
        snapshot.commit()

        integrity = snapshot.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        if integrity != "ok":
            raise RuntimeError(
                f"SQLite snapshot integrity check failed: "
                f"{integrity}"
            )

    finally:
        snapshot.close()
        source.close()


def create_build_schema(
    connection: sqlite3.Connection,
) -> None:
    connection.executescript(
        """
        CREATE TABLE rank_records (
            address TEXT PRIMARY KEY,
            prefix TEXT NOT NULL,

            native_balance_wei TEXT NOT NULL,
            estimated_stake_before_conviction_wei TEXT NOT NULL,
            conviction_locked_wei TEXT NOT NULL,
            transactions INTEGER NOT NULL,
            native_volume_wei TEXT NOT NULL,
            gas_used TEXT NOT NULL,
            nft_holdings INTEGER NOT NULL,
            collection_diversity INTEGER NOT NULL,
            reputation_score INTEGER NOT NULL,
            low_sybil_risk INTEGER NOT NULL,
            official_inception_nfts INTEGER NOT NULL
        );

        CREATE INDEX rank_records_prefix_address
        ON rank_records(prefix, address);
        """
    )


def iter_source_wallets(
    connection: sqlite3.Connection,
    limit: int | None,
) -> Iterable[tuple[str, str, str, int]]:
    query = """
        WITH official_owner_counts AS (
            SELECT
                owner_address AS address,
                COUNT(*) AS official_inception_nfts
            FROM official_inception_nft_tokens
            WHERE owner_address IS NOT NULL
            GROUP BY owner_address
        )
        SELECT
            wallet.address,
            wallet.payload_json,
            COALESCE(
                staking.estimated_current_stake_wei,
                '0'
            ) AS estimated_stake_before_conviction_wei,
            COALESCE(
                conviction.conviction_locked_wei,
                '0'
            ) AS conviction_locked_wei,
            COALESCE(
                official.official_inception_nfts,
                0
            ) AS official_inception_nfts
        FROM wallet_metrics AS wallet
        LEFT JOIN staking_metrics AS staking
            ON staking.address = wallet.address
        LEFT JOIN conviction_metrics AS conviction
            ON conviction.address = wallet.address
        LEFT JOIN official_owner_counts AS official
            ON official.address = wallet.address
        ORDER BY wallet.address
    """

    parameters: tuple[Any, ...] = ()

    if limit is not None:
        query += " LIMIT ?"
        parameters = (limit,)

    yield from connection.execute(query, parameters)


def insert_rank_records(
    source: sqlite3.Connection,
    build: sqlite3.Connection,
    limit: int | None,
    batch_size: int,
) -> int:
    batch: list[tuple[Any, ...]] = []
    inserted = 0

    insert_sql = """
        INSERT INTO rank_records (
            address,
            prefix,
            native_balance_wei,
            estimated_stake_before_conviction_wei,
            conviction_locked_wei,
            transactions,
            native_volume_wei,
            gas_used,
            nft_holdings,
            collection_diversity,
            reputation_score,
            low_sybil_risk,
            official_inception_nfts
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    build.execute("BEGIN")

    for (
        address,
        payload_json,
        estimated_stake_before_conviction_wei,
        conviction_locked_wei,
        official_inception_nfts,
    ) in iter_source_wallets(
        source,
        limit,
    ):
        metrics = json.loads(payload_json)

        normalized_address = str(address).lower()
        prefix = normalized_address[2:4]

        nft_collections = (
            metrics.get(
                "nft_collection_contract_addresses"
            )
            or []
        )

        record = {
            "native_balance_wei": to_int(
                metrics.get("native_balance_wei")
            ),
            "estimated_stake_before_conviction_wei": to_int(
                estimated_stake_before_conviction_wei
            ),
            "conviction_locked_wei": to_int(
                conviction_locked_wei
            ),
            "transactions": to_int(
                metrics.get("tx_count")
            ),
            "native_volume_wei": to_int(
                metrics.get("native_volume_wei")
            ),
            "gas_used": to_int(
                metrics.get(
                    "gas_used_total",
                    metrics.get("gas_used"),
                )
            ),
            "nft_holdings": to_int(
                metrics.get("nft_holdings_count")
            ),
            "collection_diversity": len(
                set(nft_collections)
            ),
            "successful_tx_count": to_int(
                metrics.get("successful_tx_count")
            ),
            "failed_tx_count": to_int(
                metrics.get("failed_tx_count")
            ),
            "unique_counterparty_count": to_int(
                metrics.get(
                    "unique_counterparty_count"
                )
            ),
            "contract_interaction_count": to_int(
                metrics.get(
                    "contract_interaction_count"
                )
            ),
            "official_inception_nfts": to_int(
                official_inception_nfts
            ),
        }

        reputation_score = (
            calculate_reputation_score(record)
        )

        low_sybil_risk = (
            calculate_low_sybil_risk_score(record)
        )

        batch.append(
            (
                normalized_address,
                prefix,
                integer_string(
                    record["native_balance_wei"]
                ),
                integer_string(
                    record[
                        "estimated_stake_before_conviction_wei"
                    ]
                ),
                integer_string(
                    record[
                        "conviction_locked_wei"
                    ]
                ),
                record["transactions"],
                integer_string(
                    record["native_volume_wei"]
                ),
                integer_string(record["gas_used"]),
                record["nft_holdings"],
                record["collection_diversity"],
                reputation_score,
                low_sybil_risk,
                record["official_inception_nfts"],
            )
        )

        if len(batch) >= batch_size:
            build.executemany(insert_sql, batch)

            inserted += len(batch)
            batch.clear()

            build.commit()
            build.execute("BEGIN")

            if inserted % 10000 == 0:
                print(
                    f"[PROGRESS] rank_records="
                    f"{inserted}"
                )

    if batch:
        build.executemany(insert_sql, batch)
        inserted += len(batch)

    build.commit()
    return inserted


def calculate_global_ranks(
    connection: sqlite3.Connection,
) -> None:
    print(
        "[INFO] Calculating ten small-card ranks "
        "and Official Rank Signal"
    )

    connection.executescript(
        """
        DROP TABLE IF EXISTS ranked_metrics;

        CREATE TABLE ranked_metrics AS
        SELECT
            address,
            prefix,
            native_balance_wei,
            estimated_stake_before_conviction_wei,
            conviction_locked_wei,
            transactions,
            native_volume_wei,
            gas_used,
            nft_holdings,
            collection_diversity,
            reputation_score,
            low_sybil_risk,
            official_inception_nfts,

            ROW_NUMBER() OVER (
                ORDER BY
                    length(native_balance_wei) DESC,
                    native_balance_wei DESC,
                    address ASC
            ) AS rank_native_funds,

            ROW_NUMBER() OVER (
                ORDER BY
                    length(
                        estimated_stake_before_conviction_wei
                    ) DESC,
                    estimated_stake_before_conviction_wei DESC,
                    address ASC
            ) AS rank_estimated_stake_before_conviction,

            ROW_NUMBER() OVER (
                ORDER BY
                    length(
                        conviction_locked_wei
                    ) DESC,
                    conviction_locked_wei DESC,
                    address ASC
            ) AS rank_conviction_locked,

            ROW_NUMBER() OVER (
                ORDER BY
                    transactions DESC,
                    address ASC
            ) AS rank_transactions,

            ROW_NUMBER() OVER (
                ORDER BY
                    length(native_volume_wei) DESC,
                    native_volume_wei DESC,
                    address ASC
            ) AS rank_native_volume,

            ROW_NUMBER() OVER (
                ORDER BY
                    length(gas_used) DESC,
                    gas_used DESC,
                    address ASC
            ) AS rank_gas_used,

            ROW_NUMBER() OVER (
                ORDER BY
                    nft_holdings DESC,
                    address ASC
            ) AS rank_nft_holdings,

            ROW_NUMBER() OVER (
                ORDER BY
                    collection_diversity DESC,
                    address ASC
            ) AS rank_collection_diversity,

            ROW_NUMBER() OVER (
                ORDER BY
                    reputation_score DESC,
                    address ASC
            ) AS rank_reputation_score,

            ROW_NUMBER() OVER (
                ORDER BY
                    low_sybil_risk DESC,
                    address ASC
            ) AS rank_low_sybil_risk,

            ROW_NUMBER() OVER (
                ORDER BY
                    official_inception_nfts DESC,
                    address ASC
            ) AS rank_official_inception_nfts

        FROM rank_records;

        CREATE INDEX ranked_metrics_prefix_address
        ON ranked_metrics(prefix, address);
        """
    )

    print("[INFO] Calculating global composite rank")

    connection.executescript(
        """
        DROP TABLE IF EXISTS final_ranked;

        CREATE TABLE final_ranked AS
        SELECT
            *,

            ROW_NUMBER() OVER (
                ORDER BY
                    (
                        rank_native_funds
                        + rank_transactions
                        + rank_gas_used
                        + rank_native_volume
                        + rank_nft_holdings
                        + rank_collection_diversity
                        + rank_reputation_score
                        + rank_low_sybil_risk
                    ) ASC,
                    address ASC
            ) AS rank_overall

        FROM ranked_metrics;

        CREATE INDEX final_ranked_prefix_address
        ON final_ranked(prefix, address);
        """
    )

    connection.commit()


def write_compact_shards(
    connection: sqlite3.Connection,
    output_directory: Path,
) -> tuple[int, int]:
    shards_directory = (
        output_directory
        / f".rank-shards.tmp.{os.getpid()}"
    )

    if shards_directory.exists():
        shutil.rmtree(shards_directory)

    shards_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    prefixes = [
        prefix
        for (prefix,) in connection.execute(
            """
            SELECT DISTINCT prefix
            FROM final_ranked
            ORDER BY prefix
            """
        )
    ]

    total_rows = 0

    query = """
        SELECT
            address,
            native_balance_wei,
            estimated_stake_before_conviction_wei,
            conviction_locked_wei,
            transactions,
            native_volume_wei,
            gas_used,
            nft_holdings,
            collection_diversity,
            reputation_score,
            low_sybil_risk,
            official_inception_nfts,
            rank_native_funds,
            rank_estimated_stake_before_conviction,
            rank_conviction_locked,
            rank_transactions,
            rank_native_volume,
            rank_gas_used,
            rank_nft_holdings,
            rank_collection_diversity,
            rank_reputation_score,
            rank_low_sybil_risk,
            rank_official_inception_nfts,
            rank_overall
        FROM final_ranked
        WHERE prefix = ?
        ORDER BY address
    """

    for prefix in prefixes:
        payload: Dict[str, list[Any]] = {}

        for row in connection.execute(
            query,
            (prefix,),
        ):
            (
                address,
                native_balance_wei,
                estimated_stake_before_conviction_wei,
                conviction_locked_wei,
                transactions,
                native_volume_wei,
                gas_used,
                nft_holdings,
                collection_diversity,
                reputation_score,
                low_sybil_risk,
                official_inception_nfts,
                rank_native_funds,
                rank_estimated_stake_before_conviction,
                rank_conviction_locked,
                rank_transactions,
                rank_native_volume,
                rank_gas_used,
                rank_nft_holdings,
                rank_collection_diversity,
                rank_reputation_score,
                rank_low_sybil_risk,
                rank_official_inception_nfts,
                rank_overall,
            ) = row

            payload[address] = [
                wei_to_native_string(
                    native_balance_wei
                ),
                wei_to_native_string(
                    estimated_stake_before_conviction_wei
                ),
                wei_to_native_string(
                    conviction_locked_wei
                ),
                int(transactions),
                wei_to_native_string(
                    native_volume_wei
                ),
                int(gas_used),
                int(nft_holdings),
                int(collection_diversity),
                int(reputation_score),
                int(low_sybil_risk),
                int(official_inception_nfts),

                int(rank_native_funds),
                int(rank_estimated_stake_before_conviction),
                int(rank_conviction_locked),
                int(rank_transactions),
                int(rank_native_volume),
                int(rank_gas_used),
                int(rank_nft_holdings),
                int(rank_collection_diversity),
                int(rank_reputation_score),
                int(rank_low_sybil_risk),
                int(rank_official_inception_nfts),
                int(rank_overall),
            ]

        write_json(
            shards_directory / f"{prefix}.json",
            payload,
            compact=True,
        )

        total_rows += len(payload)

    final_shards_directory = (
        output_directory / "rank-shards"
    )

    if final_shards_directory.exists():
        shutil.rmtree(final_shards_directory)

    os.replace(
        shards_directory,
        final_shards_directory,
    )

    return len(prefixes), total_rows


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--state-db",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root() / "data",
    )

    parser.add_argument(
        "--work-root",
        type=Path,
        default=Path.home()
        / "wil-v3-rank-state"
        / "rank-publisher-work",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Test-only wallet limit.",
    )

    parser.add_argument(
        "--allow-incomplete",
        action="store_true",
        help=(
            "Allow a test build before the chain state "
            "is fully publish-ready."
        ),
    )

    parser.add_argument(
        "--keep-work",
        action="store_true",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
    )

    args = parser.parse_args()

    source_database = (
        args.state_db
        .expanduser()
        .resolve()
    )

    output_directory = (
        args.output_dir
        .expanduser()
        .resolve()
    )

    work_root = (
        args.work_root
        .expanduser()
        .resolve()
    )

    if not source_database.is_file():
        raise SystemExit(
            f"SQLite state not found: "
            f"{source_database}"
        )

    if args.limit is not None and args.limit < 1:
        raise SystemExit(
            "--limit must be greater than zero"
        )

    if args.batch_size < 1:
        raise SystemExit(
            "--batch-size must be greater than zero"
        )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    work_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    work_directory = Path(
        tempfile.mkdtemp(
            prefix="wil-v3-rank-publish.",
            dir=work_root,
        )
    )

    snapshot_database = (
        work_directory
        / "source-snapshot.sqlite"
    )

    build_database = (
        work_directory
        / "rank-build.sqlite"
    )

    print(
        "[INFO] WIL v3.7.0 SQLite global rank "
        "publisher"
    )
    print(f"[INFO] state_db={source_database}")
    print(f"[INFO] output_dir={output_directory}")
    print(f"[INFO] work_dir={work_directory}")
    print(f"[INFO] limit={args.limit}")

    try:
        print(
            "[INFO] Creating consistent source "
            "SQLite snapshot"
        )

        create_consistent_snapshot(
            source_database,
            snapshot_database,
        )

        print(
            "[OK] source snapshot "
            "integrity_check: ok"
        )

        source = sqlite3.connect(
            f"file:{snapshot_database}?mode=ro",
            uri=True,
        )

        checkpoint = read_key_value_table(
            source,
            "checkpoint",
        )

        counters = read_key_value_table(
            source,
            "counters",
        )

        sync_phase = checkpoint.get("sync_phase")
        historical_complete = (
            checkpoint.get(
                "historical_backfill_complete"
            )
            is True
        )
        catch_up_status = checkpoint.get(
            "catch_up_status"
        )

        publish_ready = (
            (
                sync_phase == "INCREMENTAL"
                and historical_complete
                and catch_up_status
                in ("CAUGHT_UP", None)
            )
            or
            (
                sync_phase == "FINALIZED"
                and checkpoint.get("final_snapshot_ready") is True
            )
        )

        if not publish_ready and not args.allow_incomplete:
            source.close()

            raise SystemExit(
                "SQLite state is not publish-ready. "
                "Use --allow-incomplete only for a "
                "local test build."
            )

        source_wallet_count = int(
            source.execute(
                "SELECT COUNT(*) "
                "FROM wallet_metrics"
            ).fetchone()[0]
        )

        expected_wallet_count = int(
            counters.get(
                "total_indexed_wallets"
            )
            or 0
        )

        if (
            args.limit is None
            and expected_wallet_count
            and source_wallet_count
            != expected_wallet_count
        ):
            source.close()

            raise RuntimeError(
                "Source wallet row count does not "
                "match counters: "
                f"{source_wallet_count} != "
                f"{expected_wallet_count}"
            )

        build = sqlite3.connect(
            build_database,
        )

        build.execute(
            "PRAGMA journal_mode=OFF"
        )
        build.execute(
            "PRAGMA synchronous=OFF"
        )
        build.execute(
            "PRAGMA temp_store=FILE"
        )
        build.execute(
            "PRAGMA cache_size=-65536"
        )
        build.execute(
            "PRAGMA mmap_size=268435456"
        )

        create_build_schema(build)

        print(
            "[INFO] Streaming wallet metrics "
            "into rank build database"
        )

        ranked_wallets = insert_rank_records(
            source,
            build,
            args.limit,
            args.batch_size,
        )

        source.close()

        print(
            f"[OK] rank_records={ranked_wallets}"
        )

        calculate_global_ranks(build)

        print(
            "[INFO] Writing compact rank shards"
        )

        shard_count, shard_rows = (
            write_compact_shards(
                build,
                output_directory,
            )
        )

        build_integrity = build.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        if build_integrity != "ok":
            raise RuntimeError(
                "Rank build SQLite integrity "
                f"check failed: {build_integrity}"
            )

        if shard_rows != ranked_wallets:
            raise RuntimeError(
                "Shard row count does not match "
                "ranked wallet count: "
                f"{shard_rows} != "
                f"{ranked_wallets}"
            )

        build.close()

        generated_at = now_utc()

        valid_public_index = (
            publish_ready
            and args.limit is None
        )

        summary = {
            "schema": "WIL_V3_RANK_SUMMARY",
            "version": VERSION,
            "project": (
                "Wallet Intelligence Layer "
                "v3.7.0"
            ),
            "feature": (
                "Wallet Rank Intelligence"
            ),
            "network": NETWORK,
            "chain_id": CHAIN_ID,
            "native_token": NATIVE_TOKEN,
            "status": (
                "READY"
                if valid_public_index
                else
                "TEST_ONLY_INCOMPLETE_RANK_BUILD"
            ),
            "has_valid_rank_index": (
                valid_public_index
            ),
            "rank_lookup_enabled": (
                valid_public_index
            ),
            "generated_at": generated_at,
            "state_backend": "SQLITE",
            "rank_data_source": (
                "LOCAL_SQLITE_GLOBAL_POPULATION"
            ),
            "rank_model": (
                "wallet-rank-intelligence-"
                "v3.7.0-sqlite-global"
            ),
            "total_ranked_wallets": (
                ranked_wallets
            ),
            "total_indexed_wallets": (
                expected_wallet_count
                or source_wallet_count
            ),
            "total_processed_transactions": (
                int(
                    counters.get(
                        "total_processed_transactions"
                    )
                    or 0
                )
            ),
            "ranking_variables": RANK_ORDER,
            "small_metric_order": SMALL_METRIC_ORDER,
            "composite_ranking_variables": (
                COMPOSITE_METRIC_ORDER
            ),
            "official_rank_signal": {
                "key": OFFICIAL_SIGNAL_KEY,
                "label": (
                    "Official Testnet Inception NFTs"
                ),
                "contract": (
                    OFFICIAL_INCEPTION_NFT_CONTRACT
                ),
                "rank_tiers": OFFICIAL_RANK_TIERS,
            },
            "pending_ranking_variables": [],
            "compact_record_schema": (
                COMPACT_SCHEMA
            ),
            "rank_shards": {
                "mode": INDEX_MODE,
                "directory": (
                    "data/rank-shards"
                ),
                "prefix_length": (
                    SHARD_PREFIX_LENGTH
                ),
                "shard_count": shard_count,
                "row_count": shard_rows,
            },
            "sync_status": {
                "phase": sync_phase,
                "historical_backfill_complete": (
                    historical_complete
                ),
                "catch_up_status": (
                    catch_up_status
                ),
                "backfill_status": (
                    checkpoint.get(
                        "backfill_status"
                    )
                ),
                "last_sync_at": (
                    checkpoint.get(
                        "last_sync_at"
                    )
                ),
                "last_synced_block": (
                    checkpoint.get(
                        "last_synced_block"
                    )
                ),
                "incremental_next_block": (
                    checkpoint.get(
                        "incremental_next_block"
                    )
                ),
            },
        }

        index = {
            "schema": "WIL_V3_RANK_INDEX",
            "version": VERSION,
            "status": (
                "READY"
                if valid_public_index
                else
                "TEST_ONLY"
            ),
            "mode": INDEX_MODE,
            "directory": "data/rank-shards",
            "has_valid_rank_index": (
                valid_public_index
            ),
            "record_schema": COMPACT_SCHEMA,
            "metric_order": METRIC_ORDER,
            "small_metric_order": SMALL_METRIC_ORDER,
            "rank_order": RANK_ORDER,
            "composite_metric_order": (
                COMPOSITE_METRIC_ORDER
            ),
            "official_signal_key": (
                OFFICIAL_SIGNAL_KEY
            ),
            "official_rank_tiers": (
                OFFICIAL_RANK_TIERS
            ),
            "available_rank_variables": (
                RANK_ORDER
            ),
            "pending_rank_variables": [],
            "total_ranked_wallets": (
                ranked_wallets
            ),
            "generated_at": generated_at,
        }

        write_json(
            output_directory
            / "wallet-rank-summary.json",
            summary,
            compact=False,
        )

        write_json(
            output_directory
            / "wallet-rank-index.json",
            index,
            compact=False,
        )

        print(
            "[OK] rank build SQLite "
            "integrity_check: ok"
        )
        print(
            f"[OK] ranked_wallets="
            f"{ranked_wallets}"
        )
        print(
            f"[OK] shard_count="
            f"{shard_count}"
        )
        print(
            f"[OK] shard_rows="
            f"{shard_rows}"
        )
        print(
            f"[OK] valid_public_index="
            f"{valid_public_index}"
        )
        print(
            f"[OK] summary="
            f"{output_directory / 'wallet-rank-summary.json'}"
        )
        print(
            f"[OK] index="
            f"{output_directory / 'wallet-rank-index.json'}"
        )

    finally:
        if args.keep_work:
            print(
                f"[INFO] Keeping build work: "
                f"{work_directory}"
            )
        else:
            shutil.rmtree(
                work_directory,
                ignore_errors=True,
            )


if __name__ == "__main__":
    main()
