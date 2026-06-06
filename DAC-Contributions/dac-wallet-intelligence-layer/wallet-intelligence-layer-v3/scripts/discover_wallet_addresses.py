#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Wallet Discovery Layer

Discovers active DAC Testnet wallet addresses from recent RPC block data.

Current phase:
- RPC block-range wallet discovery.
- Extracts transaction sender and receiver addresses.
- Writes data/wallet-addresses.generated.txt.
- Writes data/wallet-discovery-summary.json.

This is a controlled discovery layer, not a full historical chain indexer yet.
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set


DEFAULT_DAC_RPC_URL = "https://rpctest.dachain.tech/"
RPC_URLS = [
    url.strip()
    for url in os.environ.get("DAC_RPC_URLS", os.environ.get("DAC_RPC_URL", DEFAULT_DAC_RPC_URL)).split(",")
    if url.strip()
]
DAC_CHAIN_ID = 21894
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 0.08


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def http_post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    encoded = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={
            "User-Agent": "Wallet-Intelligence-Layer-v3-Discovery/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def rpc_call(method: str, params: List[Any]) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params,
    }

    last_error = None

    for rpc_url in RPC_URLS:
        for attempt in range(1, 4):
            try:
                response = http_post_json(rpc_url, payload)
                if "error" in response:
                    raise RuntimeError(response["error"])
                return response.get("result")
            except Exception as exc:
                last_error = exc
                wait_seconds = 0.4 * attempt
                print(f"[WARN] RPC failed: {rpc_url} method={method} attempt={attempt}/3 error={exc}")
                time.sleep(wait_seconds)

    raise RuntimeError(f"RPC call failed across configured endpoints. method={method} last_error={last_error}")


def hex_to_int(value: str) -> int:
    return int(value, 16)


def int_to_hex(value: int) -> str:
    return hex(value)


def normalize_address(value: Any) -> str:
    address = str(value or "").strip().lower()
    if address.startswith("0x") and len(address) == 42:
        return address
    return ""


def latest_block_number() -> int:
    return hex_to_int(rpc_call("eth_blockNumber", []))


def get_block_with_txs(block_number: int) -> Dict[str, Any]:
    block = rpc_call("eth_getBlockByNumber", [int_to_hex(block_number), True])
    if not isinstance(block, dict):
        raise RuntimeError(f"Invalid block response for block {block_number}")
    return block


def discover_addresses(start_block: int, end_block: int, max_addresses: int = 0) -> Dict[str, Any]:
    addresses: Set[str] = set()
    blocks_scanned = 0
    txs_scanned = 0
    errors: List[str] = []

    for block_number in range(start_block, end_block + 1):
        try:
            block = get_block_with_txs(block_number)
            blocks_scanned += 1
            txs = block.get("transactions", [])
            if not isinstance(txs, list):
                txs = []

            for tx in txs:
                if not isinstance(tx, dict):
                    continue

                txs_scanned += 1

                from_address = normalize_address(tx.get("from"))
                to_address = normalize_address(tx.get("to"))

                if from_address:
                    addresses.add(from_address)
                if to_address:
                    addresses.add(to_address)

                if max_addresses and len(addresses) >= max_addresses:
                    break

            if max_addresses and len(addresses) >= max_addresses:
                break

            time.sleep(REQUEST_DELAY_SECONDS)

        except Exception as exc:
            errors.append(f"block {block_number}: {exc}")

    return {
        "addresses": sorted(addresses),
        "blocks_scanned": blocks_scanned,
        "txs_scanned": txs_scanned,
        "errors": errors,
    }


def write_text(path: Path, lines: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    root = project_root()

    parser = argparse.ArgumentParser(description="Discover active DAC Testnet wallet addresses from recent RPC blocks.")
    parser.add_argument(
        "--blocks",
        type=int,
        default=200,
        help="Number of recent blocks to scan.",
    )
    parser.add_argument(
        "--max-addresses",
        type=int,
        default=50,
        help="Stop after discovering this many unique addresses. Use 0 for no cap.",
    )
    parser.add_argument(
        "--out",
        default=str(root / "data" / "wallet-addresses.generated.txt"),
        help="Output discovered wallet address list.",
    )
    parser.add_argument(
        "--summary",
        default=str(root / "data" / "wallet-discovery-summary.json"),
        help="Output discovery summary JSON.",
    )
    args = parser.parse_args()

    latest = latest_block_number()
    end_block = latest
    start_block = max(0, latest - args.blocks + 1)

    print(f"[INFO] Latest block: {latest}")
    print(f"[INFO] Scanning blocks: {start_block} -> {end_block}")
    print(f"[INFO] Max addresses: {args.max_addresses if args.max_addresses else 'unlimited'}")

    result = discover_addresses(start_block, end_block, args.max_addresses)
    addresses = result["addresses"]

    summary = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "module": "Wallet Discovery Layer",
        "network": "DAC Testnet",
        "chain_id": DAC_CHAIN_ID,
        "rpc_urls": RPC_URLS,
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "latest_block": latest,
        "start_block": start_block,
        "end_block": end_block,
        "requested_blocks": args.blocks,
        "blocks_scanned": result["blocks_scanned"],
        "transactions_scanned": result["txs_scanned"],
        "unique_addresses": len(addresses),
        "output": str(Path(args.out)),
        "errors": result["errors"],
        "status": "DISCOVERED_FROM_RECENT_RPC_BLOCKS",
    }

    write_text(Path(args.out), addresses)
    write_json(Path(args.summary), summary)

    print(f"[OK] Unique addresses: {len(addresses)}")
    print(f"[OK] Wrote: {args.out}")
    print(f"[OK] Wrote: {args.summary}")

    if result["errors"]:
        print(f"[WARN] Errors: {len(result['errors'])}")


if __name__ == "__main__":
    main()
