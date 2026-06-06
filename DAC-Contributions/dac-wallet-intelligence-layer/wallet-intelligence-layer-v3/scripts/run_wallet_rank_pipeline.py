#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Wallet Rank Pipeline Runner

Runs the v3 rank data pipeline in order:

1. Discover wallet addresses from recent RPC blocks.
2. Collect Explorer/RPC wallet metrics for discovered addresses.
3. Generate wallet rank summary and wallet rank index JSON.

This script is designed as the local/automation entrypoint for refreshing
Wallet Rank Intelligence artifacts.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def run_command(command: List[str], env: dict | None = None) -> None:
    print("")
    print("[RUN]", " ".join(command))
    subprocess.run(command, check=True, env=env)


def main() -> None:
    root = project_root()
    scripts_dir = root / "scripts"
    data_dir = root / "data"

    parser = argparse.ArgumentParser(
        description="Run the Wallet Intelligence Layer v3 wallet rank pipeline."
    )
    parser.add_argument(
        "--blocks",
        type=int,
        default=500,
        help="Recent RPC blocks to scan during wallet discovery.",
    )
    parser.add_argument(
        "--max-addresses",
        type=int,
        default=100,
        help="Maximum unique wallet addresses to discover. Use 0 for no cap.",
    )
    parser.add_argument(
        "--collect-limit",
        type=int,
        default=50,
        help="Maximum discovered wallets to collect metrics for. Use 0 for all discovered wallets.",
    )
    args = parser.parse_args()

    discovered_addresses = data_dir / "wallet-addresses.generated.txt"
    generated_metrics = data_dir / "source-wallet-metrics.generated.json"

    print("[INFO] Wallet Intelligence Layer v3.0.0 — Wallet Rank Pipeline")
    print(f"[INFO] Blocks: {args.blocks}")
    print(f"[INFO] Max addresses: {args.max_addresses if args.max_addresses else 'unlimited'}")
    print(f"[INFO] Collect limit: {args.collect_limit if args.collect_limit else 'all'}")
    print("[INFO] RPC URL: https://rpctest.dachain.tech/")

    run_command(
        [
            sys.executable,
            str(scripts_dir / "discover_wallet_addresses.py"),
            "--blocks",
            str(args.blocks),
            "--max-addresses",
            str(args.max_addresses),
        ],
    )

    collect_command = [
        sys.executable,
        str(scripts_dir / "collect_wallet_metrics.py"),
        "--addresses",
        str(discovered_addresses),
        "--out",
        str(generated_metrics),
    ]

    if args.collect_limit and args.collect_limit > 0:
        collect_command.extend(["--limit", str(args.collect_limit)])

    run_command(collect_command)

    run_command(
        [
            sys.executable,
            str(scripts_dir / "generate_wallet_rank_index.py"),
            "--source",
            str(generated_metrics),
        ],
    )

    print("")
    print("[OK] Wallet Rank Pipeline completed.")
    print(f"[OK] Discovery output: {discovered_addresses}")
    print(f"[OK] Metrics output:   {generated_metrics}")
    print(f"[OK] Rank summary:     {data_dir / 'wallet-rank-summary.json'}")
    print(f"[OK] Rank index:       {data_dir / 'wallet-rank-index.json'}")


if __name__ == "__main__":
    main()
