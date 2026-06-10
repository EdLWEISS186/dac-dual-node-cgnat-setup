#!/usr/bin/env python3
"""
WIL v3.3.0 — Streaming JSON State to SQLite Migrator

Preserves:
- wallet_metrics
- checkpoint
- counters
- enrichment_queue
- all remaining top-level state metadata

The source JSON remains unchanged.
The destination is built as a temporary database, validated, and then
atomically renamed into place.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Tuple

import ijson


SCHEMA_VERSION = "WIL_V3_SQLITE_STATE_V1"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def load_non_wallet_state(source: Path) -> dict[str, Any]:
    """
    The current JSON is written with sort_keys=True, so wallet_metrics is
    the final top-level section. Read only the small prefix before that
    section and replace wallet_metrics with an empty object.
    """
    prefix: list[str] = []
    marker_found = False

    with source.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith('  "wallet_metrics": {'):
                prefix.append('  "wallet_metrics": {}\n')
                prefix.append("}\n")
                marker_found = True
                break

            prefix.append(line)

    if not marker_found:
        raise RuntimeError(
            "Could not locate the top-level wallet_metrics section."
        )

    state = json.loads("".join(prefix))
    state.pop("wallet_metrics", None)
    return state


def iter_wallet_metrics(
    source: Path,
) -> Iterator[Tuple[str, dict[str, Any]]]:
    with source.open("rb") as handle:
        yield from ijson.kvitems(
            handle,
            "wallet_metrics",
            use_float=True,
        )


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE state_meta (
            key TEXT PRIMARY KEY,
            value_json TEXT NOT NULL
        );

        CREATE TABLE checkpoint (
            key TEXT PRIMARY KEY,
            value_json TEXT NOT NULL
        );

        CREATE TABLE counters (
            key TEXT PRIMARY KEY,
            value_json TEXT NOT NULL
        );

        CREATE TABLE enrichment_queue (
            position INTEGER PRIMARY KEY,
            value_json TEXT NOT NULL
        );

        CREATE TABLE wallet_metrics (
            address TEXT PRIMARY KEY COLLATE NOCASE,
            payload_json TEXT NOT NULL,

            tx_count INTEGER GENERATED ALWAYS AS (
                CAST(COALESCE(json_extract(payload_json, '$.tx_count'), 0)
                AS INTEGER)
            ) VIRTUAL,

            gas_used_total INTEGER GENERATED ALWAYS AS (
                CAST(COALESCE(
                    json_extract(payload_json, '$.gas_used_total'), 0
                ) AS INTEGER)
            ) VIRTUAL,

            first_seen_block INTEGER GENERATED ALWAYS AS (
                CAST(COALESCE(
                    json_extract(payload_json, '$.first_seen_block'), 0
                ) AS INTEGER)
            ) VIRTUAL,

            last_seen_block INTEGER GENERATED ALWAYS AS (
                CAST(COALESCE(
                    json_extract(payload_json, '$.last_seen_block'), 0
                ) AS INTEGER)
            ) VIRTUAL
        );

        CREATE TABLE migration_info (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )


def migrate(
    source: Path,
    destination: Path,
    batch_size: int,
    overwrite: bool,
) -> None:
    if not source.is_file():
        raise SystemExit(f"Source state not found: {source}")

    if destination.exists() and not overwrite:
        raise SystemExit(
            f"Destination already exists: {destination}\n"
            "Use --overwrite only after confirming the existing database "
            "may be replaced."
        )

    destination.parent.mkdir(parents=True, exist_ok=True)

    temporary = destination.with_name(
        f"{destination.name}.tmp.{os.getpid()}"
    )

    if temporary.exists():
        temporary.unlink()

    print("[INFO] Loading non-wallet state metadata")
    state = load_non_wallet_state(source)

    checkpoint = state.pop("checkpoint", {})
    counters = state.pop("counters", {})
    enrichment_queue = state.pop("enrichment_queue", [])

    expected_wallets = int(
        counters.get("total_indexed_wallets") or 0
    )

    print("[INFO] Creating temporary SQLite database")
    print(f"[INFO] temporary_database={temporary}")

    connection = sqlite3.connect(temporary)

    try:
        connection.execute("PRAGMA journal_mode=DELETE")
        connection.execute("PRAGMA synchronous=NORMAL")
        connection.execute("PRAGMA temp_store=MEMORY")
        connection.execute("PRAGMA cache_size=-65536")
        connection.execute("PRAGMA foreign_keys=ON")

        create_schema(connection)

        connection.executemany(
            "INSERT INTO state_meta(key, value_json) VALUES (?, ?)",
            [
                (key, canonical_json(value))
                for key, value in state.items()
            ],
        )

        connection.executemany(
            "INSERT INTO checkpoint(key, value_json) VALUES (?, ?)",
            [
                (key, canonical_json(value))
                for key, value in checkpoint.items()
            ],
        )

        connection.executemany(
            "INSERT INTO counters(key, value_json) VALUES (?, ?)",
            [
                (key, canonical_json(value))
                for key, value in counters.items()
            ],
        )

        connection.executemany(
            """
            INSERT INTO enrichment_queue(position, value_json)
            VALUES (?, ?)
            """,
            [
                (position, canonical_json(value))
                for position, value in enumerate(enrichment_queue)
            ],
        )

        connection.commit()

        print("[INFO] Streaming wallet_metrics into SQLite")

        inserted = 0
        batch: list[tuple[str, str]] = []
        digest = hashlib.sha256()

        connection.execute("BEGIN")

        for address, record in iter_wallet_metrics(source):
            normalized_address = str(address).lower()
            payload = canonical_json(record)

            batch.append((normalized_address, payload))
            digest.update(normalized_address.encode("utf-8"))
            digest.update(b"\0")
            digest.update(payload.encode("utf-8"))
            digest.update(b"\n")

            if len(batch) >= batch_size:
                connection.executemany(
                    """
                    INSERT INTO wallet_metrics(address, payload_json)
                    VALUES (?, ?)
                    """,
                    batch,
                )

                inserted += len(batch)
                batch.clear()
                connection.commit()
                connection.execute("BEGIN")

                if inserted % 10000 == 0:
                    print(f"[PROGRESS] wallets_inserted={inserted}")

        if batch:
            connection.executemany(
                """
                INSERT INTO wallet_metrics(address, payload_json)
                VALUES (?, ?)
                """,
                batch,
            )
            inserted += len(batch)

        connection.commit()

        actual_wallets = int(
            connection.execute(
                "SELECT COUNT(*) FROM wallet_metrics"
            ).fetchone()[0]
        )

        actual_queue = int(
            connection.execute(
                "SELECT COUNT(*) FROM enrichment_queue"
            ).fetchone()[0]
        )

        migration_values = {
            "schema_version": SCHEMA_VERSION,
            "created_at": now_utc(),
            "source_path": str(source),
            "source_size_bytes": str(source.stat().st_size),
            "expected_wallets": str(expected_wallets),
            "inserted_wallets": str(inserted),
            "actual_wallet_rows": str(actual_wallets),
            "enrichment_queue_rows": str(actual_queue),
            "wallet_payload_digest_sha256": digest.hexdigest(),
        }

        connection.executemany(
            "INSERT INTO migration_info(key, value) VALUES (?, ?)",
            migration_values.items(),
        )
        connection.commit()

        integrity = connection.execute(
            "PRAGMA integrity_check"
        ).fetchone()[0]

        if integrity != "ok":
            raise RuntimeError(
                f"SQLite integrity check failed: {integrity}"
            )

        if inserted != actual_wallets:
            raise RuntimeError(
                "Inserted wallet count does not match SQLite row count: "
                f"{inserted} != {actual_wallets}"
            )

        if expected_wallets and actual_wallets != expected_wallets:
            raise RuntimeError(
                "SQLite wallet count does not match source counters: "
                f"{actual_wallets} != {expected_wallets}"
            )

        if actual_queue != len(enrichment_queue):
            raise RuntimeError(
                "Enrichment queue count mismatch: "
                f"{actual_queue} != {len(enrichment_queue)}"
            )

        print("[OK] SQLite integrity_check: ok")
        print(f"[OK] wallet_rows={actual_wallets}")
        print(f"[OK] enrichment_queue_rows={actual_queue}")
        print(
            "[OK] wallet_payload_digest_sha256="
            f"{digest.hexdigest()}"
        )

    except Exception:
        connection.close()

        if temporary.exists():
            temporary.unlink()

        raise

    connection.close()

    if destination.exists():
        destination.unlink()

    os.replace(temporary, destination)
    os.chmod(destination, 0o600)

    print("[OK] Migration complete")
    print(f"[OK] sqlite_database={destination}")
    print(f"[OK] sqlite_size_bytes={destination.stat().st_size}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.batch_size < 1:
        raise SystemExit("--batch-size must be greater than zero")

    migrate(
        source=args.source.expanduser().resolve(),
        destination=args.destination.expanduser().resolve(),
        batch_size=args.batch_size,
        overwrite=args.overwrite,
    )


if __name__ == "__main__":
    main()
