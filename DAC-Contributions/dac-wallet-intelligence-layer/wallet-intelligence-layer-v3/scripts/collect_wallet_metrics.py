#!/usr/bin/env python3
"""
Wallet Intelligence Layer v3.0.0 — Explorer/RPC Wallet Metrics Collector

This collector converts a wallet address list into source wallet metrics that can be
ranked by generate_wallet_rank_index.py.

Current phase:
- Address-list based collector.
- Uses DAC Explorer API first.
- Uses DAC RPC fallback for native balance and transaction count.
- Produces data/source-wallet-metrics.generated.json.

This is not yet a full-chain wallet discovery scanner.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Dict, List, Optional


DAC_EXPLORER_API = "https://exptest.dachain.tech/api"
DAC_RPC_URL = "https://rpctest.dachain.tech/"
DAC_CHAIN_ID = 21894
NATIVE_TOKEN = "DACC"
REQUEST_TIMEOUT_SECONDS = 25
REQUEST_DELAY_SECONDS = 0.2


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def normalize_address(address: str) -> str:
    value = str(address or "").strip().lower()
    if not value or value.startswith("#"):
        return ""
    if not value.startswith("0x") or len(value) != 42:
        raise ValueError(f"Invalid EVM address: {address}")
    int(value[2:], 16)
    return value


def wei_to_native(value: Any) -> str:
    try:
        amount = Decimal(str(value or "0")) / Decimal(10**18)
    except InvalidOperation:
        amount = Decimal("0")

    normalized = amount.normalize()
    if normalized == normalized.to_integral_value():
        return str(int(normalized))
    return format(normalized, "f")


def hex_to_int(value: Any) -> int:
    if not value:
        return 0
    return int(str(value), 16)


def read_addresses(path: Path) -> List[str]:
    addresses: List[str] = []
    seen = set()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        address = normalize_address(raw_line)
        if not address:
            continue
        if address not in seen:
            addresses.append(address)
            seen.add(address)

    return addresses


def http_get_json(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Wallet-Intelligence-Layer-v3-Rank-Collector/1.0",
            "Accept": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        payload = response.read().decode("utf-8")
        return json.loads(payload)


def http_post_json(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    encoded = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=encoded,
        headers={
            "User-Agent": "Wallet-Intelligence-Layer-v3-Rank-Collector/1.0",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        return json.loads(response.read().decode("utf-8"))


def explorer_request(params: Dict[str, Any]) -> Dict[str, Any]:
    query = urllib.parse.urlencode(params)
    url = f"{DAC_EXPLORER_API}?{query}"
    return http_get_json(url)


def rpc_call(method: str, params: List[Any]) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": int(time.time() * 1000),
        "method": method,
        "params": params,
    }
    response = http_post_json(DAC_RPC_URL, payload)
    if "error" in response:
        raise RuntimeError(response["error"])
    return response.get("result")


def normalize_explorer_result(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    result = data.get("result", [])

    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]

    if isinstance(result, dict) and "items" in result and isinstance(result["items"], list):
        return [item for item in result["items"] if isinstance(item, dict)]

    return []


def explorer_balance(address: str) -> Optional[str]:
    data = explorer_request({
        "module": "account",
        "action": "balance",
        "address": address,
    })

    result = data.get("result")
    if result is None:
        return None

    return wei_to_native(result)


def rpc_balance(address: str) -> str:
    result = rpc_call("eth_getBalance", [address, "latest"])
    return wei_to_native(hex_to_int(result))


def explorer_txlist(address: str) -> List[Dict[str, Any]]:
    data = explorer_request({
        "module": "account",
        "action": "txlist",
        "address": address,
        "sort": "asc",
    })
    return normalize_explorer_result(data)


def explorer_tokenlist(address: str) -> List[Dict[str, Any]]:
    data = explorer_request({
        "module": "account",
        "action": "tokenlist",
        "address": address,
    })
    return normalize_explorer_result(data)


def explorer_nft_transfers(address: str) -> List[Dict[str, Any]]:
    data = explorer_request({
        "module": "account",
        "action": "tokennfttx",
        "address": address,
        "sort": "asc",
    })
    return normalize_explorer_result(data)


def rpc_transaction_count(address: str) -> int:
    result = rpc_call("eth_getTransactionCount", [address, "latest"])
    return hex_to_int(result)


def numeric_value(value: Any) -> Decimal:
    try:
        return Decimal(str(value or "0"))
    except InvalidOperation:
        return Decimal("0")


def tx_value_native(tx: Dict[str, Any]) -> Decimal:
    return Decimal(wei_to_native(tx.get("value", "0")))


def gas_used_value(tx: Dict[str, Any]) -> Decimal:
    # Explorer txlist usually exposes gasUsed. If unavailable, use 0.
    return numeric_value(tx.get("gasUsed") or tx.get("gas_used") or 0)


def reputation_score(metrics: Dict[str, Any]) -> int:
    score = 0

    tx_count = int(metrics.get("tx_count", 0))
    native_balance = numeric_value(metrics.get("native_balance", 0))
    native_volume = numeric_value(metrics.get("native_volume", 0))
    nft_holdings = int(metrics.get("nft_holdings", 0))
    collection_diversity = int(metrics.get("collection_diversity", 0))

    if tx_count >= 500:
        score += 25
    elif tx_count >= 100:
        score += 18
    elif tx_count >= 25:
        score += 10
    elif tx_count > 0:
        score += 5

    if native_balance >= Decimal("100"):
        score += 20
    elif native_balance >= Decimal("50"):
        score += 15
    elif native_balance >= Decimal("10"):
        score += 8
    elif native_balance > 0:
        score += 4

    if native_volume >= Decimal("100"):
        score += 20
    elif native_volume >= Decimal("25"):
        score += 12
    elif native_volume > 0:
        score += 6

    if nft_holdings >= 20:
        score += 15
    elif nft_holdings >= 5:
        score += 8
    elif nft_holdings > 0:
        score += 4

    if collection_diversity >= 5:
        score += 10
    elif collection_diversity >= 2:
        score += 6
    elif collection_diversity > 0:
        score += 3

    return min(score, 100)


def sybil_risk_score(metrics: Dict[str, Any]) -> int:
    risk = 50

    tx_count = int(metrics.get("tx_count", 0))
    native_balance = numeric_value(metrics.get("native_balance", 0))
    native_volume = numeric_value(metrics.get("native_volume", 0))
    nft_holdings = int(metrics.get("nft_holdings", 0))
    collection_diversity = int(metrics.get("collection_diversity", 0))

    if tx_count >= 100:
        risk -= 15
    elif tx_count >= 25:
        risk -= 8
    elif tx_count <= 2:
        risk += 15

    if native_balance >= Decimal("10"):
        risk -= 8
    elif native_balance == 0:
        risk += 10

    if native_volume >= Decimal("25"):
        risk -= 8
    elif native_volume == 0:
        risk += 8

    if nft_holdings > 0:
        risk -= 5
    if collection_diversity >= 2:
        risk -= 5

    return max(0, min(risk, 100))


def collect_wallet(address: str) -> Dict[str, Any]:
    errors: List[str] = []

    try:
        txs = explorer_txlist(address)
    except Exception as exc:
        txs = []
        errors.append(f"explorer txlist failed: {exc}")

    try:
        native_balance = explorer_balance(address)
        if native_balance is None:
            raise RuntimeError("empty explorer balance")
    except Exception as exc:
        errors.append(f"explorer balance failed: {exc}")
        try:
            native_balance = rpc_balance(address)
        except Exception as rpc_exc:
            native_balance = "0"
            errors.append(f"rpc balance failed: {rpc_exc}")

    try:
        token_items = explorer_tokenlist(address)
    except Exception as exc:
        token_items = []
        errors.append(f"explorer tokenlist failed: {exc}")

    try:
        nft_transfers = explorer_nft_transfers(address)
    except Exception as exc:
        nft_transfers = []
        errors.append(f"explorer tokennfttx failed: {exc}")

    if txs:
        tx_count = len(txs)
    else:
        try:
            tx_count = rpc_transaction_count(address)
        except Exception as exc:
            tx_count = 0
            errors.append(f"rpc tx count failed: {exc}")

    gas_used = sum(gas_used_value(tx) for tx in txs)

    address_lower = address.lower()
    native_volume = sum(
        tx_value_native(tx)
        for tx in txs
        if str(tx.get("from", "")).lower() == address_lower or str(tx.get("to", "")).lower() == address_lower
    )

    nft_holdings = 0
    collection_addresses = set()

    for item in token_items:
        token_type = str(item.get("type") or item.get("tokenType") or "").lower()
        balance = numeric_value(item.get("balance") or item.get("amount") or 0)
        contract = str(item.get("contractAddress") or item.get("tokenAddress") or "").lower()

        if "erc-721" in token_type or "erc721" in token_type or "nft" in token_type:
            nft_holdings += int(balance)
            if contract:
                collection_addresses.add(contract)

    if not nft_holdings and nft_transfers:
        for item in nft_transfers:
            contract = str(item.get("contractAddress") or item.get("tokenAddress") or "").lower()
            if contract:
                collection_addresses.add(contract)
        nft_holdings = len(nft_transfers)

    metrics: Dict[str, Any] = {
        "tx_count": int(tx_count),
        "gas_used": int(gas_used),
        "native_volume": str(native_volume.normalize()) if native_volume else "0",
        "native_balance": native_balance,
        "estimated_stake": "0",
        "nft_holdings": int(nft_holdings),
        "collection_diversity": len(collection_addresses),
    }

    metrics["reputation_score"] = reputation_score(metrics)
    metrics["sybil_risk_score"] = sybil_risk_score(metrics)

    return {
        "address": address,
        "metrics": metrics,
        "collection_status": "OK" if not errors else "PARTIAL",
        "errors": errors,
    }


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    root = project_root()

    parser = argparse.ArgumentParser(description="Collect DAC Testnet wallet metrics for Wallet Intelligence Layer v3.")
    parser.add_argument(
        "--addresses",
        default=str(root / "data" / "wallet-addresses.sample.txt"),
        help="Text file containing wallet addresses, one per line.",
    )
    parser.add_argument(
        "--out",
        default=str(root / "data" / "source-wallet-metrics.generated.json"),
        help="Output source wallet metrics JSON file.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional maximum number of addresses to collect.",
    )

    args = parser.parse_args()

    addresses = read_addresses(Path(args.addresses))
    if args.limit and args.limit > 0:
        addresses = addresses[: args.limit]

    wallets = []

    for index, address in enumerate(addresses, start=1):
        print(f"[{index}/{len(addresses)}] Collecting {address}")
        wallets.append(collect_wallet(address))
        time.sleep(REQUEST_DELAY_SECONDS)

    payload = {
        "project": "Wallet Intelligence Layer v3.0.0",
        "feature": "Wallet Rank Intelligence",
        "network": "DAC Testnet",
        "chain_id": DAC_CHAIN_ID,
        "native_token": NATIVE_TOKEN,
        "source": {
            "explorer_api": DAC_EXPLORER_API,
            "rpc_url": DAC_RPC_URL,
            "address_list": str(Path(args.addresses)),
        },
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "wallet_count": len(wallets),
        "wallets": wallets,
    }

    write_json(Path(args.out), payload)

    print(f"[OK] Wallets collected: {len(wallets)}")
    print(f"[OK] Wrote: {args.out}")


if __name__ == "__main__":
    main()
