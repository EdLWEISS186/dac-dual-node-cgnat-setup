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

## Single-Check Rank Integration

Wallet Rank Intelligence is now integrated into the main wallet check flow.

The dashboard no longer uses a separate rank lookup panel, separate wallet input, or separate rank button. Users only paste a wallet address once into the main checker and press the existing `CHECK` button.

The output flow is now:

    paste wallet address
            ↓
    click CHECK
            ↓
    generate Wallet Intelligence profile
            ↓
    append Wallet Rank Intelligence result
            ↓
    include walletRankIntelligence in raw JSON output

The top module grid now continues from the previous v2 modules:

    01 Proof of Native Funds
    02 Proof of Assets Engine
    03 Activity Analytics
    04 Portfolio Intelligence
    05 Reputation Scoring
    06 Dynamic Badge
    07 Wallet Rank Intelligence

This aligns v3 with the intended product direction: ranking is not a separate checker, but an additional comparative intelligence layer inside the normal wallet analysis result.

---

## Hybrid Rank Intelligence Model

Wallet Intelligence Layer v3 now uses a hybrid data model.

The project uses real-time official DAC Explorer/API data where the Explorer already exposes global or address-level values, and uses a custom indexer only for rank metrics that are not directly available from the Explorer API.

Official public sources:

    RPC:          https://rpctest.dachain.tech/
    Explorer:     https://exptest.dachain.tech/
    Explorer API: https://exptest.dachain.tech/api

Explorer API data confirmed available:

    total_addresses
    total_transactions
    transactions_today
    gas_used_today
    total_blocks
    live address balance
    address list with coin_balance and transactions_count
    balance-sorted address list

Explorer API data not confirmed as directly available:

    direct rank by wallet address
    transaction-count rank by wallet
    gas-used rank by wallet
    native-volume rank by wallet
    NFT/asset rank by wallet
    reputation rank by wallet
    low-risk rank by wallet
    overall rank by wallet

Final v3 direction:

    live wallet check
            ↓
    real-time Explorer API network snapshot
            ↓
    custom rank index for unavailable rank metrics
            ↓
    one integrated Wallet Rank Intelligence section

The previous manually generated 100-wallet rank artifacts were removed because they were only pipeline validation data and should not be presented as final rank data.

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
    data/source-wallet-metrics.generated.json
    data/wallet-addresses.sample.txt
    data/wallet-addresses.generated.txt
    data/wallet-discovery-summary.json
    scripts/generate_wallet_rank_index.py
    scripts/collect_wallet_metrics.py
    scripts/discover_wallet_addresses.py
    scripts/run_wallet_rank_pipeline.py
    README.md

---

## Current Status

    Status: v3 hybrid rank model being corrected
    Network snapshot: real-time Explorer API
    Rank index: pending valid custom indexer
    Invalid manual rank artifacts: removed
    Dashboard goal: single wallet check with one integrated Wallet Rank Intelligence section


---

## Next Step

Build the corrected hybrid Wallet Rank Intelligence section.

The next implementation should show real-time Explorer API network snapshot data and only display rank values from a valid custom rank index when the index is available.
