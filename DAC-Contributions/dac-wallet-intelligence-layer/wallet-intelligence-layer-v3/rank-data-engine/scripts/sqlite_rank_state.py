#!/usr/bin/env python3
"""
WIL v3.3.0 SQLite rank-state adapter.

Provides:
- lazy wallet reads
- limited in-memory wallet cache
- dirty-wallet batch UPSERT
- checkpoint/counter/state metadata access
- transactional commits
- consistent SQLite backups
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, Optional


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


class SQLiteWalletMetrics:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.dirty_addresses: set[str] = set()
        self.new_addresses: set[str] = set()
        self._database_count: Optional[int] = None

    @staticmethod
    def normalize(address: str) -> str:
        return str(address).lower()

    def _load(self, address: str) -> Optional[Dict[str, Any]]:
        address = self.normalize(address)

        if address in self.cache:
            return self.cache[address]

        row = self.connection.execute(
            """
            SELECT payload_json
            FROM wallet_metrics
            WHERE address = ?
            """,
            (address,),
        ).fetchone()

        if row is None:
            return None

        wallet = json.loads(row[0])
        self.cache[address] = wallet
        return wallet

    def get(
        self,
        address: str,
        default: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        wallet = self._load(address)

        if wallet is None:
            return default

        # The caller may mutate the returned dictionary.
        self.dirty_addresses.add(self.normalize(address))
        return wallet

    def setdefault(
        self,
        address: str,
        default: Dict[str, Any],
    ) -> Dict[str, Any]:
        address = self.normalize(address)
        wallet = self._load(address)

        if wallet is None:
            wallet = default
            self.cache[address] = wallet
            self.new_addresses.add(address)

        # ensure_wallet mutates the returned dictionary.
        self.dirty_addresses.add(address)
        return wallet

    def __len__(self) -> int:
        if self._database_count is None:
            self._database_count = int(
                self.connection.execute(
                    "SELECT COUNT(*) FROM wallet_metrics"
                ).fetchone()[0]
            )

        return self._database_count + len(self.new_addresses)

    def flush(self) -> int:
        rows = []

        for address in sorted(self.dirty_addresses):
            wallet = self.cache.get(address)

            if wallet is None:
                continue

            rows.append((address, canonical_json(wallet)))

        if rows:
            self.connection.executemany(
                """
                INSERT INTO wallet_metrics(address, payload_json)
                VALUES (?, ?)
                ON CONFLICT(address) DO UPDATE SET
                    payload_json = excluded.payload_json
                """,
                rows,
            )

        written = len(rows)

        if self._database_count is not None:
            self._database_count += len(self.new_addresses)

        self.dirty_addresses.clear()
        self.new_addresses.clear()

        return written

    def clear_cache(self) -> None:
        self.cache.clear()
        self.dirty_addresses.clear()
        self.new_addresses.clear()


class SQLiteRankState:
    def __init__(self, database: Path | str) -> None:
        self.database = Path(database).expanduser().resolve()

        if not self.database.is_file():
            raise FileNotFoundError(
                f"SQLite rank state not found: {self.database}"
            )

        self.connection = sqlite3.connect(
            self.database,
            timeout=60,
        )

        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute("PRAGMA busy_timeout=60000")
        self.connection.execute("PRAGMA temp_store=MEMORY")

        self.wallet_metrics = SQLiteWalletMetrics(self.connection)

    def read_key_value_table(self, table: str) -> Dict[str, Any]:
        allowed = {"checkpoint", "counters", "state_meta"}

        if table not in allowed:
            raise ValueError(f"Unsupported key/value table: {table}")

        return {
            key: json.loads(value_json)
            for key, value_json in self.connection.execute(
                f"SELECT key, value_json FROM {table}"
            )
        }

    def checkpoint(self) -> Dict[str, Any]:
        return self.read_key_value_table("checkpoint")

    def counters(self) -> Dict[str, Any]:
        return self.read_key_value_table("counters")

    def state_meta(self) -> Dict[str, Any]:
        return self.read_key_value_table("state_meta")

    def enrichment_queue(self) -> list[Any]:
        return [
            json.loads(value_json)
            for (value_json,) in self.connection.execute(
                """
                SELECT value_json
                FROM enrichment_queue
                ORDER BY position
                """
            )
        ]

    def _upsert_key_value_table(
        self,
        table: str,
        values: Dict[str, Any],
    ) -> None:
        allowed = {"checkpoint", "counters", "state_meta"}

        if table not in allowed:
            raise ValueError(f"Unsupported key/value table: {table}")

        self.connection.executemany(
            f"""
            INSERT INTO {table}(key, value_json)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value_json = excluded.value_json
            """,
            [
                (key, canonical_json(value))
                for key, value in values.items()
            ],
        )

    def commit_state(
        self,
        checkpoint: Dict[str, Any],
        counters: Dict[str, Any],
        state_meta: Dict[str, Any],
    ) -> int:
        dirty_before = set(
            self.wallet_metrics.dirty_addresses
        )
        new_before = set(
            self.wallet_metrics.new_addresses
        )
        count_before = self.wallet_metrics._database_count

        try:
            self.connection.execute("BEGIN IMMEDIATE")

            wallets_written = self.wallet_metrics.flush()

            self._upsert_key_value_table(
                "checkpoint",
                checkpoint,
            )
            self._upsert_key_value_table(
                "counters",
                counters,
            )
            self._upsert_key_value_table(
                "state_meta",
                state_meta,
            )

            self.connection.commit()
            return wallets_written

        except Exception:
            self.connection.rollback()

            self.wallet_metrics.dirty_addresses = dirty_before
            self.wallet_metrics.new_addresses = new_before
            self.wallet_metrics._database_count = count_before

            raise

    def integrity_check(self) -> str:
        return str(
            self.connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]
        )

    def backup_to(self, destination: Path | str) -> Path:
        destination = Path(destination).expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)

        temporary = destination.with_name(
            f"{destination.name}.tmp.{os.getpid()}"
        )

        if temporary.exists():
            temporary.unlink()

        backup_connection = sqlite3.connect(temporary)

        try:
            self.connection.backup(backup_connection)
            backup_connection.commit()

            integrity = backup_connection.execute(
                "PRAGMA integrity_check"
            ).fetchone()[0]

            if integrity != "ok":
                raise RuntimeError(
                    f"Backup integrity check failed: {integrity}"
                )

        finally:
            backup_connection.close()

        os.replace(temporary, destination)
        os.chmod(destination, 0o600)
        return destination

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> "SQLiteRankState":
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self.close()
