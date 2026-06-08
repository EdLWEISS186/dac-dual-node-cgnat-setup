# DAC Wallet Intelligence Layer v3.1.0

Client-side wallet intelligence interface and comparative public wallet rank signal for the **DAC Quantum Chain Testnet**.

Wallet Intelligence Layer v3.1.0 continues the Wallet Intelligence Layer series by moving v3 from a rank-intelligence interface into a more complete **data workflow**.

The project is community-built by **JERUZZALEM — DAC Infra Tester**.

> Not an official DAC product, not an official eligibility checker, not a reward checker, and not a definitive Sybil detection system.

**Live Interface**

- [Wallet Intelligence Layer v3](https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3/)

![Version](https://img.shields.io/badge/version-v3.1.0-blue?style=flat-square)
![Network](https://img.shields.io/badge/network-DAC%20testnet-yellow?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Wallet Check](https://img.shields.io/badge/wallet%20check-no%20connect%20required-brightgreen?style=flat-square)
![Rank Engine](https://img.shields.io/badge/rank%20engine-local%20RPC%20worker-orange?style=flat-square)
![Public Output](https://img.shields.io/badge/public%20output-GitHub-lightgrey?style=flat-square)

---

## Table of Contents

- [Overview](#overview)
- [v3.1.0 Update Summary](#v310-update-summary)
- [Relationship to Previous Projects](#relationship-to-previous-projects)
- [Architecture Topology](#architecture-topology)
- [Data Sources](#data-sources)
- [Rank Data Workflow](#rank-data-workflow)
- [Low-Storage Worker Model](#low-storage-worker-model)
- [Public Output Files](#public-output-files)
- [UI Changes in v3.1.0](#ui-changes-in-v310)
- [Interface Preview](#interface-preview)
- [Rank Data Status Model](#rank-data-status-model)
- [Local Development Workspace](#local-development-workspace)
- [Disclaimer](#disclaimer)
- [Security and Trust Model](#security-and-trust-model)
- [Repository Role](#repository-role)
- [Changelog](#changelog)
- [License](#license)
- [Author](#author)

---

## Overview

Wallet Intelligence Layer v3.1.0 is a DAC Testnet wallet intelligence interface focused on public wallet behavior and comparative rank signals.

The interface keeps the no-connect wallet check model from earlier Wallet Intelligence Layer versions, then adds a rank intelligence section that can compare a wallet against the currently indexed wallet population.

The core v3 direction remains:

```text
Every verified wallet variable can become a comparative public rank signal.
```

Version `v3.1.0` strengthens that direction by improving the data pipeline behind the rank layer.

Instead of relying on a GitHub Actions-centered rank sync bot, the project now uses a **local RPC rank worker** that reads from the user's DAC node setup, processes rank data locally, and publishes generated rank output back to GitHub for the static frontend.

---

## v3.1.0 Update Summary

Version `v3.1.0` is a major workflow and UI update.

The main workflow change:

```text
GitHub Actions-centered sync
↓
Local RPC-powered rank data engine
```

The main UI change:

```text
Overall Wallet Rank
↓
Separated into a highlighted final composite rank card
```

Key updates:

- Added local RPC worker-based rank data processing.
- Added primary and fallback local RPC support.
- Added historical backfill, post-backfill catch-up, and incremental sync phases.
- Added low-storage temporary worker behavior.
- Preserved GitHub as the public output layer for generated rank data.
- Updated visible UI version labels from `v3.0.0` to `v3.1.0`.
- Updated Dynamic Intelligence Badge label from `DIB-v3.0.0` to `DIB-v3.1.0`.
- Improved unindexed wallet copy to reference the local RPC rank engine.
- Separated `overall_rank` from normal rank metric cards.
- Added a full-width highlighted final composite rank card.

---

## Relationship to Previous Projects

Wallet Intelligence Layer v3.1.0 is part of a broader DAC tooling progression.

It does not replace earlier projects. It builds on the same testnet tooling path: activity generation, wallet reading, dynamic wallet status representation, and public comparative rank intelligence.

| Project | Version | Role in the Progression | Reference |
|---|---:|---|---|
| DAC Sender | `v1.4.3` | Activity-generation and testnet interaction tool. It helps create visible DAC Testnet wallet behavior. | [DAC Sender](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Sender-Web) |
| Wallet Intelligence Layer | `v1.5.4` | First wallet intelligence layer focused on reading and interpreting public DAC wallet activity. | [Wallet Intelligence Layer v1](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1) |
| Wallet Intelligence Layer | `v2.0.2` | Extended wallet intelligence into a dynamic wallet-bound status badge workflow. | [Wallet Intelligence Layer v2](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2) |
| Wallet Intelligence Layer | `v3.1.0` | Turns wallet intelligence variables into comparative public rank signals using a local RPC rank data engine. | [Wallet Intelligence Layer v3](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3) |

In short:

```text
DAC Sender
→ creates / supports wallet activity

Wallet Intelligence Layer v1
→ reads wallet activity

Wallet Intelligence Layer v2
→ represents wallet status through a dynamic badge layer

Wallet Intelligence Layer v3
→ compares wallet variables through public rank intelligence
```

---

## Architecture Topology

Wallet Intelligence Layer v3.1.0 uses a hybrid architecture.

The frontend remains a static GitHub Pages interface. The rank dataset is produced by a local RPC worker and published to GitHub as generated public JSON output.

```text
                           ┌─────────────────────────────┐
                           │       DAC Testnet Chain     │
                           └──────────────┬──────────────┘
                                          │
                                          │ RPC / Explorer reads
                                          │
          ┌───────────────────────────────┴───────────────────────────────┐
          │                                                               │
          ▼                                                               ▼
┌───────────────────────┐                                     ┌───────────────────────┐
│ Official DAC Explorer │                                     │ Local DAC RPC Nodes   │
│ Explorer API / Stats  │                                     │ Primary + Fallback    │
└───────────┬───────────┘                                     └───────────┬───────────┘
            │                                                             │
            │ Live public wallet/network reads                            │ Local block + tx reads
            │                                                             │
            ▼                                                             ▼
┌────────────────────────────────┐                           ┌────────────────────────────────┐
│ Wallet Intelligence Layer UI   │                           │ Local RPC Rank Worker          │
│ Static frontend / GitHub Pages │                           │ Backfill / Catch-up / Sync     │
└───────────────┬────────────────┘                           └───────────────┬────────────────┘
                │                                                            │
                │ Reads generated rank JSON                                  │ Writes generated rank JSON
                │                                                            │
                ▼                                                            ▼
        ┌────────────────────────────────────────────────────────────────────────┐
        │ GitHub Repository Public Output Layer                                  │
        │ latest.json / wallet-rank-summary.json / wallet-rank-index.json        │
        │ rank-shards/*.json                                                     │
        └────────────────────────────────────────────────────────────────────────┘
```

The architecture separates responsibilities:

| Layer | Responsibility |
|---|---|
| Static UI | User input, wallet profile display, live network context, rank rendering |
| Official Explorer/API | Public indexed DAC Testnet data where available |
| Local RPC Nodes | Local block, transaction, and balance reads for rank data processing |
| Local RPC Worker | Historical backfill, catch-up, incremental processing, rank JSON generation |
| GitHub Repository | Public generated output layer consumed by the static UI |
| Sparse DEV workspace | Lightweight local development without pulling heavy generated data |

---

## Data Sources

The project uses public and node-derived DAC Testnet data.

### Official DAC RPC

```text
https://rpctest.dachain.tech/
```

Used for public RPC reads where applicable.

### Official DAC Explorer

```text
https://exptest.dachain.tech
```

Used as the public DAC Testnet explorer reference.

### Official DAC Explorer API

```text
https://exptest.dachain.tech/api
```

Used where explorer-indexed public wallet, transaction, address, or network data is available.

### Local DAC RPC Nodes

The v3.1.0 rank workflow uses the user's local DAC node setup as the main worker input.

Typical local RPC sources:

```text
Primary local RPC:
http://127.0.0.1:8546

Fallback local RPC:
http://192.168.100.7:8545
```

The local RPC worker uses these sources to process historical and incremental chain data for rank generation.

### Generated GitHub Rank Data

The static frontend reads generated rank outputs from the repository.

```text
rank-data-engine/data/latest.json
data/wallet-rank-summary.json
data/wallet-rank-index.json
data/rank-shards/*.json
```

These files are generated outputs, not manually authored source files.

---

## Rank Data Workflow

The v3.1.0 workflow is designed around three sync phases.

### 1. Historical Backfill

The worker starts from a fixed historical anchor and processes blocks backward toward genesis.

```text
historical_backfill_anchor_block
↓
genesis
```

During this phase, the UI can display the current indexed snapshot, but it should not imply that the rank dataset is fully complete.

### 2. Post-Backfill Catch-Up

While historical backfill is running, new blocks continue to appear on the chain.

To avoid a data gap, v3.1.0 includes a catch-up phase:

```text
historical_backfill_anchor_block + 1
↓
latest chain head
```

This fills the range created while the historical backfill was still running.

### 3. Incremental Sync

After historical backfill and catch-up are complete, the worker enters incremental mode.

```text
last processed block + 1
↓
latest block
```

At this stage, the rank engine only processes new blocks as they appear.

---

## Low-Storage Worker Model

The local worker is designed to avoid permanent local storage growth from temporary processing folders.

The worker flow:

```text
Create temporary workspace in /tmp
↓
Clone latest repository state
↓
Read local RPC data
↓
Generate rank outputs
↓
Commit and push generated outputs to GitHub
↓
Remove temporary workspace
```

This keeps the user's local machine from storing every temporary worker clone permanently.

For daily development, a separate sparse / partial clone can be used so heavy generated rank data is not pulled into the local development workspace.

---

## Public Output Files

The following generated files are part of the public rank output layer:

```text
wallet-intelligence-layer-v3/
├── data/
│   ├── wallet-rank-summary.json
│   ├── wallet-rank-index.json
│   └── rank-shards/
│       └── *.json
└── rank-data-engine/
    └── data/
        └── latest.json
```

Output role:

| Output | Purpose |
|---|---|
| `latest.json` | Latest local RPC worker snapshot and sync state |
| `wallet-rank-summary.json` | Summary metadata for the current rank dataset |
| `wallet-rank-index.json` | Rank index metadata / compatibility output |
| `rank-shards/*.json` | Sharded rank lookup data for frontend wallet checks |

---

## UI Changes in v3.1.0

The v3.1.0 UI update improves how Wallet Rank Intelligence is presented.

### Version Labels

Visible version labels were updated:

```text
Wallet Intelligence Layer v3.0.0
↓
Wallet Intelligence Layer v3.1.0
```

Dynamic Intelligence Badge label:

```text
DIB-v3.0.0
↓
DIB-v3.1.0
```

### Rank Card Layout

Before v3.1.0, `overall_rank` appeared as part of the normal metric card grid.

In v3.1.0, `overall_rank` is separated into a full-width final composite card.

```text
Metric rank cards
├── Transaction Rank
├── Gas Used Rank
├── Native Volume Rank
└── Other available rank variables

Final composite card
└── Overall Wallet Rank
```

### Overall Wallet Rank

The Overall Wallet Rank now has its own highlighted UI treatment.

It is presented as the final composite signal derived from the available indexed rank variables.

The UI uses a dedicated visual label:

```text
FINAL COMPOSITE RANK
```

This makes the hierarchy clearer:

```text
Individual variables
↓
Rank metric cards

Composite result
↓
Overall Wallet Rank
```

### Unindexed Wallet Copy

The unindexed wallet state now better reflects the new data workflow.

The UI explains that the wallet may already have live wallet intelligence data, while rank values may still be unavailable in the current indexed snapshot because the local RPC rank engine is still processing historical backfill.

---

## Interface Preview

The Wallet Rank Intelligence section is expected to look similar to the current project.

![Wallet Rank Intelligence](assets/WalletRankIntelligence.png)

---

## Rank Data Status Model

The UI should distinguish between live network visibility and rank dataset completeness.

| State | Meaning |
|---|---|
| `HISTORICAL_BACKFILL_IN_PROGRESS` | The engine is still processing historical blocks toward genesis. |
| `POST_BACKFILL_CATCH_UP` | Historical backfill has reached genesis and the engine is filling the gap from anchor + 1 to latest. |
| `INCREMENTAL` | The engine has caught up and is processing new blocks incrementally. |

The project should only imply a fully synced rank dataset after historical backfill and catch-up are complete.

---

## Local Development Workspace

Because generated rank output can become large, the recommended local development approach is to use a sparse / partial clone.

The development workspace can exclude generated files such as:

```text
data/rank-shards/
data/wallet-rank-index.json
data/wallet-rank-summary.json
data/indexer-work/
rank-data-engine/data/
```

This keeps daily UI, README, script, and workflow editing lightweight while allowing GitHub to remain the public output layer.

---

## Disclaimer

Wallet Intelligence Layer v3.1.0 is a **community-built engineering tool**.

Although the project uses official DAC Testnet-facing sources where applicable, including official RPC and Explorer/API endpoints, some interpretation layers are custom developer logic.

This includes, but is not limited to:

```text
rank variable modeling
wallet metric aggregation
backfill and catch-up workflow design
rank shard formatting
UI status interpretation
composite rank presentation
```

The output should be treated as a transparent community analytics layer, not as an official DAC score, reward system, eligibility checker, or final Sybil judgment.

The project is built for testnet observation, public-data debugging, infrastructure testing, wallet behavior review, and community intelligence.

---

## Security and Trust Model

Wallet Intelligence Layer v3.1.0 keeps the same safety principles as earlier versions:

```text
No private key handling
No forced wallet connection for checking
No backend account system
No custody
No hidden eligibility claim
No official reward claim
No fabricated score output
```

The interface reads public DAC Testnet data and generated public rank data.

The rank worker reads local/public chain data and writes generated JSON outputs. It does not require private keys for the wallet intelligence check flow.

---

## Repository Role

This project is part of the larger:

```text
dac-dual-node-cgnat-setup
```

repository.

The v3.1.0 folder contains the frontend UI, rank engine integration, data worker scripts, and generated public rank outputs used by the Wallet Rank Intelligence section.

---

## Changelog

### v3.1.0 — Local RPC Rank Workflow and UI Rank Layout

- Added local RPC rank worker workflow.
- Added primary/fallback local RPC source support.
- Added historical backfill mode.
- Added post-backfill catch-up mode.
- Added incremental sync mode.
- Added low-storage temporary worker execution model.
- Preserved GitHub as the public generated-data output layer.
- Updated visible UI version labels to `v3.1.0`.
- Updated Dynamic Intelligence Badge label to `DIB-v3.1.0`.
- Improved unindexed rank wording to reference the local RPC rank engine.
- Separated `overall_rank` from standard metric cards.
- Added highlighted full-width Overall Wallet Rank card.
- Added final composite rank visual treatment.

### v3.0.0 — Wallet Rank Intelligence Foundation

- Introduced Wallet Rank Intelligence as the v3 direction.
- Added comparative public rank concept for verified wallet variables.
- Added rank summary and rank index foundations.
- Added sharded frontend rank lookup support.
- Added partial rank rendering behavior.
- Added placeholder rank states while valid rank data is pending.

---

## License

This project is part of the [`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the root repository license.

---

## Author

**JERUZZALEM**  
DAC Infra Tester

Built by Communities for Communities.
