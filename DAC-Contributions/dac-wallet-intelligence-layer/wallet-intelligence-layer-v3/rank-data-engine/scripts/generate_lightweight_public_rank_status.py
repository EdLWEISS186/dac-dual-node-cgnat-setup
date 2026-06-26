#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VERSION = "v3.3.0"


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--status-file",
        required=True,
        help="Path to public-run-status.json",
    )
    args = parser.parse_args()

    status_path = Path(args.status_file)
    status = read_json(status_path)

    project_root = Path(__file__).resolve().parents[2]
    manifest_path = project_root / "rank-data-engine/data/latest.json"
    summary_path = project_root / "data/wallet-rank-summary.json"
    index_path = project_root / "data/wallet-rank-index.json"
    shards_dir = project_root / "data/rank-shards"

    if shards_dir.exists():
        shutil.rmtree(shards_dir)

    sync_status = status.get("sync_status", {})
    counters = status.get("counters", {})
    generated_at = now_utc()

    total_wallets = int(counters.get("total_indexed_wallets") or 0)
    total_transactions = int(
        counters.get("total_processed_transactions") or 0
    )

    summary = {
        "schema": "WIL_V3_RANK_SUMMARY",
        "version": VERSION,
        "status": "EXTERNALIZED_STATE_BACKFILL_IN_PROGRESS",
        "has_valid_rank_index": False,
        "rank_lookup_enabled": False,
        "generated_at": generated_at,
        "rank_data_source": "externalized-local-state",
        "externalized_state": True,
        "external_state_file": "~/wil-v3-rank-state/latest-state.json",
        "total_ranked_wallets": total_wallets,
        "total_indexed_wallets": total_wallets,
        "total_processed_transactions": total_transactions,
        "rank_shards": {
            "status": "DISABLED_DURING_BACKFILL",
            "directory": None,
            "reason": (
                "Rank shards are not published while historical "
                "backfill or catch-up is still in progress."
            ),
        },
        "sync_status": sync_status,
        "metrics": [
            "native_funds",
            "transactions",
            "gas_used",
            "native_volume",
            "nft_holdings",
            "collection_diversity",
            "reputation_score",
            "low_sybil_risk",
            "overall_rank",
        ],
        "note": (
            "v3.7.0 parity-safe rebuild publish mode. Full global rank "
            "generation is deferred until the state is publish-ready."
        ),
    }

    index = {
        "schema": "WIL_V3_RANK_INDEX",
        "version": VERSION,
        "status": "EXTERNALIZED_STATE_PENDING_VALID_PUBLISH",
        "mode": "EXTERNALIZED_STATE",
        "has_valid_rank_index": False,
        "rank_lookup_enabled": False,
        "directory": None,
        "summary": (
            "Rank shards are intentionally not published during "
            "historical backfill or catch-up."
        ),
        "externalized_state": True,
        "sync_status": sync_status,
    }

    manifest = {
        "schema": "WIL_V3_PUBLIC_RANK_MANIFEST",
        "version": VERSION,
        "project": "Wallet Intelligence Layer v3.7.0",
        "engine": "rank-data-engine",
        "network": status.get("network", "DAC Testnet"),
        "chain_id": status.get("chain_id", 21894),
        "status": "EXTERNALIZED_STATE_BACKFILL_IN_PROGRESS",
        "updated_at": generated_at,
        "externalized_state": True,
        "heavy_state_storage": status.get(
            "heavy_state_storage",
            "LOCAL_EXTERNAL_STATE_WITH_OPTIONAL_GOOGLE_DRIVE_BACKUP",
        ),
        "heavy_state_local_path": status.get(
            "heavy_state_local_path",
            "~/wil-v3-rank-state/latest-state.json",
        ),
        "github_storage_role": "PUBLIC_MANIFEST_ONLY",
        "rank_lookup_enabled": False,
        "rank_shards_published": False,
        "snapshot_archive_written": status.get(
            "snapshot_archive_written",
            False,
        ),
        "latest_snapshot": "externalized-local-state",
        "sync_status": sync_status,
        "counters": counters,
        "public_summary": {
            "path": "data/wallet-rank-summary.json",
            "status": summary["status"],
            "has_valid_rank_index": False,
            "total_ranked_wallets": total_wallets,
        },
        "note": (
            "v3.7.0 parity-safe rebuild publish mode. GitHub stores "
            "public manifest and summary only. Heavy wallet metrics "
            "remain local with optional Google Drive rollover backup."
        ),
    }

    write_json(summary_path, summary)
    write_json(index_path, index)
    write_json(manifest_path, manifest)

    print("[OK] WIL v3.6.0 lightweight public artifacts generated")
    print(f"[OK] Manifest: {manifest_path}")
    print(f"[OK] Summary: {summary_path}")
    print(f"[OK] Index: {index_path}")


if __name__ == "__main__":
    main()
