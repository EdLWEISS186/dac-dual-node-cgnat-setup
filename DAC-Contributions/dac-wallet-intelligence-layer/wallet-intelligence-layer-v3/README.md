# DAC Wallet Intelligence Layer v3.0.0

Client-side wallet intelligence interface and comparative public wallet rank signal for the **DAC Quantum Chain Testnet**.

Wallet Intelligence Layer v3.0.0 introduces **Wallet Rank Intelligence**: a rank layer that turns verified wallet variables into comparative public rank signals.

The project is community-built by **JERUZZALEM — DAC Infra Tester**.

> Not an official DAC product, not an official eligibility checker, not a reward checker, and not a definitive Sybil detection system.

**Live Interface**

- [Wallet Intelligence Layer v3](https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3/)

![Version](https://img.shields.io/badge/version-v3.0.0-blue?style=flat-square)
![Network](https://img.shields.io/badge/network-DAC%20testnet-yellow?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Wallet Check](https://img.shields.io/badge/wallet%20check-no%20connect%20required-brightgreen?style=flat-square)
![Rank Engine](https://img.shields.io/badge/rank%20engine-variable--aware-orange?style=flat-square)
![Data Sync](https://img.shields.io/badge/data%20sync-GitHub%20Actions-lightgrey?style=flat-square)

---

## v3.0.0 Initial Release

`v3.0.0` is the initial release of the Wallet Rank Intelligence layer.

Core statement:

```text
v3 turns every verified wallet variable into a comparative public rank signal.
```

The wallet check remains a no-connect, pasted-address flow. The new rank section adds comparative context from a generated public rank dataset.

Current active behavior:

| Component | Status |
|---|---|
| Main wallet checker | Active |
| Wallet connection for checking | Not required |
| Wallet Rank Intelligence section | Active |
| Rank data engine | Active |
| Historical backfill | In progress until genesis is reached |
| Fully synced rank claim | Only shown after `historical_backfill_complete: true` |
| Public data sources | Official DAC Explorer/RPC sources |

---

## Table of Contents

- [Overview](#overview)
- [Interface Preview](#interface-preview)
- [Design Goals](#design-goals)
- [Architecture](#architecture)
- [Wallet Rank Intelligence](#wallet-rank-intelligence)
- [Rank Data Engine](#rank-data-engine)
- [Ranking Variables](#ranking-variables)
- [Rank Data Status Model](#rank-data-status-model)
- [Data Sources](#data-sources)
- [Network Configuration](#network-configuration)
- [Security Model](#security-model)
- [Failure Handling](#failure-handling)
- [Repository Structure](#repository-structure)
- [Local Usage](#local-usage)
- [Initial Release Scope](#initial-release-scope)
- [License](#license)
- [Author](#author)

---

## Overview

Wallet Intelligence Layer v3 is a static public wallet intelligence interface for DAC Testnet.

The project reads public wallet activity, generates wallet-level intelligence, and adds a rank layer that compares wallet variables against the current indexed wallet dataset.

```text
Wallet address
↓
Live DAC Explorer/RPC check
↓
Wallet intelligence profile
↓
Wallet Rank Intelligence
↓
Comparative public rank signal
```

The rank layer is transparent by design.

If a wallet is not yet indexed, the UI shows `NaN` rank placeholders instead of fake values.  
If the rank engine is still backfilling historical data, the UI shows the current sync state instead of claiming full historical coverage.

---

## Interface Preview

The Wallet Rank Intelligence section is expected to look similar to the screenshot below:

![Wallet Rank Intelligence](assets/WalletRankIntelligence.png)

The screenshot shows the v3 rank section while the rank data engine was still in the **historical backfill** phase.

At the time the screenshot was taken:

```text
Backfill Status: IN_PROGRESS
Historical Complete: false
```

This means the displayed ranks were based on the current indexed snapshot, not yet the fully synced chain history from genesis.

Once the backfill reaches genesis, the same panel will show the completed historical state.

---

## Design Goals

The v3 design follows strict principles:

```text
No forced wallet connection for checking
No private key handling
No account login
No backend custody
No fabricated rank output
No hidden identity scoring
No full-chain validity claim before backfill completion
```

Core goals:

- Keep wallet checking simple and no-connect.
- Add comparative rank intelligence without hiding sync status.
- Use official DAC public sources only.
- Make rank progress visible directly in the UI.
- Display `NaN` placeholders for unindexed wallets.
- Keep generated rank data static and GitHub Pages compatible.
- Separate current indexed snapshot ranks from fully synced historical ranks.

---

## Architecture

Current implementation:

```text
wallet-intelligence-layer-v3/
├── index.html
├── wallet-intelligence.css
├── wallet-intelligence.js
├── rank-engine.js
├── README.md
├── assets/
│   └── WalletRankIntelligence.png
├── data/
│   ├── wallet-rank-summary.json
│   ├── wallet-rank-index.json
│   └── rank-shards/
│       └── {address_prefix}.json
├── scripts/
│   └── generate_rank_from_engine_data.py
└── rank-data-engine/
    ├── .gitignore
    ├── data/
    │   ├── latest.json
    │   └── snapshots/
    │       ├── backfill-from-latest-to-genesis.json
    │       └── backfill-*.json
    └── scripts/
        └── sync_rank_data_engine.py
```

Conceptual layout:

```text
wallet-intelligence.js
├── wallet input validation
├── live Explorer/RPC wallet reads
├── wallet profile generation
├── Wallet Rank Intelligence rendering
├── indexed wallet state
├── unindexed wallet state
└── failure-safe UI states

rank-engine.js
├── rank summary fetch
├── rank index fetch
├── rank shard lookup
└── safe unavailable state

rank-data-engine/scripts/sync_rank_data_engine.py
├── transaction stream backfill
├── checkpoint handling
├── wallet metric accumulation
├── wallet balance / asset enrichment
└── latest + snapshot writing

scripts/generate_rank_from_engine_data.py
├── reads rank-data-engine/data/latest.json
├── calculates variable-aware ranks
├── writes wallet-rank-summary.json
├── writes wallet-rank-index.json
└── writes data/rank-shards/*.json
```

---

## Wallet Rank Intelligence

Wallet Rank Intelligence displays:

```text
Network snapshot
Rank Data Engine Status
Rank tier
Strongest signal
Rank denominator
Per-variable rank cards
Unindexed wallet placeholder cards
```

### Indexed Wallet State

When the checked wallet exists in the current rank shard, the UI shows rank cards for:

```text
Native Funds
Transactions
Gas Used
Native Volume
NFT Holdings
Collection Diversity
Reputation Score
Low-Risk Profile
Overall Wallet Rank
```

Each card can show:

```text
metric value
rank position
rank denominator
top percentage
```

### Unindexed Wallet State

When the checked wallet has live wallet intelligence data but is not included in the current rank snapshot yet, the UI shows:

```text
NaN value
Rank: NaN / current ranked wallets
Percentile: NaN%
Current indexed snapshot
```

This prevents fake rank values while still showing the intended rank structure.

---

## Rank Data Engine

The rank data engine is the data sync layer for WIL v3.

It stores normalized wallet metric data, not raw transaction dumps.

Current flow:

```text
DAC Explorer transaction stream
↓
Normalize wallet metrics
↓
Accumulate sender / receiver data
↓
Enrich wallets with balance and asset data
↓
Write rank-data-engine/data/latest.json
↓
Write rank-data-engine/data/snapshots/*.json
↓
Generate public rank summary, index, and shards
```

The engine is driven by GitHub Actions:

```text
.github/workflows/wil-v3-rank-data-engine.yml
```

Current workflow behavior:

```text
sync_rank_data_engine.py --max-pages 5 --enrich-limit 100
↓
generate_rank_from_engine_data.py
↓
commit latest engine data, snapshots, summary, index, and shards
```

The schedule is offset to improve reliability:

```text
2-59/5 * * * *
```

Concurrency protection is enabled so rank-data-engine runs do not overlap.

---

## Ranking Variables

Wallet Rank Intelligence currently ranks these variables:

| Variable | Source / Logic |
|---|---|
| Native Funds | `native_balance_wei` from wallet enrichment |
| Transactions | `tx_count` accumulated from transaction stream |
| Gas Used | `gas_used_total` accumulated from transaction stream |
| Native Volume | `native_volume_wei` accumulated from native value movement |
| NFT Holdings | `nft_holdings_count` from asset enrichment |
| Collection Diversity | unique NFT collection contract count |
| Reputation Score | derived heuristic score from collected wallet metrics |
| Low-Risk Profile | derived heuristic score from collected wallet metrics |
| Overall Wallet Rank | composite rank across available variables |

Important clarification:

```text
Reputation Score, Low-Risk Profile, and Overall Wallet Rank are calculated by project logic.
They are not direct blockchain fields.
```

The bot collects the blockchain-derived input variables.  
The rank generator computes derived variables from those inputs.

---

## Rank Data Status Model

The UI exposes the rank engine state directly:

```text
Rank Data Engine Status
State
Last Sync
Latest Snapshot
Processed Transactions
Ranked Wallets
Backfill Status
Historical Complete
```

During historical backfill:

```text
backfill_status: IN_PROGRESS
historical_backfill_complete: false
```

After full historical backfill:

```text
backfill_status: COMPLETE
historical_backfill_complete: true
```

Until full backfill completes, ranks are scoped to the current indexed snapshot.

---

## Data Sources

### DAC Explorer API

```text
https://exptest.dachain.tech/api
https://exptest.dachain.tech/api/v2
```

Used for:

```text
network stats
transaction stream
address-level data
token / asset information where available
```

### DAC RPC Endpoint

```text
https://rpctest.dachain.tech/
```

Used for:

```text
eth_getBalance
eth_getTransactionCount
eth_getBlockByNumber
eth_call
fallback native proof
```

### Generated Rank Data

```text
data/wallet-rank-summary.json
data/wallet-rank-index.json
data/rank-shards/*.json
rank-data-engine/data/latest.json
rank-data-engine/data/snapshots/*.json
```

The frontend reads generated rank data from static JSON files.

---

## Network Configuration

| Parameter | Value |
|---|---|
| Network | DAC Testnet |
| Chain ID | `21894` |
| Native Token | `DACC` |
| RPC Endpoint | `https://rpctest.dachain.tech/` |
| Explorer | `https://exptest.dachain.tech` |
| Explorer API | `https://exptest.dachain.tech/api` |
| Explorer API v2 | `https://exptest.dachain.tech/api/v2` |
| Stats Endpoint | `https://exptest.dachain.tech/api/v2/stats` |
| Transactions Endpoint | `https://exptest.dachain.tech/api/v2/transactions` |

---

## Security Model

### Wallet Check

- No wallet connection.
- No transaction signing.
- No private key access.
- No backend account.
- Public Explorer/RPC data only.

### Wallet Rank Intelligence

- Static JSON rank data.
- No private data collection.
- No IP/device-based scoring.
- No account login.
- No private key access.
- No hidden identity scoring.
- No official DAC eligibility claim.

---

## Failure Handling

The checker follows a fail-safe output model:

```text
Verified data      → full profile
Partial data       → partial profile
RPC fallback only  → limited profile
No verified data   → no score
```

Rank Intelligence follows a separate fail-safe model:

```text
Wallet indexed        → show real rank cards
Wallet not indexed    → show NaN placeholder cards
Rank data unavailable → show safe unavailable state
Backfill incomplete   → show current indexed snapshot scope
Backfill complete     → show fully synced historical scope
```

No random score, mock score, fabricated rank, or hidden placeholder analytics should be generated.

---

## Repository Structure

```text
wallet-intelligence-layer-v3/
├── .gitignore
├── README.md
├── index.html
├── wallet-intelligence.css
├── wallet-intelligence.js
├── rank-engine.js
├── assets/
│   └── WalletRankIntelligence.png
├── data/
│   ├── wallet-rank-summary.json
│   ├── wallet-rank-index.json
│   └── rank-shards/
├── scripts/
│   └── generate_rank_from_engine_data.py
└── rank-data-engine/
    ├── .gitignore
    ├── data/
    │   ├── latest.json
    │   └── snapshots/
    └── scripts/
        └── sync_rank_data_engine.py
```

Obsolete legacy rank pipeline scripts were removed after the final variable-aware rank-data-engine flow was confirmed.

---

## Local Usage

Run from the repository root:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3/
```

Example wallet:

```text
0x870ad63acc507cdfd878F170606d19ae78988AFE
```

Generate rank output locally from current engine data:

```bash
BASE="DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3"

python3 "$BASE/scripts/generate_rank_from_engine_data.py"
```

Validate generated JSON:

```bash
python3 -m json.tool "$BASE/data/wallet-rank-summary.json" >/dev/null
python3 -m json.tool "$BASE/data/wallet-rank-index.json" >/dev/null
python3 -m json.tool "$BASE/rank-data-engine/data/latest.json" >/dev/null
```

---

## Initial Release Scope

This initial release includes:

- Wallet Rank Intelligence UI.
- Rank Data Engine Status panel.
- Live DAC Testnet network snapshot.
- Variable-aware wallet rank cards.
- Indexed wallet rank state.
- Unindexed wallet placeholder state.
- Static sharded rank lookup.
- GitHub Actions rank data sync.
- Historical backfill tracking.
- Current indexed snapshot rank scope.
- Full historical completion guard.

This README does not define future roadmap items.

---

## License

This project is part of the [`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the root repository license.

---

## Author

**JERUZZALEM**  
DAC Infra Tester

Built by Communities for Communities.
