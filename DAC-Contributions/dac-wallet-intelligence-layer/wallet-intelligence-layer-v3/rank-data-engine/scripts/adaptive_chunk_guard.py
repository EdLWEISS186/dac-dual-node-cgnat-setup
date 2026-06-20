#!/usr/bin/env python3
"""
WIL v3 Adaptive Chunk Guard

Evaluates one completed worker chunk using:
- chain/data density metrics from public-run-status.json
- device/resource metrics supplied by the runner

Outputs shell-safe variable assignments for the runner.
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


def shell_var(name: str, value) -> str:
    if isinstance(value, bool):
        value = "1" if value else "0"
    return f"{name}={shlex.quote(str(value))}"


def as_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def as_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def read_status(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def decide(args: argparse.Namespace) -> dict:
    status = read_status(Path(args.status))
    last = status.get("last_run", {}) or {}

    processed_blocks = as_int(last.get("processed_blocks"))
    processed_tx = as_int(last.get("processed_transactions"))
    wallet_rows = as_int(last.get("wallet_rows_written"))
    staking_rows = as_int(last.get("staking_rows_written"))
    stop_reason = str(last.get("stop_reason") or "UNKNOWN")

    elapsed = as_int(args.elapsed_seconds)
    wal_growth = max(0, as_int(args.wal_growth_bytes))
    free_kb = as_int(args.free_kb)
    mem_available_kb = as_int(args.mem_available_kb)
    swap_used_kb = as_int(args.swap_used_kb)
    worker_mem_kb = as_int(args.worker_mem_kb)
    cpu_idle_pct = as_float(args.cpu_idle_pct)
    io_wait_pct = as_float(args.io_wait_pct)
    load1 = as_float(args.load1)
    cpu_cores = max(1, as_int(args.cpu_cores, 1))

    should_continue = True
    reason = "OK"

    load_threshold = cpu_cores * (as_float(args.max_load_factor_x100) / 100.0)

    checks = [
        (processed_blocks <= 0, "processed_blocks_zero"),
        (stop_reason != "MAX_BLOCKS_REACHED", f"worker_stop_reason_{stop_reason}"),
        (free_kb < as_int(args.min_free_kb), f"disk_free_low_{free_kb}_lt_{args.min_free_kb}"),
        (mem_available_kb < as_int(args.min_mem_available_kb), f"mem_available_low_{mem_available_kb}_lt_{args.min_mem_available_kb}"),
        (swap_used_kb > as_int(args.max_swap_used_kb), f"swap_used_high_{swap_used_kb}_gt_{args.max_swap_used_kb}"),
        (worker_mem_kb > as_int(args.max_worker_mem_kb), f"worker_mem_high_{worker_mem_kb}_gt_{args.max_worker_mem_kb}"),
        (load1 > load_threshold, f"load_high_{load1:.2f}_gt_{load_threshold:.2f}"),
        (cpu_idle_pct < as_float(args.min_cpu_idle_pct), f"cpu_idle_low_{cpu_idle_pct:.2f}_lt_{args.min_cpu_idle_pct}"),
        (io_wait_pct > as_float(args.max_io_wait_pct), f"io_wait_high_{io_wait_pct:.2f}_gt_{args.max_io_wait_pct}"),
        (elapsed > as_int(args.max_chunk_seconds), f"elapsed_high_{elapsed}_gt_{args.max_chunk_seconds}"),
        (processed_tx > as_int(args.max_chunk_tx), f"tx_density_high_{processed_tx}_gt_{args.max_chunk_tx}"),
        (wallet_rows > as_int(args.max_wallet_rows), f"wallet_rows_high_{wallet_rows}_gt_{args.max_wallet_rows}"),
        (staking_rows > as_int(args.max_staking_rows), f"staking_rows_high_{staking_rows}_gt_{args.max_staking_rows}"),
        (wal_growth > as_int(args.max_wal_growth_bytes), f"wal_growth_high_{wal_growth}_gt_{args.max_wal_growth_bytes}"),
    ]

    for failed, failed_reason in checks:
        if failed:
            should_continue = False
            reason = failed_reason
            break

    return {
        "should_continue": should_continue,
        "reason": reason,
        "processed_blocks": processed_blocks,
        "processed_tx": processed_tx,
        "wallet_rows": wallet_rows,
        "staking_rows": staking_rows,
        "stop_reason": stop_reason,
        "elapsed_seconds": elapsed,
        "wal_growth_bytes": wal_growth,
        "free_kb": free_kb,
        "mem_available_kb": mem_available_kb,
        "swap_used_kb": swap_used_kb,
        "worker_mem_kb": worker_mem_kb,
        "load1": f"{load1:.2f}",
        "cpu_cores": cpu_cores,
        "cpu_idle_pct": f"{cpu_idle_pct:.2f}",
        "io_wait_pct": f"{io_wait_pct:.2f}",
        "load_threshold": f"{load_threshold:.2f}",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate WIL adaptive chunk health")
    parser.add_argument("--status", required=True)
    parser.add_argument("--elapsed-seconds", required=True)
    parser.add_argument("--wal-growth-bytes", required=True)
    parser.add_argument("--free-kb", required=True)
    parser.add_argument("--mem-available-kb", required=True)
    parser.add_argument("--swap-used-kb", required=True)
    parser.add_argument("--worker-mem-kb", required=True)
    parser.add_argument("--load1", required=True)
    parser.add_argument("--cpu-cores", required=True)
    parser.add_argument("--cpu-idle-pct", required=True)
    parser.add_argument("--io-wait-pct", required=True)

    parser.add_argument("--max-chunk-seconds", required=True)
    parser.add_argument("--max-chunk-tx", required=True)
    parser.add_argument("--max-wallet-rows", required=True)
    parser.add_argument("--max-staking-rows", required=True)
    parser.add_argument("--max-wal-growth-bytes", required=True)
    parser.add_argument("--min-free-kb", required=True)
    parser.add_argument("--min-mem-available-kb", required=True)
    parser.add_argument("--max-swap-used-kb", required=True)
    parser.add_argument("--max-worker-mem-kb", required=True)
    parser.add_argument("--max-load-factor-x100", required=True)
    parser.add_argument("--min-cpu-idle-pct", required=True)
    parser.add_argument("--max-io-wait-pct", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = decide(args)

    mapping = {
        "ADAPTIVE_SHOULD_CONTINUE": result["should_continue"],
        "ADAPTIVE_STOP_REASON": result["reason"],
        "ADAPTIVE_CHUNK_PROCESSED_BLOCKS": result["processed_blocks"],
        "ADAPTIVE_CHUNK_PROCESSED_TX": result["processed_tx"],
        "ADAPTIVE_CHUNK_WALLET_ROWS": result["wallet_rows"],
        "ADAPTIVE_CHUNK_STAKING_ROWS": result["staking_rows"],
        "ADAPTIVE_CHUNK_WORKER_STOP_REASON": result["stop_reason"],
        "ADAPTIVE_CHUNK_ELAPSED_SECONDS": result["elapsed_seconds"],
        "ADAPTIVE_CHUNK_WAL_GROWTH_BYTES": result["wal_growth_bytes"],
        "ADAPTIVE_FREE_KB": result["free_kb"],
        "ADAPTIVE_MEM_AVAILABLE_KB": result["mem_available_kb"],
        "ADAPTIVE_SWAP_USED_KB": result["swap_used_kb"],
        "ADAPTIVE_WORKER_MEM_KB": result["worker_mem_kb"],
        "ADAPTIVE_LOAD1": result["load1"],
        "ADAPTIVE_CPU_CORES": result["cpu_cores"],
        "ADAPTIVE_CPU_IDLE_PCT": result["cpu_idle_pct"],
        "ADAPTIVE_IO_WAIT_PCT": result["io_wait_pct"],
        "ADAPTIVE_LOAD_THRESHOLD": result["load_threshold"],
    }

    for key, value in mapping.items():
        print(shell_var(key, value))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
