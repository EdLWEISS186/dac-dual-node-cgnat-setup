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

## Final v3 Architecture Lock

Wallet Intelligence Layer v3.0.0 is locked as a hybrid rank intelligence layer.

The final model is:

    single wallet address input
            ↓
    single CHECK button
            ↓
    live wallet intelligence from existing v2 logic
            ↓
    real-time Explorer API network snapshot
            ↓
    valid custom rank index for unavailable rank metrics
            ↓
    one integrated Wallet Rank Intelligence section

This project must not introduce a second wallet input, a second rank button, or a standalone rank checker.

Official public sources only:

    RPC:          https://rpctest.dachain.tech/
    Explorer:     https://exptest.dachain.tech/
    Explorer API: https://exptest.dachain.tech/api
    Explorer API v2: https://exptest.dachain.tech/api/v2

Data taken directly from Explorer API should be used live. Data not directly exposed as rank endpoints should be calculated by custom indexer logic from Explorer/RPC/Explorer API data.

Confirmed live Explorer API data:

    total_addresses
    total_transactions
    transactions_today
    gas_used_today
    total_blocks
    network_utilization_percentage
    live address balance
    address list with coin_balance and transactions_count
    balance-sorted address list

Rank data requiring custom indexer logic:

    transaction-count rank
    gas-used rank
    native-volume rank
    NFT holdings rank
    collection diversity rank
    reputation score rank
    low-risk rank
    overall wallet rank

Manual or limited test index runs are validation-only and must not be presented as final Wallet Rank Intelligence data.

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

## Full Explorer Address Rank Indexer Foundation

The v3 project now includes the foundation for a full Explorer-visible address rank indexer:

    scripts/build_full_explorer_address_rank_index.py

Purpose:

    Build valid Native Funds Rank and Transactions Rank from the official DAC Explorer API address population.

Official source:

    https://exptest.dachain.tech/api/v2/addresses

Confirmed address fields:

    hash
    coin_balance
    transactions_count
    is_contract

The indexer has two important modes:

    --probe
        Verifies Explorer API fields and writes no public rank data.

    --full --publish
        Reserved for full Explorer-visible address pagination.
        Publishes rank data only if pagination completes without a page cap.

Integrity rule:

    Capped or limited runs must not be published as final Wallet Rank Intelligence data.

The full indexer is designed to support sharded rank output:

    data/rank-shards/{address_prefix}.json

This avoids loading a very large wallet-rank-index file in the browser. The dashboard can later fetch only the shard needed for the checked wallet address.

Latest probe result:

    total_addresses: 6,410,389
    total_transactions: 21,533,530
    transactions_today: 474,628
    gas_used_today: 19,892,450,018
    total_blocks: 14,965,794
    first address page item count: 50

No public rank data was written during the probe.

---

## Full Indexer Resume and Pagination Safety

The full Explorer address rank indexer now includes resume/checkpoint safety for long pagination runs.

Checkpoint file:

    data/indexer-work/full-address-indexer-checkpoint.json

Work database:

    data/indexer-work/explorer-address-rank.sqlite

Safety behavior:

- `--reset` clears the local work database and checkpoint.
- `--resume` continues from the last saved `next_page_params`.
- capped runs remain validation-only.
- `--publish` is refused when `--max-pages` is used.
- public rank data is only allowed after full Explorer pagination completes.
- duplicate/stalled pagination is detected and stops the run.

Latest validation result:

    mode: --full --max-pages 3 --reset
    pages fetched: 2
    total unique rows: 50
    stop reason: STALLED_PAGINATION_DUPLICATE_PAGE
    public rank data written: no

This means the indexer correctly refused to continue when the Explorer address pagination returned duplicate data. This protects Wallet Rank Intelligence from publishing incomplete or unreliable rank data.

Next investigation:

    confirm the correct Explorer API pagination parameters for /api/v2/addresses
    then re-run full pagination only after pagination advances reliably

---

## Transaction Rank Indexer Foundation

The v3 project now includes a transaction-stream rank indexer foundation:

    scripts/build_transaction_rank_index.py

This is the correct custom-indexer direction after `/api/v2/addresses` pagination was found to return duplicate/stalled pages.

Official source:

    https://exptest.dachain.tech/api/v2/transactions

Confirmed transaction pagination result:

    page 1 count: 50
    page 2 count: 50
    overlap: 0
    new page 2 transactions: 50
    result: OK_ADVANCES

Confirmed transaction fields:

    hash
    block_number
    position
    from
    to
    gas_used
    value
    timestamp
    status

Current validation result:

    validation pages: 3
    processed transactions: 150
    wallets seen: 167
    stop reason: MAX_PAGES_VALIDATION_ONLY
    public rank data written: false

Indexer metrics foundation:

    transactions
    gas_used
    native_volume

Integrity rule:

    Validation runs do not publish public rank data.
    Public rank output must only be generated after full/integrity-safe indexing is implemented.

This transaction indexer becomes the primary custom rank source for variables not directly exposed as rank endpoints by Explorer API.

---

## Transaction Indexer Full Mode and Publish Guard

The transaction-stream indexer has been upgraded beyond validation-only mode.

Updated script:

    scripts/build_transaction_rank_index.py

Added capabilities:

    --full
        Runs transaction pagination until the Explorer transaction stream ends.

    --publish
        Publishes rank summary and rank shards only after full stream completion.

    --reset
        Clears the local transaction indexer work state.

    --validate-pages N
        Runs capped validation only and never publishes public rank data.

Rank generation foundation:

    transactions rank
    gas_used rank
    native_volume rank
    overall rank

Publish safety:

    --publish is refused unless --full is used.
    --publish is refused when --validate-pages is used.
    public rank data is written only if the full transaction stream completes.

Latest validation result:

    command: --validate-pages 2 --reset
    processed transactions: 100
    wallets seen: 134
    stop reason: MAX_PAGES_VALIDATION_ONLY
    public rank data written: false

Publish guard validation:

    command: --validate-pages 2 --publish
    result: Refusing to publish without --full.

This confirms that capped validation runs cannot accidentally publish final Wallet Rank Intelligence rank data.

---

## Current Status

    Status: final hybrid v3 architecture locked
    Network snapshot: live Explorer API
    Rank index: pending completed full transaction-stream custom indexer run
    Manual/sample rank artifacts: removed
    UI model: single wallet input, single CHECK button, one integrated Wallet Rank Intelligence section
    Public dependency model: official DAC public sources only



---

## Next Step

Continue the full Explorer-visible address rank indexer.

Next implementation steps:
1. Add or confirm resume behavior for long transaction-stream full indexing.
2. Run longer validation windows to check stability across more transaction pages.
3. Add sharded frontend lookup for rank-shards/{address_prefix}.json.
4. Publish rank data only after full/integrity-safe indexing is completed.
5. Keep limited runs as probe/validation only, never as final Wallet Rank Intelligence output.
