# DAC Wallet Intelligence Layer v3.6.0

Client-side wallet intelligence interface and globally comparative public wallet rank system for the **DAC Quantum Chain Testnet**.

Wallet Intelligence Layer v3.6.0 is the **Back to Normal** release. It restores the normal WIL scoring model after the official DAC Testnet Inception Conviction Lock flow became inconsistent as an active scoring basis.

The project is community-built by **JERUZZALEM — DAC Infra Tester**.

> Not an official DAC product, not an official eligibility checker, not a reward checker, and not a definitive Sybil detection system.

**Live Interface**

- [Wallet Intelligence Layer v3](https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3/)

![Version](https://img.shields.io/badge/version-v3.6.0-blue?style=flat-square)
![Release](https://img.shields.io/badge/release-back%20to%20normal-brightgreen?style=flat-square)
![Network](https://img.shields.io/badge/network-DAC%20testnet-yellow?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Wallet Check](https://img.shields.io/badge/wallet%20check-no%20connect%20required-brightgreen?style=flat-square)
![State Backend](https://img.shields.io/badge/state-SQLite-orange?style=flat-square)
![Rank Schema](https://img.shields.io/badge/rank%20schema-Compact%20V3-informational?style=flat-square)
![Public Output](https://img.shields.io/badge/public%20output-GitHub-lightgrey?style=flat-square)

---

## Table of Contents

- [Overview](#overview)
- [v3.6.0 Update Summary](#v360-update-summary)
- [Release Notes](#release-notes)
- [Relationship to Previous Projects](#relationship-to-previous-projects)
- [Architecture Topology](#architecture-topology)
- [Data Sources](#data-sources)
- [Authoritative SQLite State](#authoritative-sqlite-state)
- [Rank Data Workflow](#rank-data-workflow)
- [Low-Storage Worker Model](#low-storage-worker-model)
- [Global Rank Builder](#global-rank-builder)
- [Compact Public Rank Schema V3](#compact-public-rank-schema-v3)
- [Ranking Model](#ranking-model)
- [Dynamic Intelligence Badge](#dynamic-intelligence-badge)
- [Official Rank Signal](#official-rank-signal)
- [Dedicated Rank Publisher](#dedicated-rank-publisher)
- [Public Output Files](#public-output-files)
- [UI Architecture](#ui-architecture)
- [Rank Data Status Model](#rank-data-status-model)
- [Google Drive Backup Layer](#google-drive-backup-layer)
- [Local Development Workspace](#local-development-workspace)
- [Security and Trust Model](#security-and-trust-model)
- [Validation Status](#validation-status)
- [Changelog](#changelog)
- [License](#license)
- [Author](#author)

---

## Overview

Wallet Intelligence Layer v3.6.0 is a DAC Testnet wallet intelligence and comparative ranking system using a static browser interface, locally indexed rank state, compact public rank artifacts, and a no-wallet-connect check flow.

The v3.6.0 release returns WIL to the normal wallet-quality scoring model:

```text
Current Native Funds
+
Current DACC Stake
+
Transaction activity
+
NFT signals
+
DAC Inception Rank
```

The v3.5.0 Conviction/cutoff model is preserved as historical work, but it is no longer treated as the active scoring or public rank signal.

The core v3 principle remains:

```text
Every verified wallet variable can become a comparative public rank signal.
```

The browser does not calculate a global wallet rank from isolated wallet data. Global rank is precomputed from the indexed wallet population, published as compact rank artifacts, and retrieved by the UI through an address-prefix shard.

```text
Full indexed population
↓
Global comparative rank calculation
↓
Compact public rank records
↓
Address-prefix shards
↓
Browser wallet lookup
```

The shard is only a delivery format. The comparison population remains global.

---

## v3.6.0 Update Summary

Version `v3.6.0` is the **Back to Normal** release.

This release is documented as:

```text
Back to Normal — inconsistent Conviction by Official DAC Team
```

The reason for the rollback is that the official DAC Testnet Inception Conviction Lock flow was removed from the web testnet path and previously locked funds were refunded. Because of that, Conviction/cutoff scoring is no longer a reliable active scoring basis for WIL.

The v3.6.0 update restores:

```text
Native Funds Before Conviction
↓
Current Native Funds
```

```text
Estimated Stake Before Conviction + Conviction Locked
↓
Current DACC Stake
```

```text
Conviction-aware reputation model
↓
Normal wallet-quality reputation model
```

Key updates:

- Updated WIL web labels to `Wallet Intelligence Layer v3.6.0`.
- Updated policy label to `WIL-v3.6.0`.
- Updated model label to `wallet-quality-scoring-v3.6.0-normal`.
- Updated Dynamic Intelligence Badge label to `DIB-v3.6.0`.
- Updated Explorer-only Sybil Heuristics label to `EOH-v3.6.0`.
- Removed Conviction Locked from active scoreboard/UI output.
- Removed Conviction Timeliness from active badge metadata.
- Restored Native Funds Score to current live native DACC balance.
- Restored DACC Stake Score to normal current stake flow.
- Restored stake classifier to `STAKE_FLOW_CLASSIFIER`.
- Normalized public worker staking metadata to `ESTIMATED_CURRENT_STAKE`.
- Normalized public worker staking source to `DAC_STAKE_UNSTAKE_TRANSACTION_FLOW`.
- Updated rank publisher and snapshot metadata to v3.6.0.
- Disabled active Conviction worker processing with `CONVICTION_METRICS_ACTIVE = False`.
- Preserved legacy SQLite Conviction tables for backward compatibility only.
- Preserved Dynamic Intelligence Badge monotonic progression.
- Added legacy localStorage fallback so v3.6.0 respects preserved badge tier state from v3.5.0.

Active v3.6.0 scoring anchors:

```text
CURRENT_NATIVE_FUNDS
CURRENT_DACC_STAKE
STAKE_FLOW_CLASSIFIER
ESTIMATED_CURRENT_STAKE
DAC_STAKE_UNSTAKE_TRANSACTION_FLOW
```

Deprecated as active scoring/UI signals:

```text
Native Funds Before Conviction
Estimated Stake Before Conviction
Conviction Locked
Conviction Timeliness
Conviction cutoff scoring
first-lock timing multiplier
post-cutover Conviction rank signal
```

Important compatibility note:

Some internal historical field names may remain for compact schema compatibility, such as:

```text
estimated_stake_before_conviction
conviction_metrics
conviction_lock_events
conviction_locked_wei
```

In v3.6.0, these are not promoted as active scoring labels. For example, the public rank UI displays the compatibility stake key as:

```text
DACC Stake
```

---

## Release Notes

Versions `v3.0.0` through `v3.2.0` were experimental/beta releases. They document the architecture evolution that led to the mature v3 implementation.

```text
v3.0.0 — GitHub Actions prototype
v3.1.0 — Local node processing
v3.2.0 — Externalized state and Google Drive backup
v3.3.0 — Stable SQLite-backed production architecture
v3.4.0 — Worker Acceleration & Operational Hardening
v3.5.0 — Conviction-aware web, worker, and Compact V3 public rank schema
v3.6.0 — Back to Normal scoring after official Conviction flow inconsistency
```

Version `v3.6.0` keeps the v3.3.0/v3.4.0 architecture but returns the active logic to normal scoring because the official Conviction flow was removed/refunded and became unsuitable as an active score signal.

“Production-ready” refers to the completed and validated architecture. Rank completeness still follows the current synchronization phase. During historical backfill or catch-up, the UI must not imply that the full chain population is already finalized.

---

## Relationship to Previous Projects

Wallet Intelligence Layer v3.6.0 is part of a broader DAC tooling progression.

| Project | Version | Role in the Progression | Reference |
|---|---:|---|---|
| DAC Sender | `v1.4.3` | Activity-generation and testnet interaction tool. | [DAC Sender](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Sender-Web) |
| Wallet Intelligence Layer | `v1.5.4` | First wallet intelligence layer focused on reading public DAC wallet activity. | [Wallet Intelligence Layer v1](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1) |
| Wallet Intelligence Layer | `v2.0.2` | Dynamic wallet-bound status badge workflow. | [Wallet Intelligence Layer v2](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2) |
| Wallet Intelligence Layer | `v3.6.0` | Global comparative wallet intelligence using local DAC nodes, SQLite state, Compact V3 rank artifacts, normal current-funds/current-stake scoring, and public shard lookup. | [Wallet Intelligence Layer v3](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3) |

```text
DAC Sender
→ creates / supports wallet activity

Wallet Intelligence Layer v1
→ reads wallet activity

Wallet Intelligence Layer v2
→ represents wallet status through a dynamic badge layer

Wallet Intelligence Layer v3
→ compares wallet variables across the indexed population
```

---

## Architecture Topology

Wallet Intelligence Layer v3.6.0 uses the hybrid local-processing and public-delivery architecture established in v3.3.0.

```text
                           ┌──────────────────────────────┐
                           │      DAC Testnet Chain       │
                           └──────────────┬───────────────┘
                                          │
                       ┌──────────────────┴──────────────────┐
                       │                                     │
                       ▼                                     ▼
          ┌────────────────────────┐             ┌────────────────────────┐
          │ Linux DAC Node in WSL  │             │ Windows DAC Node       │
          │ Primary local RPC      │             │ Fallback local RPC     │
          │ 127.0.0.1:8546         │             │ 192.168.100.7:8545     │
          └────────────┬───────────┘             └────────────┬───────────┘
                       │                                      │
                       └──────────────────┬───────────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ Local RPC Rank Worker        │
                           │ Backfill / Catch-up / Sync   │
                           │ v3.6.0 normal mode           │
                           └──────────────┬───────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ Authoritative SQLite State   │
                           │ wallet / stake / NFT / sync  │
                           │ legacy compatibility state   │
                           └───────────┬───────────┬──────┘
                                       │           │
                       ┌───────────────┘           └────────────────┐
                       ▼                                            ▼
          ┌──────────────────────────┐               ┌──────────────────────────┐
          │ Consistent GDrive Backup │               │ Global Rank Builder      │
          │ Drive A / Drive B        │               │ Full population compare  │
          └──────────────────────────┘               └─────────────┬────────────┘
                                                                   ▼
                                                    ┌──────────────────────────┐
                                                    │ Compact V3 Rank Artifacts│
                                                    │ summary / index / shards │
                                                    │ normal public signals    │
                                                    └─────────────┬────────────┘
                                                                   ▼
                                                    ┌──────────────────────────┐
                                                    │ Snapshot Publisher       │
                                                    │ wil-v3-rank-data branch  │
                                                    └─────────────┬────────────┘
                                                                   ▼
                                                    ┌──────────────────────────┐
                                                    │ Static UI / GitHub Pages │
                                                    │ rank-engine.js lookup    │
                                                    │ Compact V2/V3 decoder    │
                                                    └──────────────────────────┘
```

---

## Data Sources

The project uses public and node-derived DAC Testnet data.

### Official DAC RPC

```text
https://rpctest.dachain.tech/
```

### Official DAC Explorer

```text
https://exptest.dachain.tech
```

### Official DAC Explorer API

```text
https://exptest.dachain.tech/api
```

### Local DAC RPC Nodes

```text
Primary:
http://127.0.0.1:8546

Fallback:
http://192.168.100.7:8545
```

Expected chain ID:

```text
0x5586
```

### Current DACC Stake Flow

v3.6.0 uses normal stake/unstake flow for current DACC stake estimation.

```text
staking_metric = ESTIMATED_CURRENT_STAKE
staking_source = DAC_STAKE_UNSTAKE_TRANSACTION_FLOW
```

Browser classifier:

```text
STAKE_FLOW_CLASSIFIER
Estimated Current Stake = totalStakeIn - totalUnstakeOut
```

### Legacy Conviction Data

Legacy Conviction tables may remain in SQLite for backward compatibility with v3.5.0 state.

In v3.6.0, Conviction is not an active public scoring or rank signal.

```text
CONVICTION_METRICS_ACTIVE = False
```

---

## Authoritative SQLite State

The active heavy state is stored outside GitHub:

```text
~/wil-v3-rank-state/wil-v3-rank-state.sqlite
```

SQLite is the source of truth for the v3.6.0 rank worker.

Principal logical tables include:

```text
wallet_metrics
staking_metrics
official_inception_nft_tokens
checkpoint
counters
state_meta
enrichment_queue
official_inception_nft_repair_state
```

Legacy compatibility tables may also exist:

```text
conviction_lock_events
conviction_metrics
```

These legacy tables are retained to avoid breaking historical state, but Conviction is not active in v3.6.0 scoring.

---

## Rank Data Workflow

The main worker uses three synchronization phases.

| Phase | Meaning |
|---|---|
| Historical Backfill | Processes historical blocks backward toward genesis. |
| Post-Backfill Catch-Up | Fills the forward gap created while backfill was running. |
| Incremental Sync | Processes newly produced blocks only. |

Worker responsibilities in v3.6.0:

- block transactions;
- senders and recipients;
- native-value flow;
- gas usage;
- wallet activity counters;
- NFT activity;
- collection diversity;
- stake and unstake flow;
- Official Inception NFT `Transfer` logs;
- checkpoint and phase transitions.

Lightweight status may include sync phase, last synced block, next backfill block, latest chain block at sync, indexed wallet count, total processed transactions, state backend, feature support flags, and public rank readiness.

Global rank generation is handled separately.

---

## Low-Storage Worker Model

The project follows an explicit low-storage lifecycle:

```text
input
↓
temporary working area
↓
process and validate
↓
publish or persist output
↓
remove temporary work
```

Temporary work may include a temporary repository clone, a consistent source database snapshot, a temporary rank-build database, a temporary snapshot repository, compressed backup work, and temporary manifests.

This design keeps daily source work lightweight and prevents generated operational data from being accidentally committed.

---

## Global Rank Builder

The global rank builder is:

```text
scripts/generate_rank_from_sqlite.py
```

It reads a consistent snapshot of the complete SQLite population.

The builder:

1. creates a consistent source snapshot;
2. streams wallet metrics into a temporary rank-build database;
3. joins stake metrics as DACC Stake;
4. counts current Official NFT ownership;
5. computes global metric ranks;
6. computes the Final Composite Rank;
7. creates compact records;
8. splits records into prefix shards;
9. writes summary and index metadata;
10. validates the rank-build database;
11. removes temporary builder work.

Rank calculation occurs before sharding. A wallet stored in `ab.json` is still ranked against the complete indexed population, not only against addresses beginning with `0xab`.

---

## Compact Public Rank Schema V3

v3.6.0 keeps Compact V3 delivery:

```text
WIL_V3_COMPACT_ARRAY_V3
SHARDED_COMPACT_V3
```

However, v3.6.0 no longer promotes Conviction Locked as an active comparative signal.

The stake compatibility key may remain:

```text
estimated_stake_before_conviction
```

but in v3.6.0 it is displayed as:

```text
DACC Stake
```

Active comparative signals include:

```text
native_funds
DACC Stake
transactions
native_volume
gas_used
nft_holdings
collection_diversity
reputation_score
low_sybil_risk
official_inception_nfts
overall_rank
```

The reader supports:

```text
WIL_V3_COMPACT_ARRAY_V2
WIL_V3_COMPACT_ARRAY_V3
```

Older snapshots remain readable, while v3.6.0 displays active labels according to the normal scoring model.

---

## Ranking Model

WIL v3.6.0 separates two related but different concepts:

```text
Global comparative public rank
→ precomputed from the full indexed wallet population

Live wallet reputation score
→ computed in the browser from the checked wallet's verified data
```

### Comparative rank cards

v3.6.0 exposes normal comparative wallet signals, including:

```text
Native Funds
DACC Stake
Transactions
Native Volume
Gas Used
NFT Holdings
Collection Diversity
Reputation Score
Low-Risk Profile
Official Rank Signal
Final Composite Rank
```

Old active labels removed from the UI:

```text
Estimated Stake Before Conviction
Conviction Locked
```

### Final Composite Rank

The Final Composite Rank remains the preserved eight-variable global rank formula from the stable v3 architecture.

Final Composite Rank inputs:

1. Native Funds
2. Transactions
3. Gas Used
4. Native Volume
5. NFT Holdings
6. Collection Diversity
7. Reputation Score
8. Low-Risk Profile

DACC Stake and Official Testnet Inception NFTs are displayed separately and are not merged into the preserved Final Composite Rank formula.

### Live Reputation Scoring Layer

| Component | Max Points | v3.6.0 interpretation |
|---|---:|---|
| Transaction Score | 20 | Wallet activity volume |
| NFT Diversity Score | 10 | Number of distinct NFT collections |
| NFT Holdings Score | 10 | Total NFT holdings |
| Native Funds Score | 15 | Current native DACC balance |
| DACC Stake Score | 20 | Current DACC Stake from normal stake/unstake flow |
| DAC Inception Rank Score | 25 | DAC Inception Rank NFT signal |
| **Total** | **100** | Community-defined wallet-quality score |

Native Funds scoring mode:

```text
CURRENT_NATIVE_FUNDS
```

DACC Stake scoring mode:

```text
CURRENT_DACC_STAKE
```

---

## Dynamic Intelligence Badge

The Dynamic Intelligence Badge follows monotonic progression behavior in v3.6.0.

A badge update is offered only when the newly calculated tier is higher than the highest known tier already achieved.

This means:

- a wallet can move upward;
- a wallet is not downgraded;
- an update is not offered for the same or lower tier;
- the highest known badge tier is preserved locally.

v3.6.0 also reads v3.5.0 preserved badge state as a fallback.

Local preserved badge keys:

```text
wil:v3.6.0:highestBadgeClass:<wallet>
wil:v3.5.0:highestBadgeClass:<wallet>
```

Active badge engine label:

```text
DIB-v3.6.0
```

---

## Official Rank Signal

Official Testnet Inception NFT contract:

```text
0xB36ab4c2Bd6aCfC36e9D6c53F39F4301901Bd647
```

The worker tracks ERC-721 `Transfer` logs and stores the latest owner for each token.

The Official Rank Signal is derived from the wallet's current token count.

| NFT Count | Official Rank |
|---:|---|
| 0 | NONE |
| 1 | CADET |
| 2 | COMMANDO |
| 3 | SEAL |
| 4 | SHADOW UNIT |
| 5 | VANGUARD |
| 6 | SENTINEL |
| 7 | SOVEREIGN |
| 8 | WARRIOR |
| 9 | ARCHITECT |
| 10 | INTERCEPTOR |
| 11 | PHANTOM |
| 12 | CIPHER |
| 13 or more | CROWN |

This is an independent official ecosystem signal. It is not merged into the Final Composite Rank formula.

---

## Dedicated Rank Publisher

The publisher is:

```text
scripts/publish_rank_snapshot_branch.sh
```

It validates configuration, creates isolated temporary work, runs the global rank builder, validates Compact V3 metadata, validates shard completeness, creates a clean snapshot repository, creates one snapshot commit, optionally pushes the public snapshot branch, and removes temporary work.

Public rank branch:

```text
wil-v3-rank-data
```

Safety rules prevent incomplete snapshots, limited test snapshots, or temporary fixture data from becoming production output.

---

## Public Output Files

Public rank artifacts:

```text
wallet-intelligence-layer-v3/
└── data/
    ├── wallet-rank-summary.json
    ├── wallet-rank-index.json
    └── rank-shards/
        ├── 00.json
        ├── 01.json
        ├── ...
        └── ff.json
```

The authoritative SQLite database is not published to GitHub.

---

## UI Architecture

The UI version is:

```text
Wallet Intelligence Layer v3.6.0
DIB-v3.6.0
EOH-v3.6.0
```

Browser lookup flow:

1. normalize the address;
2. load the public rank summary;
3. load the rank index;
4. derive the address prefix;
5. fetch the matching rank shard;
6. decode metric values and ranks;
7. render the Wallet Rank Intelligence section.

Expected v3.6.0 UI labels:

```text
Wallet Intelligence Layer v3.6.0
WIL-v3.6.0
wallet-quality-scoring-v3.6.0-normal
DIB-v3.6.0
EOH-v3.6.0
Native Funds Score
DACC Stake Score
CURRENT_NATIVE_FUNDS
CURRENT_DACC_STAKE
STAKE_FLOW_CLASSIFIER
```

The v3.6.0 web UI should not show the old Conviction-era active labels:

```text
Conviction Locked
Conviction Timeliness
Native Funds Before Conviction
Estimated Stake Before Conviction
before Conviction
Conviction cutover
cutoff-aware
postCutover
```

---

## Rank Data Status Model

| State | Meaning |
|---|---|
| `HISTORICAL_BACKFILL_IN_PROGRESS` | The worker is processing historical blocks backward toward genesis. |
| `POST_BACKFILL_CATCH_UP` | Historical backfill reached genesis and the worker is filling the forward gap. |
| `INCREMENTAL` | The worker has caught up and is processing newly produced blocks. |

The UI should only imply a fully synchronized rank dataset after historical backfill and catch-up are complete.

---

## Google Drive Backup Layer

The heavy SQLite state is backed up locally through `rclone`.

Configured remotes:

```text
gdrive_wil_a:
gdrive_wil_b:
```

Backup cadence:

```text
0 */6 * * *
```

GitHub does not upload the heavy state to Google Drive. The local environment performs backups. GitHub stores source and public rank artifacts; Google Drive stores external heavy-state recovery snapshots.

---

## Local Development Workspace

Canonical repository:

```text
https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup
```

Daily working clone:

```text
~/dac-contribution/DEV-SPACE
```

WIL project source:

```text
DAC-Contributions/
└── dac-wallet-intelligence-layer/
    └── wallet-intelligence-layer-v3/
```

Heavy operational state is outside the repository:

```text
~/wil-v3-rank-state/
```

Worker and benchmark logs are outside the repository:

```text
~/wil-v3-worker-logs/
```

Explicit file staging is preferred over broad commands such as:

```text
git add .
```

---

## Security and Trust Model

Wallet Intelligence Layer v3.6.0 keeps the same safety principles as earlier versions:

```text
No private key handling
No forced wallet connection for checking
No backend account system
No custody
No hidden eligibility claim
No official reward claim
No fabricated score output
```

The wallet check flow uses public DAC Testnet information and public rank artifacts.

The local worker reads blockchain data and updates local intelligence state. It does not require private keys for wallet checking.

The system should be treated as a transparent community analytics layer, not an official DAC scoring or eligibility system.

---

## Validation Status

The v3.6.0 code update was validated before commit and push.

Validated commit:

```text
bc7baa8 Update WIL v3.6.0 back to normal scoring
```

Validation commands:

```text
python3 -m py_compile scripts/generate_rank_from_sqlite.py
python3 -m py_compile rank-data-engine/scripts/local_rpc_rank_data_worker.py
python3 -m py_compile rank-data-engine/scripts/sqlite_rank_state.py
bash -n scripts/publish_rank_snapshot_branch.sh
bash -n rank-data-engine/scripts/run_local_rpc_rank_worker_low_storage.sh
node --check wallet-intelligence.js
node --check rank-engine.js
git diff --check
```

Validated results:

```text
py_compile_all_exit_code=0
publish_bash_check_exit_code=0
runner_bash_check_exit_code=0
wallet_js_node_check_exit_code=0
rank_engine_node_check_exit_code=0
diff_check_exit_code=0
commit_exit_code=0
push_exit_code=0
```

v3.6.0 browser validation confirmed:

- header shows `Wallet Intelligence Layer v3.6.0`;
- policy label shows `WIL-v3.6.0`;
- policy engine shows `wallet-quality-scoring-v3.6.0-normal`;
- Conviction Locked card is removed;
- Native Funds Score uses current native balance;
- DACC Stake Score uses current stake flow;
- Wallet Rank Intelligence shows `DACC Stake`;
- Wallet Rank Intelligence no longer shows `Estimated Stake Before Conviction`;
- Wallet Rank Intelligence no longer shows `Conviction Locked`;
- Dynamic Intelligence Badge still only offers update when tier increases.

---

## Changelog

### v3.6.0 — Back to Normal Scoring

- Restored normal Native Funds Score using current live native DACC balance.
- Restored normal DACC Stake Score using current stake/unstake flow.
- Removed Conviction Locked from active web UI.
- Removed Conviction Timeliness from active DIB metadata.
- Removed Conviction/cutoff scoring from active reputation logic.
- Normalized public rank UI stake label to `DACC Stake`.
- Removed visible `Estimated Stake Before Conviction` and `Conviction Locked` labels from Wallet Rank Intelligence.
- Updated WIL web label to `v3.6.0`.
- Updated policy label to `WIL-v3.6.0`.
- Updated scoring model to `wallet-quality-scoring-v3.6.0-normal`.
- Updated Dynamic Intelligence Badge label to `DIB-v3.6.0`.
- Updated Explorer-only Sybil Heuristics label to `EOH-v3.6.0`.
- Preserved Dynamic Intelligence Badge monotonic update behavior.
- Added v3.5.0 localStorage fallback for preserved badge tier.
- Updated worker public status version to `v3.6.0`.
- Updated rank publisher version to `v3.6.0`.
- Updated public worker staking metadata to `ESTIMATED_CURRENT_STAKE`.
- Updated public worker staking source to `DAC_STAKE_UNSTAKE_TRANSACTION_FLOW`.
- Disabled active Conviction worker processing with `CONVICTION_METRICS_ACTIVE = False`.
- Preserved legacy Conviction SQLite state only for backward compatibility.
- Documented the release as `Back to Normal — inconsistent Conviction by Official DAC Team`.

### v3.5.0 — Conviction-aware Web Schema

- Added Compact V3 public rank records.
- Added Conviction Locked as a comparative public rank metric.
- Renamed the stake-era metric to Estimated Stake Before Conviction.
- Added Conviction cutover metadata to public rank summary output.
- Added Conviction SQLite event and aggregate state.
- Preserved backward-compatible Compact V2 browser decoding.
- Completed Conviction-aware live reputation scoring.
- Added monotonic Dynamic Intelligence Badge behavior.

### v3.4.0 — Worker Acceleration & Operational Hardening

- Optimized Local RPC worker counterparty tracking.
- Improved historical backfill throughput through sorted counterparty lookup.
- Benchmarked production worker presets.
- Added backup wrapper cleanup after successful Google Drive upload.
- Added terminal phase monitoring.

### v3.3.0 — Stable

- Introduced the LiteSQLite architecture.
- Introduced compact public rank sharding for browser lookup.
- Finalized the global rank builder.
- Finalized the dedicated public snapshot publisher.
- Added Estimated Current Stake.
- Added Official Testnet Inception NFT ownership tracking.
- Added consistent compressed SQLite backup to Google Drive A/B.
- First production-ready v3 release.

### v3.2.0 — Beta

- Introduced the Google Drive storage backend.
- Externalized heavy rank state outside GitHub.
- Added Google Drive A/B rollover behavior.

### v3.1.0 — Beta

- Switched processing to Local Node.
- Added Linux primary and Windows fallback RPC sources.
- Added historical backfill, post-backfill catch-up, and incremental phases.

### v3.0.0 — Beta

- Initial rewrite using GitHub Actions.
- Introduced Wallet Rank Intelligence as the v3 direction.
- Added the global comparative rank concept.

---

## License

This project is part of the [`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the root repository license.

---

## Author

**JERUZZALEM**  
DAC Infra Tester

Built by Communities for Communities.
