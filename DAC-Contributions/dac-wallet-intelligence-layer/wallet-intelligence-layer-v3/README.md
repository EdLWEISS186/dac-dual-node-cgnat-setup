# DAC Wallet Intelligence Layer v3.0.0

## Wallet Intelligence Layer v3.0.0 — Wallet Rank Intelligence

> v3 turns every verified wallet variable into a comparative public rank signal.

Wallet Intelligence Layer v3.0.0 continues the public-data wallet intelligence direction from v1 and v2.

v1 focused on public wallet analysis.  
v2 continued that direction and introduced a dynamic wallet-bound badge layer through Wallet Status SBT.  
v3 extends the same model by adding comparative wallet ranking for every verified wallet variable.

Instead of only showing isolated wallet metrics, v3 prepares each verified variable to be compared against the broader indexed DAC Testnet wallet population.

---

## Core Idea

Wallet Intelligence Layer v3 turns wallet analysis into wallet positioning.

For each supported wallet variable, the dashboard is designed to show:

    raw value
    rank position
    total ranked wallets
    percentile
    rank tier

Example:

    Transactions Rank: #1023 / 18,430
    Gas Used Rank:     #927 / 18,430
    Native Volume Rank:#883 / 18,430

---

## Main Feature

### Wallet Rank Intelligence

Wallet Rank Intelligence is the main feature of v3.

It introduces a comparative public rank signal for wallet variables that were already part of the Wallet Intelligence Layer direction, including:

    transactions
    gas used
    native volume
    native balance
    estimated stake
    NFT holdings
    collection diversity
    reputation score
    low Sybil-risk profile

The goal is to move from:

    This wallet has 381 transactions.

to:

    This wallet ranks #1023 by transactions among indexed active DAC Testnet wallets.

---

## Version Direction

    v1 = public-data wallet analysis
    v2 = public-data wallet analysis + Wallet Status SBT
    v3 = rank-aware wallet intelligence

v3 does not replace v2. It continues the same no-connect, public-data-first model and adds a rank-aware layer on top of it.

---

## Current Implementation

The initial v3 foundation adds:

    wallet-intelligence-layer-v3/

This folder was created as a continuation of v2 and updated for the v3 identity.

Current additions:

- v3 project identity and title.
- Wallet Rank Intelligence positioning.
- Initial rank summary JSON schema.
- Initial wallet rank index JSON schema.
- Frontend rank engine.
- Address-based rank lookup UI.
- Empty-index handling before the indexer is implemented.
- Local wallet rank indexer skeleton.
- Sample source wallet metrics file.
- Generated sample rank summary and wallet rank index artifacts.
- Local `.gitignore` allowlist for v3 JSON rank artifacts.
- README documentation for the v3 rank-aware model.

---

## Rank Data

Current rank data files:

    data/wallet-rank-summary.json
    data/wallet-rank-index.json

### wallet-rank-summary.json

Stores rank model metadata, including:

    project
    feature
    core statement
    network
    chain ID
    native token
    rank model
    generated timestamp
    total ranked wallets
    latest indexed block
    ranking variables

### wallet-rank-index.json

Stores wallet-level rank data.

The current rank index is intentionally empty because the chain-wide rank indexer has not been implemented yet.

---
## Wallet Rank Indexer Skeleton

The v3 project now includes a local rank generator:

    scripts/generate_wallet_rank_index.py

Current input:

    data/source-wallet-metrics.sample.json

Current outputs:

    data/wallet-rank-summary.json
    data/wallet-rank-index.json

The generator reads wallet-level metric data, computes comparative ranks for supported variables, calculates percentiles, assigns rank tiers, and writes static JSON artifacts for the dashboard.

Current skeleton behavior:

    source wallet count: 4
    status: GENERATED_FROM_LOCAL_SOURCE

The sample wallet:

    0x870ad63acc507cdfd878f170606d19ae78988afe

currently produces:

    TX Rank: 2
    Gas Rank: 2
    Volume Rank: 2
    Tier: TOP_50_PERCENT

This confirms that the ranking logic, JSON generation, and frontend-readable data format are working before connecting the indexer to Explorer API or RPC-derived data.

---


## Frontend Rank Engine

The v3 dashboard includes:

    rank-engine.js

The rank engine currently:

- Loads rank summary data.
- Loads wallet rank index data.
- Validates wallet addresses.
- Normalizes addresses.
- Looks up rank data for a pasted wallet address.
- Displays metric value, rank, and percentile.
- Handles empty rank index state.
- Handles wallets not found in the current rank index.

Current pre-indexer behavior:

    Rank index is ready, but no wallet rankings have been generated yet.

This confirms that the frontend rank layer is ready before the real indexer is added.

---

## Ranking Variables

Initial v3 ranking variables:

    tx_count
    gas_used
    native_volume
    native_balance
    estimated_stake
    nft_holdings
    collection_diversity
    reputation_score
    low_sybil_risk

The low-Sybil-risk ranking is treated as an inverted safety signal. Lower risk should produce a stronger low-risk position.

---

## Architecture

Wallet Intelligence Layer v3 is designed to remain GitHub Pages compatible.

The intended architecture is:

    Explorer API / RPC
            ↓
    Wallet rank indexer
            ↓
    Generated rank JSON
            ↓
    Static dashboard fetch
            ↓
    Wallet address lookup
            ↓
    Rank-aware wallet profile

The browser should not scan the entire chain directly.

Chain-wide ranking should be generated by a local script or GitHub Actions workflow, then written into static JSON files that the dashboard can read.

---

## Safety and Scope

Wallet Intelligence Layer v3 remains:

- Public-data based.
- No wallet connection required for rank lookup.
- No private key handling.
- No backend custody.
- Not an official DAC product.
- Not an eligibility checker.
- Not a reward checker.
- Not a definitive Sybil detection system.

The rank layer is a community-built public testnet intelligence signal.

---

## Files Added or Updated

    index.html
    wallet-intelligence.css
    wallet-intelligence.js
    rank-engine.js
    data/wallet-rank-summary.json
    data/wallet-rank-index.json
    README.md

---

## Current Status

    Status: v3 foundation, frontend rank lookup layer, and local indexer skeleton added
    Indexer: local skeleton implemented
    Rank data: generated from sample source wallet metrics
    Dashboard: ready to read generated rank JSON
    Next indexer phase: Explorer API / RPC data integration

---

## Next Step

Connect the wallet rank indexer to Explorer API and/or RPC-derived wallet variables.

The next phase will move from sample local wallet metrics into real DAC Testnet wallet activity data.
