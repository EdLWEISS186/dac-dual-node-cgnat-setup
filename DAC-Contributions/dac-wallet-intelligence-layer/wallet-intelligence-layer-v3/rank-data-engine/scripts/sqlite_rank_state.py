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


class SQLiteStakingMetrics:
    """
    Lazy, rollback-safe current staking state.

    Estimated Current Stake is derived from observed stake/unstake flow.
    A direct balanceOf(address) result may be stored separately as a
    cross-check without replacing the primary flow-derived estimate.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.dirty_addresses: set[str] = set()

    @staticmethod
    def normalize(address: str) -> str:
        return str(address).lower()

    @staticmethod
    def default_record(address: str) -> Dict[str, Any]:
        return {
            "address": str(address).lower(),
            "estimated_current_stake_wei": "0",
            "stake_in_wei": "0",
            "unstake_out_wei": "0",
            "direct_contract_balance_wei": None,
            "stake_tx_count": 0,
            "unstake_tx_count": 0,
            "flow_tx_count": 0,
            "source": "NO_STAKE_FLOW",
            "confidence": "LOW",
            "last_event_block": None,
            "last_event_tx_hash": None,
            "last_refreshed_block": None,
            "updated_at": "",
        }

    def _load(self, address: str) -> Optional[Dict[str, Any]]:
        address = self.normalize(address)

        if address in self.cache:
            return self.cache[address]

        row = self.connection.execute(
            """
            SELECT
                estimated_current_stake_wei,
                stake_in_wei,
                unstake_out_wei,
                direct_contract_balance_wei,
                stake_tx_count,
                unstake_tx_count,
                flow_tx_count,
                source,
                confidence,
                last_event_block,
                last_event_tx_hash,
                last_refreshed_block,
                updated_at
            FROM staking_metrics
            WHERE address = ?
            """,
            (address,),
        ).fetchone()

        if row is None:
            return None

        record = {
            "address": address,
            "estimated_current_stake_wei": str(row[0] or "0"),
            "stake_in_wei": str(row[1] or "0"),
            "unstake_out_wei": str(row[2] or "0"),
            "direct_contract_balance_wei": (
                None if row[3] is None else str(row[3])
            ),
            "stake_tx_count": int(row[4] or 0),
            "unstake_tx_count": int(row[5] or 0),
            "flow_tx_count": int(row[6] or 0),
            "source": str(row[7] or "NO_STAKE_FLOW"),
            "confidence": str(row[8] or "LOW"),
            "last_event_block": row[9],
            "last_event_tx_hash": row[10],
            "last_refreshed_block": row[11],
            "updated_at": str(row[12] or ""),
        }

        self.cache[address] = record
        return record

    def get(
        self,
        address: str,
        default: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        record = self._load(address)

        if record is None:
            return default

        self.dirty_addresses.add(self.normalize(address))
        return record

    def setdefault(
        self,
        address: str,
        default: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        address = self.normalize(address)
        record = self._load(address)

        if record is None:
            record = (
                default
                if default is not None
                else self.default_record(address)
            )
            record["address"] = address
            self.cache[address] = record

        self.dirty_addresses.add(address)
        return record

    def count(self) -> int:
        return int(
            self.connection.execute(
                "SELECT COUNT(*) FROM staking_metrics"
            ).fetchone()[0]
        )

    def flush(self) -> int:
        rows = []

        for address in sorted(self.dirty_addresses):
            record = self.cache.get(address)

            if record is None:
                continue

            rows.append(
                (
                    address,
                    str(
                        record.get(
                            "estimated_current_stake_wei",
                            "0",
                        )
                        or "0"
                    ),
                    str(record.get("stake_in_wei", "0") or "0"),
                    str(record.get("unstake_out_wei", "0") or "0"),
                    (
                        None
                        if record.get(
                            "direct_contract_balance_wei"
                        )
                        is None
                        else str(
                            record.get(
                                "direct_contract_balance_wei"
                            )
                        )
                    ),
                    int(record.get("stake_tx_count") or 0),
                    int(record.get("unstake_tx_count") or 0),
                    int(record.get("flow_tx_count") or 0),
                    str(
                        record.get("source")
                        or "NO_STAKE_FLOW"
                    ),
                    str(record.get("confidence") or "LOW"),
                    record.get("last_event_block"),
                    record.get("last_event_tx_hash"),
                    record.get("last_refreshed_block"),
                    str(record.get("updated_at") or ""),
                )
            )

        if rows:
            self.connection.executemany(
                """
                INSERT INTO staking_metrics (
                    address,
                    estimated_current_stake_wei,
                    stake_in_wei,
                    unstake_out_wei,
                    direct_contract_balance_wei,
                    stake_tx_count,
                    unstake_tx_count,
                    flow_tx_count,
                    source,
                    confidence,
                    last_event_block,
                    last_event_tx_hash,
                    last_refreshed_block,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(address) DO UPDATE SET
                    estimated_current_stake_wei =
                        excluded.estimated_current_stake_wei,
                    stake_in_wei =
                        excluded.stake_in_wei,
                    unstake_out_wei =
                        excluded.unstake_out_wei,
                    direct_contract_balance_wei =
                        excluded.direct_contract_balance_wei,
                    stake_tx_count =
                        excluded.stake_tx_count,
                    unstake_tx_count =
                        excluded.unstake_tx_count,
                    flow_tx_count =
                        excluded.flow_tx_count,
                    source =
                        excluded.source,
                    confidence =
                        excluded.confidence,
                    last_event_block =
                        excluded.last_event_block,
                    last_event_tx_hash =
                        excluded.last_event_tx_hash,
                    last_refreshed_block =
                        excluded.last_refreshed_block,
                    updated_at =
                        excluded.updated_at
                """,
                rows,
            )

        written = len(rows)
        self.dirty_addresses.clear()
        return written

    def clear_cache(self) -> None:
        self.cache.clear()
        self.dirty_addresses.clear()



class SQLiteConvictionMetrics:
    """
    Legacy, rollback-safe Conviction state.

    Legacy Conviction tables are retained for backward compatibility with
    historical v3.5.0 state. v3.6.0 no longer treats Conviction as an
    active public scoring or rank signal.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.dirty_addresses: set[str] = set()
        self.pending_events: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def normalize(address: str) -> str:
        return str(address).lower()

    @staticmethod
    def normalize_tx_hash(tx_hash: str) -> str:
        return str(tx_hash).lower()

    @staticmethod
    def default_record(address: str) -> Dict[str, Any]:
        return {
            "address": str(address).lower(),
            "conviction_locked_wei": "0",
            "conviction_lock_tx_count": 0,
            "first_conviction_lock_block": None,
            "first_conviction_lock_tx_hash": None,
            "first_conviction_lock_time": None,
            "last_conviction_lock_block": None,
            "last_conviction_lock_tx_hash": None,
            "last_conviction_lock_time": None,
            "source": "NO_CONVICTION_LOCK_FLOW",
            "confidence": "LOW",
            "updated_at": "",
        }

    def _load(self, address: str) -> Optional[Dict[str, Any]]:
        address = self.normalize(address)

        if address in self.cache:
            return self.cache[address]

        row = self.connection.execute(
            """
            SELECT
                conviction_locked_wei,
                conviction_lock_tx_count,
                first_conviction_lock_block,
                first_conviction_lock_tx_hash,
                first_conviction_lock_time,
                last_conviction_lock_block,
                last_conviction_lock_tx_hash,
                last_conviction_lock_time,
                source,
                confidence,
                updated_at
            FROM conviction_metrics
            WHERE address = ?
            """,
            (address,),
        ).fetchone()

        if row is None:
            return None

        record = {
            "address": address,
            "conviction_locked_wei": str(row[0] or "0"),
            "conviction_lock_tx_count": int(row[1] or 0),
            "first_conviction_lock_block": row[2],
            "first_conviction_lock_tx_hash": row[3],
            "first_conviction_lock_time": row[4],
            "last_conviction_lock_block": row[5],
            "last_conviction_lock_tx_hash": row[6],
            "last_conviction_lock_time": row[7],
            "source": str(row[8] or "NO_CONVICTION_LOCK_FLOW"),
            "confidence": str(row[9] or "LOW"),
            "updated_at": str(row[10] or ""),
        }

        self.cache[address] = record
        return record

    def setdefault(
        self,
        address: str,
        default: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        address = self.normalize(address)
        record = self._load(address)

        if record is None:
            record = (
                default
                if default is not None
                else self.default_record(address)
            )
            record["address"] = address
            self.cache[address] = record

        self.dirty_addresses.add(address)
        return record

    def has_event(self, tx_hash: str) -> bool:
        tx_hash = self.normalize_tx_hash(tx_hash)

        if tx_hash in self.pending_events:
            return True

        row = self.connection.execute(
            """
            SELECT 1
            FROM conviction_lock_events
            WHERE tx_hash = ?
            LIMIT 1
            """,
            (tx_hash,),
        ).fetchone()

        return row is not None

    def record_lock_event(
        self,
        *,
        address: str,
        value_wei: int,
        block_number: int,
        transaction_index: int,
        tx_hash: str,
        timestamp: str,
    ) -> bool:
        address = self.normalize(address)
        tx_hash = self.normalize_tx_hash(tx_hash)
        value_wei = int(value_wei)

        if value_wei <= 0:
            return False

        if self.has_event(tx_hash):
            return False

        self.pending_events[tx_hash] = {
            "tx_hash": tx_hash,
            "address": address,
            "block_number": int(block_number),
            "transaction_index": int(transaction_index),
            "value_wei": str(value_wei),
            "timestamp": str(timestamp),
        }

        record = self.setdefault(address)

        current_locked = int(
            str(record.get("conviction_locked_wei") or "0")
        )

        record["conviction_locked_wei"] = str(
            current_locked + value_wei
        )

        record["conviction_lock_tx_count"] = (
            int(record.get("conviction_lock_tx_count") or 0)
            + 1
        )

        first_block = record.get("first_conviction_lock_block")
        if first_block is None or int(block_number) < int(first_block):
            record["first_conviction_lock_block"] = int(block_number)
            record["first_conviction_lock_tx_hash"] = tx_hash
            record["first_conviction_lock_time"] = str(timestamp)

        last_block = record.get("last_conviction_lock_block")
        if last_block is None or int(block_number) >= int(last_block):
            record["last_conviction_lock_block"] = int(block_number)
            record["last_conviction_lock_tx_hash"] = tx_hash
            record["last_conviction_lock_time"] = str(timestamp)

        record["source"] = "CONVICTION_LOCK_TRANSACTION_FLOW"
        record["confidence"] = "HIGH"
        record["updated_at"] = str(timestamp)

        self.dirty_addresses.add(address)
        return True

    def count(self) -> int:
        return int(
            self.connection.execute(
                "SELECT COUNT(*) FROM conviction_metrics"
            ).fetchone()[0]
        )

    def flush(self) -> int:
        event_rows = []

        for tx_hash in sorted(self.pending_events):
            event = self.pending_events[tx_hash]
            event_rows.append(
                (
                    event["tx_hash"],
                    event["address"],
                    event["block_number"],
                    event["transaction_index"],
                    event["value_wei"],
                    event["timestamp"],
                )
            )

        if event_rows:
            self.connection.executemany(
                """
                INSERT OR IGNORE INTO conviction_lock_events (
                    tx_hash,
                    address,
                    block_number,
                    transaction_index,
                    value_wei,
                    timestamp
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                event_rows,
            )

        rows = []

        for address in sorted(self.dirty_addresses):
            record = self.cache.get(address)

            if record is None:
                continue

            rows.append(
                (
                    address,
                    str(
                        record.get("conviction_locked_wei", "0")
                        or "0"
                    ),
                    int(record.get("conviction_lock_tx_count") or 0),
                    record.get("first_conviction_lock_block"),
                    record.get("first_conviction_lock_tx_hash"),
                    record.get("first_conviction_lock_time"),
                    record.get("last_conviction_lock_block"),
                    record.get("last_conviction_lock_tx_hash"),
                    record.get("last_conviction_lock_time"),
                    str(
                        record.get("source")
                        or "NO_CONVICTION_LOCK_FLOW"
                    ),
                    str(record.get("confidence") or "LOW"),
                    str(record.get("updated_at") or ""),
                )
            )

        if rows:
            self.connection.executemany(
                """
                INSERT INTO conviction_metrics (
                    address,
                    conviction_locked_wei,
                    conviction_lock_tx_count,
                    first_conviction_lock_block,
                    first_conviction_lock_tx_hash,
                    first_conviction_lock_time,
                    last_conviction_lock_block,
                    last_conviction_lock_tx_hash,
                    last_conviction_lock_time,
                    source,
                    confidence,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(address) DO UPDATE SET
                    conviction_locked_wei =
                        excluded.conviction_locked_wei,
                    conviction_lock_tx_count =
                        excluded.conviction_lock_tx_count,
                    first_conviction_lock_block =
                        excluded.first_conviction_lock_block,
                    first_conviction_lock_tx_hash =
                        excluded.first_conviction_lock_tx_hash,
                    first_conviction_lock_time =
                        excluded.first_conviction_lock_time,
                    last_conviction_lock_block =
                        excluded.last_conviction_lock_block,
                    last_conviction_lock_tx_hash =
                        excluded.last_conviction_lock_tx_hash,
                    last_conviction_lock_time =
                        excluded.last_conviction_lock_time,
                    source =
                        excluded.source,
                    confidence =
                        excluded.confidence,
                    updated_at =
                        excluded.updated_at
                """,
                rows,
            )

        written = len(rows)

        self.pending_events.clear()
        self.dirty_addresses.clear()

        return written


class SQLiteOfficialInceptionNFTTokens:
    """
    Latest-owner state for the official DAC Testnet Inception NFT.

    Token IDs are tracked individually so historical backfill can run
    from latest blocks toward genesis without allowing an older Transfer
    event to overwrite a newer owner.

    Incremental forward sync still updates a token when a strictly newer
    event position is observed.
    """

    ZERO_ADDRESS = (
        "0x0000000000000000000000000000000000000000"
    )

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.dirty_token_ids: set[str] = set()

    @staticmethod
    def normalize_token_id(token_id: Any) -> str:
        raw = str(token_id)

        if raw.startswith("0x"):
            return str(int(raw, 16))

        return str(int(raw))

    @classmethod
    def normalize_address(
        cls,
        address: Any,
    ) -> Optional[str]:
        if address is None:
            return None

        normalized = str(address).lower()

        if normalized == cls.ZERO_ADDRESS:
            return None

        return normalized

    def _load(
        self,
        token_id: Any,
    ) -> Optional[Dict[str, Any]]:
        token_id = self.normalize_token_id(token_id)

        if token_id in self.cache:
            return self.cache[token_id]

        row = self.connection.execute(
            """
            SELECT
                owner_address,
                from_address,
                event_block,
                event_transaction_index,
                event_log_index,
                event_tx_hash,
                event_type,
                updated_at
            FROM official_inception_nft_tokens
            WHERE token_id = ?
            """,
            (token_id,),
        ).fetchone()

        if row is None:
            return None

        record = {
            "token_id": token_id,
            "owner_address": row[0],
            "from_address": row[1],
            "event_block": int(row[2]),
            "event_transaction_index": int(row[3]),
            "event_log_index": int(row[4]),
            "event_tx_hash": str(row[5]),
            "event_type": str(row[6]),
            "updated_at": str(row[7] or ""),
        }

        self.cache[token_id] = record
        return record

    def observe_transfer(
        self,
        token_id: Any,
        from_address: Any,
        to_address: Any,
        block_number: int,
        transaction_index: int,
        log_index: int,
        tx_hash: str,
        timestamp: str,
    ) -> bool:
        token_id = self.normalize_token_id(token_id)
        from_address = self.normalize_address(from_address)
        owner_address = self.normalize_address(to_address)

        event_position = (
            int(block_number),
            int(transaction_index),
            int(log_index),
        )

        existing = self._load(token_id)

        if existing is not None:
            existing_position = (
                int(existing["event_block"]),
                int(existing["event_transaction_index"]),
                int(existing["event_log_index"]),
            )

            # Backfill berjalan latest -> genesis. Event yang lebih lama
            # tidak boleh menimpa pemilik dari event yang lebih baru.
            if event_position <= existing_position:
                return False

        if from_address is None:
            event_type = "MINT"
        elif owner_address is None:
            event_type = "BURN"
        else:
            event_type = "TRANSFER"

        self.cache[token_id] = {
            "token_id": token_id,
            "owner_address": owner_address,
            "from_address": from_address,
            "event_block": event_position[0],
            "event_transaction_index": event_position[1],
            "event_log_index": event_position[2],
            "event_tx_hash": str(tx_hash),
            "event_type": event_type,
            "updated_at": str(timestamp),
        }

        self.dirty_token_ids.add(token_id)
        return True

    def count(self) -> int:
        return int(
            self.connection.execute(
                """
                SELECT COUNT(*)
                FROM official_inception_nft_tokens
                """
            ).fetchone()[0]
        )

    def flush(self) -> int:
        rows = []

        for token_id in sorted(
            self.dirty_token_ids,
            key=int,
        ):
            record = self.cache.get(token_id)

            if record is None:
                continue

            rows.append(
                (
                    token_id,
                    record.get("owner_address"),
                    record.get("from_address"),
                    int(record["event_block"]),
                    int(record["event_transaction_index"]),
                    int(record["event_log_index"]),
                    str(record["event_tx_hash"]),
                    str(record["event_type"]),
                    str(record.get("updated_at") or ""),
                )
            )

        if rows:
            self.connection.executemany(
                """
                INSERT INTO official_inception_nft_tokens (
                    token_id,
                    owner_address,
                    from_address,
                    event_block,
                    event_transaction_index,
                    event_log_index,
                    event_tx_hash,
                    event_type,
                    updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(token_id) DO UPDATE SET
                    owner_address = excluded.owner_address,
                    from_address = excluded.from_address,
                    event_block = excluded.event_block,
                    event_transaction_index =
                        excluded.event_transaction_index,
                    event_log_index = excluded.event_log_index,
                    event_tx_hash = excluded.event_tx_hash,
                    event_type = excluded.event_type,
                    updated_at = excluded.updated_at
                """,
                rows,
            )

        written = len(rows)
        self.dirty_token_ids.clear()
        return written

    def clear_cache(self) -> None:
        self.cache.clear()
        self.dirty_token_ids.clear()


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

        self._ensure_schema()

        self.wallet_metrics = SQLiteWalletMetrics(self.connection)
        self.staking_metrics = SQLiteStakingMetrics(self.connection)
        self.conviction_metrics = SQLiteConvictionMetrics(
            self.connection
        )
        self.official_inception_nft_tokens = (
            SQLiteOfficialInceptionNFTTokens(self.connection)
        )

        self.last_staking_rows_written = 0
        self.last_conviction_rows_written = 0
        self.last_official_inception_nft_rows_written = 0

    def _ensure_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS staking_metrics (
                address TEXT PRIMARY KEY COLLATE NOCASE,

                estimated_current_stake_wei TEXT
                    NOT NULL DEFAULT '0',

                stake_in_wei TEXT
                    NOT NULL DEFAULT '0',

                unstake_out_wei TEXT
                    NOT NULL DEFAULT '0',

                direct_contract_balance_wei TEXT,

                stake_tx_count INTEGER
                    NOT NULL DEFAULT 0,

                unstake_tx_count INTEGER
                    NOT NULL DEFAULT 0,

                flow_tx_count INTEGER
                    NOT NULL DEFAULT 0,

                source TEXT
                    NOT NULL DEFAULT 'NO_STAKE_FLOW',

                confidence TEXT
                    NOT NULL DEFAULT 'LOW',

                last_event_block INTEGER,
                last_event_tx_hash TEXT,
                last_refreshed_block INTEGER,

                updated_at TEXT
                    NOT NULL DEFAULT ''
            );

            CREATE INDEX IF NOT EXISTS
                staking_metrics_last_event_block
            ON staking_metrics(last_event_block);

            CREATE INDEX IF NOT EXISTS
                staking_metrics_last_refreshed_block
            ON staking_metrics(last_refreshed_block);

            CREATE TABLE IF NOT EXISTS conviction_lock_events (
                tx_hash TEXT PRIMARY KEY,
                address TEXT NOT NULL COLLATE NOCASE,
                block_number INTEGER NOT NULL,
                transaction_index INTEGER NOT NULL DEFAULT 0,
                value_wei TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS
                conviction_lock_events_address
            ON conviction_lock_events(address);

            CREATE INDEX IF NOT EXISTS
                conviction_lock_events_block
            ON conviction_lock_events(block_number);

            CREATE TABLE IF NOT EXISTS conviction_metrics (
                address TEXT PRIMARY KEY COLLATE NOCASE,

                conviction_locked_wei TEXT
                    NOT NULL DEFAULT '0',

                conviction_lock_tx_count INTEGER
                    NOT NULL DEFAULT 0,

                first_conviction_lock_block INTEGER,
                first_conviction_lock_tx_hash TEXT,
                first_conviction_lock_time TEXT,

                last_conviction_lock_block INTEGER,
                last_conviction_lock_tx_hash TEXT,
                last_conviction_lock_time TEXT,

                source TEXT
                    NOT NULL DEFAULT 'NO_CONVICTION_LOCK_FLOW',

                confidence TEXT
                    NOT NULL DEFAULT 'LOW',

                updated_at TEXT
                    NOT NULL DEFAULT ''
            );

            CREATE INDEX IF NOT EXISTS
                conviction_metrics_last_lock_block
            ON conviction_metrics(last_conviction_lock_block);


            CREATE TABLE IF NOT EXISTS
                official_inception_nft_tokens (
                    token_id TEXT PRIMARY KEY,

                    owner_address TEXT
                        COLLATE NOCASE,

                    from_address TEXT
                        COLLATE NOCASE,

                    event_block INTEGER
                        NOT NULL,

                    event_transaction_index INTEGER
                        NOT NULL,

                    event_log_index INTEGER
                        NOT NULL,

                    event_tx_hash TEXT
                        NOT NULL,

                    event_type TEXT
                        NOT NULL,

                    updated_at TEXT
                        NOT NULL DEFAULT ''
                );

            CREATE INDEX IF NOT EXISTS
                official_inception_nft_owner_address
            ON official_inception_nft_tokens(owner_address);

            CREATE INDEX IF NOT EXISTS
                official_inception_nft_event_position
            ON official_inception_nft_tokens(
                event_block,
                event_transaction_index,
                event_log_index
            );
            """
        )

        self.connection.commit()

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

        staking_dirty_before = set(
            self.staking_metrics.dirty_addresses
        )

        conviction_dirty_before = set(
            self.conviction_metrics.dirty_addresses
        )

        conviction_pending_events_before = dict(
            self.conviction_metrics.pending_events
        )

        last_staking_rows_written_before = (
            self.last_staking_rows_written
        )

        last_conviction_rows_written_before = (
            self.last_conviction_rows_written
        )

        official_inception_dirty_before = set(
            self.official_inception_nft_tokens.dirty_token_ids
        )

        last_official_inception_nft_rows_written_before = (
            self.last_official_inception_nft_rows_written
        )

        try:
            self.connection.execute("BEGIN IMMEDIATE")

            wallets_written = self.wallet_metrics.flush()
            staking_rows_written = self.staking_metrics.flush()
            conviction_rows_written = self.conviction_metrics.flush()

            official_inception_nft_rows_written = (
                self.official_inception_nft_tokens.flush()
            )

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

            self.last_staking_rows_written = (
                staking_rows_written
            )

            self.last_conviction_rows_written = (
                conviction_rows_written
            )

            self.last_official_inception_nft_rows_written = (
                official_inception_nft_rows_written
            )

            return wallets_written

        except Exception:
            self.connection.rollback()

            self.wallet_metrics.dirty_addresses = dirty_before
            self.wallet_metrics.new_addresses = new_before
            self.wallet_metrics._database_count = count_before

            self.staking_metrics.dirty_addresses = (
                staking_dirty_before
            )

            self.last_staking_rows_written = (
                last_staking_rows_written_before
            )

            self.conviction_metrics.dirty_addresses = (
                conviction_dirty_before
            )

            self.conviction_metrics.pending_events = (
                conviction_pending_events_before
            )

            self.last_conviction_rows_written = (
                last_conviction_rows_written_before
            )

            self.official_inception_nft_tokens.dirty_token_ids = (
                official_inception_dirty_before
            )

            self.last_official_inception_nft_rows_written = (
                last_official_inception_nft_rows_written_before
            )

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
