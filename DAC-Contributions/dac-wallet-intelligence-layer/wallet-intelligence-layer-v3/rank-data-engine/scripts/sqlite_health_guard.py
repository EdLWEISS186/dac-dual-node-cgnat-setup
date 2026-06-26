#!/usr/bin/env python3
"""
WIL v3 SQLite Health Guard

Safe operational health guard for the WIL SQLite rank-state database.

Modes:
- lightweight: fast startup readiness check
- full: full PRAGMA quick_check integrity check
- diagnose: classify failure symptoms and escalate safely

This script does not mutate the SQLite database.
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable


REQUIRED_TABLES = {
    "checkpoint",
    "counters",
    "state_meta",
    "wallet_metrics",
    "enrichment_queue",
    "indexed_block_coverage",
    "indexed_transaction_ledger",
}

SQLITE_ERROR_PATTERNS = [
    "database disk image is malformed",
    "file is not a database",
    "disk i/o error",
    "database is locked",
    "database or disk is full",
    "no such table",
    "readonly database",
    "attempt to write a readonly database",
    "unable to open database file",
    "sqlite",
]

DISK_ERROR_PATTERNS = [
    "no space left on device",
    "disk quota exceeded",
    "input/output error",
]

RPC_ERROR_PATTERNS = [
    "connection refused",
    "timed out",
    "timeout",
    "http error",
    "rpc",
    "failed to establish",
]

GIT_ERROR_PATTERNS = [
    "git fetch failed",
    "git pull failed",
    "git push",
    "non-fast-forward",
    "failed to push",
    "repository",
]


def emit(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def tail_text(path: Path, max_bytes: int = 250_000) -> str:
    if not path or not path.exists():
        return ""

    try:
        size = path.stat().st_size
        with path.open("rb") as handle:
            if size > max_bytes:
                handle.seek(size - max_bytes)
            data = handle.read()
        return data.decode("utf-8", errors="replace")
    except Exception as exc:
        return f"[health_guard_log_read_error] {exc}"


def contains_any(text: str, patterns: Iterable[str]) -> list[str]:
    lowered = text.lower()
    return [pattern for pattern in patterns if pattern.lower() in lowered]


def sqlite_connect_ro(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(
        f"file:{db_path.resolve()}?mode=ro",
        uri=True,
        timeout=10,
    )


def check_file_basics(db_path: Path) -> int:
    if not db_path.exists():
        emit("ERROR", f"SQLite state file does not exist: {db_path}")
        return 10

    if not db_path.is_file():
        emit("ERROR", f"SQLite state path is not a file: {db_path}")
        return 11

    size = db_path.stat().st_size
    if size < 4096:
        emit("ERROR", f"SQLite state file is too small to be valid: {size} bytes")
        return 12

    emit("INFO", f"SQLite state file: {db_path}")
    emit("INFO", f"SQLite state size bytes: {size}")
    return 0


def lightweight_check(db_path: Path) -> int:
    file_rc = check_file_basics(db_path)
    if file_rc != 0:
        return file_rc

    try:
        db = sqlite_connect_ro(db_path)
        db.execute("PRAGMA query_only=ON")
        schema_version = db.execute("PRAGMA schema_version").fetchone()[0]

        tables = {
            row[0]
            for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        missing_tables = sorted(REQUIRED_TABLES - tables)
        db.close()

        if missing_tables:
            emit(
                "ERROR",
                "SQLite missing required tables: " + ", ".join(missing_tables),
            )
            return 20

        emit(
            "OK",
            f"SQLite lightweight schema guard passed | schema_version={schema_version}",
        )
        return 0

    except sqlite3.DatabaseError as exc:
        emit("ERROR", f"SQLite lightweight check database error: {exc}")
        return 21
    except Exception as exc:
        emit("ERROR", f"SQLite lightweight check failed: {exc}")
        return 22


def full_check(db_path: Path) -> int:
    file_rc = check_file_basics(db_path)
    if file_rc != 0:
        return file_rc

    try:
        emit("INFO", "Running SQLite full PRAGMA quick_check")
        db = sqlite_connect_ro(db_path)
        result = db.execute("PRAGMA quick_check").fetchone()[0]
        db.close()

        if result != "ok":
            emit("ERROR", f"SQLite full quick_check failed: {result}")
            return 30

        emit("OK", "SQLite full quick_check passed")
        return 0

    except sqlite3.DatabaseError as exc:
        emit("ERROR", f"SQLite full check database error: {exc}")
        return 31
    except Exception as exc:
        emit("ERROR", f"SQLite full check failed: {exc}")
        return 32


def classify_log(log_path: Path | None) -> tuple[str, list[str]]:
    if not log_path:
        return "NO_LOG_PROVIDED", []

    text = tail_text(log_path)
    if not text:
        return "NO_LOG_CONTENT", []

    sqlite_hits = contains_any(text, SQLITE_ERROR_PATTERNS)
    disk_hits = contains_any(text, DISK_ERROR_PATTERNS)
    rpc_hits = contains_any(text, RPC_ERROR_PATTERNS)
    git_hits = contains_any(text, GIT_ERROR_PATTERNS)

    if sqlite_hits:
        return "SQLITE_RELATED_FAILURE", sqlite_hits
    if disk_hits:
        return "DISK_OR_FILESYSTEM_FAILURE", disk_hits
    if rpc_hits:
        return "RPC_OR_NETWORK_FAILURE", rpc_hits
    if git_hits:
        return "GIT_OR_PUBLISH_FAILURE", git_hits

    return "UNCLASSIFIED_FAILURE", []


def diagnose(db_path: Path, log_path: Path | None, force_full: bool) -> int:
    emit("INFO", "Starting SQLite health diagnosis")

    lightweight_rc = lightweight_check(db_path)
    classification, hits = classify_log(log_path)

    emit("DIAG", f"failure_classification={classification}")
    if log_path:
        emit("DIAG", f"log_path={log_path}")
    if hits:
        emit("DIAG", "matched_patterns=" + ", ".join(hits))

    should_full_check = (
        force_full
        or lightweight_rc != 0
        or classification in {
            "SQLITE_RELATED_FAILURE",
            "DISK_OR_FILESYSTEM_FAILURE",
        }
    )

    if should_full_check:
        emit("INFO", "Escalating to full SQLite quick_check")
        full_rc = full_check(db_path)

        if full_rc != 0:
            emit(
                "ACTION",
                "Stop indexing. Do not auto-repair or overwrite the SQLite state. "
                "Use the latest verified backup or perform manual recovery.",
            )
            return full_rc

        if lightweight_rc != 0:
            emit(
                "ACTION",
                "Full check passed but lightweight guard failed. Inspect schema/migration state.",
            )
            return lightweight_rc

        emit("ACTION", "Full SQLite check passed. Investigate non-corruption causes if worker still fails.")
        return 0

    if classification == "RPC_OR_NETWORK_FAILURE":
        emit("ACTION", "SQLite appears readable. Check RPC node availability and retry next cycle.")
        return 0

    if classification == "GIT_OR_PUBLISH_FAILURE":
        emit("ACTION", "SQLite appears readable. Check GitHub/network publishing path.")
        return 0

    emit("ACTION", "SQLite lightweight guard passed. No SQLite corruption signal detected.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WIL SQLite health guard")
    parser.add_argument(
        "--sqlite-state",
        required=True,
        help="Path to the SQLite rank-state database",
    )
    parser.add_argument(
        "--mode",
        choices=["lightweight", "full", "diagnose"],
        default="lightweight",
    )
    parser.add_argument(
        "--log",
        default="",
        help="Optional worker log path for diagnosis",
    )
    parser.add_argument(
        "--force-full",
        action="store_true",
        help="Force full quick_check during diagnose mode",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.sqlite_state).expanduser()
    log_path = Path(args.log).expanduser() if args.log else None

    if args.mode == "lightweight":
        return lightweight_check(db_path)

    if args.mode == "full":
        return full_check(db_path)

    if args.mode == "diagnose":
        return diagnose(db_path, log_path, args.force_full)

    emit("ERROR", f"Unsupported mode: {args.mode}")
    return 99


if __name__ == "__main__":
    raise SystemExit(main())
