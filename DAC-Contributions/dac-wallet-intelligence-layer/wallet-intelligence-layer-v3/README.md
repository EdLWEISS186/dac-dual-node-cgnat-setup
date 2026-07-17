# DAC Wallet Intelligence Layer v3.7.0

Client-side wallet intelligence interface and globally comparative
public wallet rank system for the **DAC Quantum Chain Testnet**.

Wallet Intelligence Layer v3.7.0 is the **Parity-Safe Rebuild** release.
It rebuilds the local SQLite rank state from a deterministic anchor with
explicit block-coverage and transaction-ledger guards so WIL cannot
silently claim full sync while missing block or transaction data.

The project is community-built by **JERUZZALEM --- DAC Infra Tester**.

> Not an official DAC product, not an official eligibility checker, not
> a reward checker, and not a definitive Sybil detection system.

**Live Interface**

-   [Wallet Intelligence Layer
    v3](https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3/)

![Version](https://img.shields.io/badge/version-v3.7.0-blue?style=flat-square)
![Release](https://img.shields.io/badge/release-parity--safe%20rebuild-brightgreen?style=flat-square)
![Network](https://img.shields.io/badge/network-DAC%20testnet-yellow?style=flat-square)
![Chain
ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Wallet
Check](https://img.shields.io/badge/wallet%20check-no%20connect%20required-brightgreen?style=flat-square)
![State
Backend](https://img.shields.io/badge/state-SQLite-orange?style=flat-square)
![Rank
Schema](https://img.shields.io/badge/rank%20schema-Compact%20V3-informational?style=flat-square)
![Backup](https://img.shields.io/badge/backup-GDrive%20rollover-lightgrey?style=flat-square)
![Public
Output](https://img.shields.io/badge/public%20output-GitHub-lightgrey?style=flat-square)

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [v3.7.0 Update Summary](#v370-update-summary)
-   [Release Notes](#release-notes)
-   [Relationship to Previous
    Projects](#relationship-to-previous-projects)
-   [Architecture Topology](#architecture-topology)
-   [Data Sources](#data-sources)
-   [Scoring Compatibility Model](#scoring-compatibility-model)
-   [Authoritative SQLite State](#authoritative-sqlite-state)
-   [Parity-Safe Rebuild Workflow](#parity-safe-rebuild-workflow)
-   [Rank Data Workflow](#rank-data-workflow)
-   [Low-Storage Worker Model](#low-storage-worker-model)
-   [SQLite Health Escalation Guard](#sqlite-health-escalation-guard)
-   [Adaptive Chunk Checkpoint
    Worker](#adaptive-chunk-checkpoint-worker)
-   [Phase-Aware Incremental
    Micro-Sync](#phase-aware-incremental-micro-sync)
-   [Global Rank Builder](#global-rank-builder)
-   [Compact Public Rank Schema V3](#compact-public-rank-schema-v3)
-   [Ranking Model](#ranking-model)
-   [Dynamic Intelligence Badge](#dynamic-intelligence-badge)
-   [Official Rank Signal](#official-rank-signal)
-   [Dedicated Rank Publisher](#dedicated-rank-publisher)
-   [Public Output Files](#public-output-files)
-   [UI Architecture](#ui-architecture)
-   [Rank Data Status Model](#rank-data-status-model)
-   [Google Drive Backup Layer](#google-drive-backup-layer)
-   [Local Development Workspace](#local-development-workspace)
-   [Security and Trust Model](#security-and-trust-model)
-   [Validation Status](#validation-status)
-   [Changelog](#changelog)
-   [License](#license)
-   [Author](#author)

------------------------------------------------------------------------

## Overview

Wallet Intelligence Layer v3.7.0 is a DAC Testnet wallet intelligence
and comparative ranking system using a static browser interface, locally
indexed rank state, compact public rank artifacts, and a
no-wallet-connect check flow.

The v3.7.0 release is primarily an **indexing correctness and
operational safety release**.

It does not introduce a new scoring formula. Instead, it rebuilds the
WIL rank-state database with stricter proof of coverage:

``` text
Deterministic rebuild anchor
+
Block coverage table
+
Transaction ledger table
+
SQLite checkpoint resume
+
phase-aware worker workflow
```

The v3.6.0 normal wallet-quality scoring model remains the active
scoring policy:

``` text
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

The v3.5.0 Conviction/cutoff model is preserved as historical work, but
it is no longer treated as the active scoring or public rank signal.

The core v3 principle remains:

``` text
Every verified wallet variable can become a comparative public rank signal.
```

The browser does not calculate a global wallet rank from isolated wallet
data. Global rank is precomputed from the indexed wallet population,
published as compact rank artifacts, and retrieved by the UI through an
address-prefix shard.

``` text
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

During the v3.7.0 rebuild, public output may temporarily expose
lightweight status artifacts rather than complete rank shards. The UI
must treat this as a synchronization state, not as a completed global
rank dataset.

The shard is only a delivery format. The comparison population remains
global.

------------------------------------------------------------------------

------------------------------------------------------------------------

# Project Status

> **Status:** Finished & Discontinued

Wallet Intelligence Layer v3.7.0 represents the final state of this
community project.

The primary objective of this project was to demonstrate that a fully
local, deterministic wallet intelligence and comparative ranking system
for the DAC Testnet could be designed and implemented using public
blockchain data, local RPC nodes, SQLite, and static web technologies.

That objective has been successfully achieved.

During development, the complete indexing pipeline, synchronization
workflow, ranking engine, public artifact generation, and browser-based
lookup system were successfully implemented and validated. The project
demonstrates that this architecture is technically feasible and can
operate as a complete end-to-end solution.

## Why Development Has Been Discontinued

Although the architecture proved successful, the project relies on
continuous blockchain indexing performed entirely from a local device.

Maintaining a continuously synchronized local blockchain node, SQLite
database, historical indexing worker, backup pipeline, and public rank
generation requires substantial long-term consumption of CPU resources,
memory, disk storage, network bandwidth, and continuous device uptime.

For a community-developed project running solely on personal hardware,
this operational cost became impractical for long-term maintenance.

As a result, active development and continuous synchronization have been
discontinued.

This decision was made because of operational resource limitations,
**not because of any architectural limitation or technical failure**.

## Proof of Concept Successfully Demonstrated

This project successfully demonstrates that the following architecture
is technically feasible:

-   Local blockchain indexing
-   Deterministic synchronization
-   SQLite-based authoritative state
-   Global comparative wallet ranking
-   Static browser-based wallet lookup
-   Compact public rank artifacts
-   No wallet connection required
-   Community-driven infrastructure

The implementation confirms that this concept can be realized in
practice.

## Project Legacy

Although no longer actively maintained, this repository remains
available as a reference implementation documenting the architecture,
synchronization strategy, ranking methodology, and engineering decisions
developed throughout the Wallet Intelligence Layer project.

Future developers and community members are welcome to study, adapt, or
build upon the ideas presented here using infrastructure that is more
suitable for long-term operation.

------------------------------------------------------------------------

## v3.7.0 Update Summary

Version `v3.7.0` is the **Parity-Safe Rebuild** release.

Following the audit of the v3.6.0 incremental state, the project
confirmed that portions of the indexed wallet and transaction population
could diverge from the authoritative RPC data. Rather than patching the
existing state, v3.7.0 rebuilds the entire authoritative SQLite state
from a deterministic anchor and introduces explicit block-coverage and
transaction-ledger verification so this class of mismatch cannot
silently pass as a completed synchronization.

Core v3.7.0 rebuild parameters:

``` text
REBUILD_ANCHOR_BLOCK = 15,000,000
anchor_source = V3_7_0_DETERMINISTIC_REBUILD_ANCHOR
initial direction = latest_to_genesis
initial phase = HISTORICAL_BACKFILL_IN_PROGRESS
state status = REBUILDING
```

Current high-level workflow:

``` text
Backfill from block 15,000,000 down to genesis
↓
Catch up from block 15,000,001 toward the chain tip
↓
Incremental sync after catch-up reaches latest
```

Key updates:

-   Reset and rebuilt the active SQLite state for v3.7.0.
-   Added deterministic historical backfill anchor at block
    `15,000,000`.
-   Added explicit block coverage tracking through
    `indexed_block_coverage`.
-   Added explicit processed transaction tracking through
    `indexed_transaction_ledger`.
-   Added guard semantics requiring `tx_count == processed_tx_count` for
    a block to be complete.
-   Derived total processed transactions from coverage/ledger data
    instead of trusting a loose counter alone.
-   Kept `state_meta.status = REBUILDING` until full parity is proven.
-   Prevented premature public `SYNCED` / `INCREMENTAL` claims during
    rebuild.
-   Reset public artifacts to v3.7.0 rebuild/pending status before the
    first rebuild cycle.
-   Published lightweight public progress artifacts during rebuild.
-   Normalized worker, generator, backup, rank builder, and publisher
    labels to v3.7.0 where they describe release/workflow status.
-   Updated the public UI browser title, topbar, and hero heading to
    `Wallet Intelligence Layer v3.7.0`.
-   Preserved v3.6.0 scoring/model labels where they identify unchanged
    scoring policy.
-   Reconnected and verified Google Drive `rclone` remotes after OAuth
    token expiration/revocation.
-   Verified GDrive backup upload to `gdrive_wil_a:WIL-v3-rank-state`.
-   Preserved low-storage adaptive worker behavior using temporary
    clones, adaptive runtime directories, cleanup, and sleep cycles.

Important scoring compatibility note:

``` text
Project/UI release label       → v3.7.0
Rebuild/indexing workflow      → v3.7.0
Public progress/status labels  → v3.7.0
Scoring policy marker          → WIL-v3.6.0
Scoring model marker           → wallet-quality-scoring-v3.6.0-normal
Dynamic Intelligence Badge     → DIB-v3.6.0
Explorer-only Sybil Heuristics → EOH-v3.6.0
```

v3.7.0 is therefore not a scoring reset. It is a parity-safe state
rebuild and operational correctness release.

------------------------------------------------------------------------

## Release Notes

Versions `v3.0.0` through `v3.2.0` were experimental/beta releases. They
document the architecture evolution that led to the mature v3
implementation.

``` text
v3.0.0 — GitHub Actions prototype
v3.1.0 — Local node processing
v3.2.0 — Externalized state and Google Drive backup
v3.3.0 — Stable SQLite-backed production architecture
v3.4.0 — Worker Acceleration & Operational Hardening
v3.5.0 — Conviction-aware web, worker, and Compact V3 public rank schema
v3.6.0 — Back to Normal scoring after official Conviction flow inconsistency, with adaptive checkpoint worker hardening and phase-aware incremental micro-sync
v3.7.0 — Parity-safe rebuild from deterministic anchor with block coverage and transaction ledger guards
```

Version `v3.7.0` keeps the v3.6.0 normal scoring model but rebuilds the
authoritative rank-state path so full sync cannot be accepted without
explicit block and transaction coverage.

### Why v3.7.0 Was Necessary

Although the v3.6.0 architecture successfully reached the `INCREMENTAL`
synchronization phase, later validation revealed that the locally
indexed worker state was not fully aligned with the blockchain data
returned by the RPC.

The initial suspicion was that this discrepancy originated from repeated
architectural restructuring during the early evolution of the v3
project. As the architecture matured from multiple experimental
iterations into the stable production workflow, several indexing
assumptions and synchronization paths had also evolved. A comprehensive
audit later confirmed that this suspicion was correct: despite reaching
incremental operation, portions of the indexed state could diverge from
authoritative RPC data under certain historical conditions.

Rather than attempting to repair the existing state incrementally, the
project adopted a more conservative approach.

Version **v3.7.0 --- Parity-Safe Rebuild** was introduced to rebuild the
authoritative SQLite state from a deterministic and easily auditable
foundation. The rebuild introduces stronger safety guards, explicit
block coverage verification, transaction-level accounting, and a
deterministic rebuild anchor placed at the round block height
**15,000,000**. Using a round-number anchor simplifies future auditing,
making it significantly easier to verify coverage boundaries or repeat a
complete state audit if similar situations---or any future integrity
investigation---become necessary.

As part of this redesign, the worker performs a complete blockchain
re-index from the rebuild anchor, ensuring that every indexed block and
processed transaction can be independently verified before the project
is considered fully synchronized again.

"Production-ready" refers to the architecture and safety model. Rank
completeness still follows the current synchronization phase. During
historical backfill or catch-up, the UI must not imply that the full
chain population is already finalized.

------------------------------------------------------------------------

## Relationship to Previous Projects

Wallet Intelligence Layer v3.7.0 is part of a broader DAC tooling
progression.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Project                        Version Role in the           Reference
                                         Progression           
  ---------------- --------------------- --------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------
  DAC Sender                    `v1.4.3` Activity-generation   [DAC Sender](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/Sender-Web)
                                         and testnet           
                                         interaction tool.     

  Wallet                        `v1.5.4` First wallet          [Wallet Intelligence Layer
  Intelligence                           intelligence layer    v1](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1)
  Layer                                  focused on reading    
                                         public DAC wallet     
                                         activity.             

  Wallet                        `v2.0.2` Dynamic wallet-bound  [Wallet Intelligence Layer
  Intelligence                           status badge          v2](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2)
  Layer                                  workflow.             

  Wallet                        `v3.7.0` Global comparative    [Wallet Intelligence Layer
  Intelligence                           wallet intelligence   v3](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v3)
  Layer                                  using local DAC       
                                         nodes, SQLite state,  
                                         Compact V3 rank       
                                         artifacts, normal     
                                         v3.6.0 scoring        
                                         policy, and           
                                         parity-safe           
                                         rebuild/indexing      
                                         guards.               
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

``` text
DAC Sender
→ creates / supports wallet activity

Wallet Intelligence Layer v1
→ reads wallet activity

Wallet Intelligence Layer v2
→ represents wallet status through a dynamic badge layer

Wallet Intelligence Layer v3
→ compares wallet variables across the indexed population
```

------------------------------------------------------------------------

## Architecture Topology

Wallet Intelligence Layer v3.7.0 uses the hybrid local-processing and
public-delivery architecture established in v3.3.0, the normal scoring
policy restored in v3.6.0, and the parity-safe indexing guards added in
v3.7.0.

``` text
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
                           │ Phase-Aware Local Runner     │
                           │ Backfill / Catch-up / Micro  │
                           │ low-storage temp clone model │
                           └──────────────┬───────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ Local RPC Rank Worker        │
                           │ v3.7.0 parity-safe rebuild   │
                           │ v3.6.0 scoring compatibility │
                           └──────────────┬───────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ Adaptive Chunk Guard         │
                           │ 5,000-block safety unit      │
                           │ 50,000-block cycle ceiling   │
                           └──────────────┬───────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ SQLite Health Guard          │
                           │ lightweight / full / diagnose│
                           └──────────────┬───────────────┘
                                          ▼
                           ┌──────────────────────────────┐
                           │ Authoritative SQLite State   │
                           │ wallet / stake / NFT / sync  │
                           │ coverage / transaction ledger│
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

------------------------------------------------------------------------

## Data Sources

The project uses public and node-derived DAC Testnet data.

### Official DAC RPC

``` text
https://rpctest.dachain.tech/
```

### Official DAC Explorer

``` text
https://exptest.dachain.tech
```

### Official DAC Explorer API

``` text
https://exptest.dachain.tech/api
```

### Local DAC RPC Nodes

``` text
Primary:
http://127.0.0.1:8546

Fallback:
http://192.168.100.7:8545
```

Expected chain ID:

``` text
0x5586
```

### Current DACC Stake Flow

v3.7.0 keeps the v3.6.0 normal stake/unstake flow for current DACC stake
estimation.

``` text
staking_metric = ESTIMATED_CURRENT_STAKE
staking_source = DAC_STAKE_UNSTAKE_TRANSACTION_FLOW
```

Browser classifier:

``` text
STAKE_FLOW_CLASSIFIER
Estimated Current Stake = totalStakeIn - totalUnstakeOut
```

### Legacy Conviction Data

Legacy Conviction tables may remain in SQLite for backward compatibility
with v3.5.0 state.

In v3.7.0, Conviction remains inactive as a public scoring or rank
signal.

``` text
CONVICTION_METRICS_ACTIVE = False
```

------------------------------------------------------------------------

## Scoring Compatibility Model

v3.7.0 separates the **release / indexing workflow version** from the
**scoring policy version**.

The project and rebuild workflow are v3.7.0:

``` text
Wallet Intelligence Layer v3.7.0
Parity-Safe Rebuild
V3_7_0_DETERMINISTIC_REBUILD_ANCHOR
```

The active wallet-quality scoring policy remains v3.6.0:

``` text
WIL-v3.6.0
wallet-quality-scoring-v3.6.0-normal
DIB-v3.6.0
EOH-v3.6.0
```

This is intentional.

v3.7.0 does not change the formula for reputation scoring, badge
tiering, or Explorer-only Sybil Heuristics. It changes the safety of the
state that feeds global rank and public status.

------------------------------------------------------------------------

## Authoritative SQLite State

The active heavy state is stored outside GitHub:

``` text
~/wil-v3-rank-state/wil-v3-rank-state.sqlite
```

SQLite is the source of truth for the v3.7.0 rank worker.

Principal logical tables include:

``` text
wallet_metrics
staking_metrics
official_inception_nft_tokens
checkpoint
counters
state_meta
enrichment_queue
official_inception_nft_repair_state
indexed_block_coverage
indexed_transaction_ledger
```

Legacy compatibility tables may also exist:

``` text
conviction_lock_events
conviction_metrics
```

These legacy tables are retained to avoid breaking historical state, but
Conviction is not active in v3.7.0 scoring.

### v3.7.0 Coverage Tables

`indexed_block_coverage` records whether a block was fully processed.

A block is complete only when:

``` text
tx_count == processed_tx_count
status = COMPLETE
```

`indexed_transaction_ledger` records processed transactions for the
coverage range.

A healthy parity checkpoint should satisfy:

``` text
SUM(indexed_block_coverage.tx_count)
=
SUM(indexed_block_coverage.processed_tx_count)
=
COUNT(indexed_transaction_ledger)
```

This is the core v3.7.0 guard against silent missing block or
transaction data.

------------------------------------------------------------------------

## Parity-Safe Rebuild Workflow

v3.7.0 starts from a deterministic historical anchor:

``` text
historical_backfill_anchor_block = 15000000
historical_backfill_anchor_source = V3_7_0_DETERMINISTIC_REBUILD_ANCHOR
```

The rebuild sequence is:

``` text
1. HISTORICAL_BACKFILL_IN_PROGRESS
   Process block 15,000,000 downward toward genesis.

2. POST_BACKFILL_CATCH_UP
   After genesis is reached, process forward from block 15,000,001 toward the chain tip.

3. INCREMENTAL
   After catch-up reaches latest, process newly produced blocks in small live cycles.
```

During rebuild:

``` text
state_meta.status = REBUILDING
rank_lookup_enabled = false until valid rank artifacts exist
rank_shards_published = false until full rank publisher is safely run
```

The system should not claim full rank completeness until:

``` text
historical backfill is complete
+
post-backfill catch-up is complete
+
coverage has no missing blocks
+
all complete blocks satisfy tx_count == processed_tx_count
+
ledger row count equals processed transaction sum
+
state is no longer REBUILDING
```

This is the central difference between v3.7.0 and the older state that
could appear synced while still having wallet/transaction gaps.

------------------------------------------------------------------------

## Rank Data Workflow

The main worker uses three synchronization phases.

  -----------------------------------------------------------------------------------
  Phase                               Meaning                 v3.7.0 runner behavior
  ----------------------------------- ----------------------- -----------------------
  `HISTORICAL_BACKFILL_IN_PROGRESS`   Processes historical    Large adaptive ceiling,
                                      blocks backward from    5,000-block safety
                                      block 15,000,000 toward chunks, 180s sleep.
                                      genesis.                

  `POST_BACKFILL_CATCH_UP`            Fills the forward gap   Large adaptive ceiling,
                                      created while backfill  5,000-block safety
                                      was running.            chunks, 180s sleep.

  `INCREMENTAL`                       Processes newly         Small lag-aware
                                      produced blocks after   micro-sync cycles,
                                      catch-up reaches the    normally 10 blocks, 60s
                                      chain tip.              sleep.
  -----------------------------------------------------------------------------------

During long historical backfill or post-backfill catch-up, the worker
may run in adaptive checkpoint mode. In that mode, each 5,000-block
chunk is treated as an evaluation point. The cycle may continue toward a
larger ceiling when the chunk is light, or stop early when the chunk is
dense or the device shows pressure.

Worker responsibilities in v3.7.0:

-   block transactions;
-   block-level coverage accounting;
-   per-transaction ledger accounting;
-   senders and recipients;
-   native-value flow;
-   gas usage;
-   wallet activity counters;
-   NFT activity;
-   collection diversity;
-   stake and unstake flow;
-   Official Inception NFT `Transfer` logs;
-   checkpoint and phase transitions;
-   incremental position and lag metadata.

Lightweight status may include sync phase, last synced block, next
backfill block, catch-up next block, incremental next block, latest
chain block at sync, indexed wallet count, total processed transactions,
state backend, feature support flags, and public rank readiness.

Global rank generation is handled separately and should not be run as a
complete public snapshot until rebuild parity is proven.

------------------------------------------------------------------------

## Low-Storage Worker Model

The project follows an explicit low-storage lifecycle:

``` text
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

Temporary work may include a temporary repository clone, a consistent
source database snapshot, a temporary rank-build database, a temporary
snapshot repository, compressed backup work, adaptive runtime checkpoint
files, and temporary manifests.

The active dashboard/runner workflow uses a temporary clone for each
cycle. The runner publishes lightweight public status artifacts, cleans
temporary runtime directories, cleans the temporary repository clone,
then sleeps before the next cycle.

Observed v3.7.0 operating pattern:

``` text
MAX_BLOCKS=50000
BALANCE_ENRICH_LIMIT=1000
SLEEP_SECONDS=180
ADAPTIVE_CHUNK_SIZE=5000
```

This design keeps daily source work lightweight and prevents generated
operational data from being accidentally committed.

------------------------------------------------------------------------

## SQLite Health Escalation Guard

v3.7.0 keeps the SQLite health guard to protect the authoritative
rank-state database from silent corruption or unsafe writes.

The guard supports three modes:

``` text
lightweight
full
diagnose
```

### Normal startup path

The default worker startup uses a lightweight preflight check.

``` text
sqlite_health_guard.py --mode lightweight
```

This is intended to be fast enough for every worker cycle.

### Full integrity check path

A full SQLite integrity check may be enabled explicitly when deeper
validation is needed.

``` text
WIL_V3_FULL_SQLITE_QUICK_CHECK=1
sqlite_health_guard.py --mode full
```

### Automatic escalation path

If a lightweight check fails, the runner escalates to diagnostic mode:

``` text
sqlite_health_guard.py --mode diagnose --force-full
```

The worker should not continue as if the state is healthy when the
SQLite preflight fails.

### Safe reaction policy

A health failure is treated as a state-safety event, not a normal worker
stop.

Safe reaction:

``` text
stop worker
run diagnose
preserve external SQLite state
avoid publishing suspect output
restore or repair before continuing
```

------------------------------------------------------------------------

## Adaptive Chunk Checkpoint Worker

v3.7.0 keeps the adaptive chunk checkpoint worker mode for the local RPC
rank worker.

The purpose is to make historical backfill and post-backfill catch-up
faster without removing the original safety behavior of the
`5,000/1000/180` worker preset.

### Operating preset

Validated high-efficiency preset for backfill/catch-up:

``` text
MAX_BLOCKS=50000
BALANCE_ENRICH_LIMIT=1000
SLEEP_SECONDS=180
ADAPTIVE_CHUNK_MODE=1
ADAPTIVE_CHUNK_SIZE=5000
```

This means:

``` text
Cycle ceiling: 50,000 blocks
Safety unit: 5,000 blocks
Maximum chunks per full cycle: 10
Sleep after cycle: 180 seconds
```

The cycle ceiling is not a forced workload. It is only the maximum the
worker may attempt when the observed chain range and device signals
remain safe.

### Why this improves throughput

Previous safe baseline:

``` text
5,000 blocks
↓
publish
↓
sleep 180s
↓
5,000 blocks
↓
publish
↓
sleep 180s
```

Adaptive high-efficiency mode:

``` text
5,000 blocks
↓
check safety
↓
5,000 blocks
↓
check safety
↓
continue up to 50,000 only while safe
↓
publish once
↓
sleep 180s
```

Dense ranges may stop after one chunk, behaving like the original
`5,000/1000/180` baseline.

Light ranges may complete multiple chunks, reducing calendar time to
reach incremental sync.

### Safety model

Each chunk is evaluated before the next chunk starts.

The adaptive guard evaluates chain-density and device-resource signals,
including:

``` text
processed blocks
processed transactions
wallet rows written
staking rows written
chunk elapsed time
SQLite WAL growth
free disk space
available memory
swap usage
worker RSS memory
system load
CPU idle percentage
IO wait percentage
```

A stop-early cycle is not treated as a worker failure. It means the
adaptive safety layer worked as intended.

------------------------------------------------------------------------

## Phase-Aware Incremental Micro-Sync

v3.7.0 keeps the phase-aware runtime preset layer to the low-storage
runner.

The runner reads the current sync phase from SQLite before each cycle
and applies a preset appropriate to the phase.

### Phase presets

  -------------------------------------------------------------------------------------------------------
  Phase                                    MAX_BLOCKS   ADAPTIVE_CHUNK_SIZE   SLEEP_SECONDS Purpose
  ----------------------------------- --------------- --------------------- --------------- -------------
  `HISTORICAL_BACKFILL_IN_PROGRESS`           `50000`                `5000`           `180` Fast
                                                                                            historical
                                                                                            progress
                                                                                            while
                                                                                            preserving
                                                                                            5,000-block
                                                                                            safety.

  `POST_BACKFILL_CATCH_UP`                    `50000`                `5000`           `180` Fill the
                                                                                            forward gap
                                                                                            without
                                                                                            reducing
                                                                                            device rest
                                                                                            time.

  `INCREMENTAL` normal                           `10`                  `10`            `60` Keep public
                                                                                            data close to
                                                                                            the chain
                                                                                            tip.

  `INCREMENTAL` lag \<= 100                      `25`                  `25`            `60` Recover from
                                                                                            a small
                                                                                            temporary
                                                                                            gap.

  `INCREMENTAL` lag \<= 500                     `100`                 `100`            `60` Recover from
                                                                                            a medium
                                                                                            temporary
                                                                                            gap.

  `INCREMENTAL` lag \> 500                      `500`                 `100`            `60` Recover from
                                                                                            a larger
                                                                                            outage or
                                                                                            delayed
                                                                                            runner
                                                                                            restart.
  -------------------------------------------------------------------------------------------------------

### Why incremental does not use the 50,000-block preset

The `50,000/5000/180` behavior is useful for historical and catch-up
phases, but it is too coarse for live incremental mode.

In incremental mode, the worker should not wait for a large batch before
publishing. Instead, it should process the new blocks that appeared
during the previous push/sleep interval and publish again when the
public manifest changes.

Normal incremental behavior:

``` text
check latest block
↓
process up to 10 blocks
↓
publish changed public artifacts
↓
sleep 60s
↓
repeat
```

This does not make WIL real-time, but it makes the freshness gap
explicit and small.

------------------------------------------------------------------------

## Global Rank Builder

The global rank builder is:

``` text
scripts/generate_rank_from_sqlite.py
```

It reads a consistent snapshot of the complete SQLite population.

The builder:

1.  creates a consistent source snapshot;
2.  streams wallet metrics into a temporary rank-build database;
3.  joins stake metrics as DACC Stake;
4.  counts current Official NFT ownership;
5.  computes global metric ranks;
6.  computes the Final Composite Rank;
7.  creates compact records;
8.  splits records into prefix shards;
9.  writes summary and index metadata;
10. validates the rank-build database;
11. removes temporary builder work.

Rank calculation occurs before sharding. A wallet stored in `ab.json` is
still ranked against the complete indexed population, not only against
addresses beginning with `0xab`.

In v3.7.0, the full global rank builder should be run only after
parity-safe rebuild conditions are satisfied.

------------------------------------------------------------------------

## Compact Public Rank Schema V3

v3.7.0 keeps Compact V3 delivery:

``` text
WIL_V3_COMPACT_ARRAY_V3
SHARDED_COMPACT_V3
```

The v3.6.0 scoring model remains active and Conviction Locked is not
promoted as an active comparative signal.

The stake compatibility key may remain:

``` text
estimated_stake_before_conviction
```

but in the active UI it is displayed as:

``` text
DACC Stake
```

Active comparative signals include:

``` text
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

``` text
WIL_V3_COMPACT_ARRAY_V2
WIL_V3_COMPACT_ARRAY_V3
```

Older snapshots remain readable, while v3.7.0 displays active labels
according to the normal v3.6.0 scoring model.

------------------------------------------------------------------------

## Ranking Model

WIL v3.7.0 separates two related but different concepts:

``` text
Global comparative public rank
→ precomputed from the full indexed wallet population

Live wallet reputation score
→ computed in the browser from the checked wallet's verified data
```

### Comparative rank cards

v3.7.0 exposes normal comparative wallet signals, including:

``` text
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

``` text
Estimated Stake Before Conviction
Conviction Locked
```

### Final Composite Rank

The Final Composite Rank remains the preserved eight-variable global
rank formula from the stable v3 architecture.

Final Composite Rank inputs:

1.  Native Funds
2.  Transactions
3.  Gas Used
4.  Native Volume
5.  NFT Holdings
6.  Collection Diversity
7.  Reputation Score
8.  Low-Risk Profile

DACC Stake and Official Testnet Inception NFTs are displayed separately
and are not merged into the preserved Final Composite Rank formula.

### Live Reputation Scoring Layer

  ------------------------------------------------------------------------
  Component                               Max Points Active interpretation
  --------------------- ---------------------------- ---------------------
  Transaction Score                               20 Wallet activity
                                                     volume

  NFT Diversity Score                             10 Number of distinct
                                                     NFT collections

  NFT Holdings Score                              10 Total NFT holdings

  Native Funds Score                              15 Current native DACC
                                                     balance

  DACC Stake Score                                20 Current DACC Stake
                                                     from normal
                                                     stake/unstake flow

  DAC Inception Rank                              25 DAC Inception Rank
  Score                                              NFT signal

  **Total**                                  **100** Community-defined
                                                     wallet-quality score
  ------------------------------------------------------------------------

Native Funds scoring mode:

``` text
CURRENT_NATIVE_FUNDS
```

DACC Stake scoring mode:

``` text
CURRENT_DACC_STAKE
```

------------------------------------------------------------------------

## Dynamic Intelligence Badge

The Dynamic Intelligence Badge follows monotonic progression behavior.

A badge update is offered only when the newly calculated tier is higher
than the highest known tier already achieved.

This means:

-   a wallet can move upward;
-   a wallet is not downgraded;
-   an update is not offered for the same or lower tier;
-   the highest known badge tier is preserved locally.

Active badge engine label remains:

``` text
DIB-v3.6.0
```

Local preserved badge keys:

``` text
wil:v3.6.0:highestBadgeClass:<wallet>
wil:v3.5.0:highestBadgeClass:<wallet>
```

These remain v3.6.0/v3.5.0 intentionally so existing badge progression
state is not broken by the v3.7.0 indexing rebuild.

------------------------------------------------------------------------

## Official Rank Signal

Official Testnet Inception NFT contract:

``` text
0xB36ab4c2Bd6aCfC36e9D6c53F39F4301901Bd647
```

The worker tracks ERC-721 `Transfer` logs and stores the latest owner
for each token.

The Official Rank Signal is derived from the wallet's current token
count.

     NFT Count Official Rank
  ------------ ---------------
             0 NONE
             1 CADET
             2 COMMANDO
             3 SEAL
             4 SHADOW UNIT
             5 VANGUARD
             6 SENTINEL
             7 SOVEREIGN
             8 WARRIOR
             9 ARCHITECT
            10 INTERCEPTOR
            11 PHANTOM
            12 CIPHER
    13 or more CROWN

This is an independent official ecosystem signal. It is not merged into
the Final Composite Rank formula.

------------------------------------------------------------------------

## Dedicated Rank Publisher

The publisher is:

``` text
scripts/publish_rank_snapshot_branch.sh
```

It validates configuration, creates isolated temporary work, runs the
global rank builder, validates Compact V3 metadata, validates shard
completeness, creates a clean snapshot repository, creates one snapshot
commit, optionally pushes the public snapshot branch, and removes
temporary work.

Public rank branch:

``` text
wil-v3-rank-data
```

Safety rules prevent incomplete snapshots, limited test snapshots, or
temporary fixture data from becoming production output.

v3.7.0 operational rule:

``` text
Do not run the dedicated full rank publisher as final production output until the parity-safe rebuild has completed historical backfill, catch-up, and coverage validation.
```

During rebuild, lightweight public status artifacts may be published to
show progress without pretending the global rank dataset is complete.

------------------------------------------------------------------------

## Public Output Files

Public rank/status artifacts:

``` text
wallet-intelligence-layer-v3/
├── data/
│   ├── wallet-rank-summary.json
│   ├── wallet-rank-index.json
│   └── rank-shards/
│       ├── 00.json
│       ├── 01.json
│       ├── ...
│       └── ff.json
└── rank-data-engine/
    └── data/
        └── latest.json
```

During rebuild, the public summary/index/latest files may represent
rebuild progress rather than final rank shards.

The authoritative SQLite database is not published to GitHub.

------------------------------------------------------------------------

## UI Architecture

The public UI release label is:

``` text
Wallet Intelligence Layer v3.7.0
```

This appears in the browser title, topbar brand, and hero heading.

The scoring/model labels remain:

``` text
WIL-v3.6.0
wallet-quality-scoring-v3.6.0-normal
DIB-v3.6.0
EOH-v3.6.0
```

This split is intentional:

``` text
v3.7.0 = public release / parity-safe rebuild / indexing workflow
v3.6.0 = active scoring, badge, and behavior heuristic model
```

Browser lookup flow:

1.  normalize the address;
2.  load the public rank summary;
3.  load the rank index;
4.  derive the address prefix;
5.  fetch the matching rank shard when rank shards are valid;
6.  decode metric values and ranks;
7.  render the Wallet Rank Intelligence section.

The v3.7.0 web UI should not show old Conviction-era active labels:

``` text
Conviction Locked
Conviction Timeliness
Native Funds Before Conviction
Estimated Stake Before Conviction
before Conviction
Conviction cutover
cutoff-aware
postCutover
```

The Rank Data Engine Status UI exposes synchronization position rows:

``` text
Historical Backfill
- Anchor
- Current Position

Post Backfill Catch Up
- Anchor
- Current Position

Incremental Sync
- Status
- Current Position
- Chain Latest
- Incremental Lag
```

### Pending Rank State Rendering

Wallet Rank Intelligence is intentionally defensive when rank data is
not publish-ready yet.

The UI should not render user-facing `NaN` for rank cards, official rank
cards, percentile rows, or rank population denominators.

Pending rank states are rendered as explicit text:

``` text
Rank pending
Percentile pending
population pending
Pending
```

Typical rebuild display:

``` text
Network snapshot live · Rank pending until incremental sync
Rank pending / <population>
Percentile pending
```

When rank shards are available and the wallet is indexed, the same UI
returns to numeric rank display:

``` text
#1,279 / 4,300,000
Percentile: 99.97%
```

### RAW OUTPUT Wallet Rank Intelligence Context

Wallet Rank Intelligence is loaded asynchronously after the main wallet
profile render.

The UI mirrors that asynchronous rank lookup into the `RAW OUTPUT`
object through:

``` text
walletRankIntelligence
```

This makes the visual Wallet Rank Intelligence panel and the copied JSON
output consistent.

------------------------------------------------------------------------

## Rank Data Status Model

  -----------------------------------------------------------------------
  State                               Meaning
  ----------------------------------- -----------------------------------
  `HISTORICAL_BACKFILL_IN_PROGRESS`   The worker is processing historical
                                      blocks backward from the v3.7.0
                                      deterministic anchor toward
                                      genesis.

  `POST_BACKFILL_CATCH_UP`            Historical backfill reached genesis
                                      and the worker is filling the
                                      forward gap.

  `INCREMENTAL`                       The worker has caught up and is
                                      processing newly produced blocks.
  -----------------------------------------------------------------------

Important status fields:

  ------------------------------------------------------------------------------
  Field                                 Meaning
  ------------------------------------- ----------------------------------------
  `historical_backfill_anchor_block`    The deterministic v3.7.0 backfill anchor
                                        block.

  `historical_backfill_anchor_source`   Expected to be
                                        `V3_7_0_DETERMINISTIC_REBUILD_ANCHOR`.

  `local_rpc_backfill_next_block`       The next historical block to process
                                        while backfill is active.

  `post_backfill_catch_up_from_block`   The first block of the forward catch-up
                                        range.

  `catch_up_next_block`                 The next catch-up block to process.

  `incremental_next_block`              The next incremental block to process
                                        after catch-up.

  `local_rpc_latest_block_at_sync`      The latest chain block observed by the
                                        worker at sync time.

  `incremental_lag_blocks`              UI-computed freshness gap between latest
                                        block and incremental position.
  ------------------------------------------------------------------------------

The UI should only imply a fully synchronized rank dataset after
historical backfill and catch-up are complete.

When rank data is not ready, the UI renders explicit pending labels
instead of user-facing `NaN` values. When rank data is available but
incremental sync has lag, the UI keeps the last valid rank context
visible and uses Current Position, Chain Latest, and Incremental Lag to
explain freshness.

------------------------------------------------------------------------

## Google Drive Backup Layer

The heavy SQLite state is backed up locally through `rclone`.

Configured remotes:

``` text
gdrive_wil_a:
gdrive_wil_b:
```

Backup root:

``` text
gdrive_wil_a:WIL-v3-rank-state
gdrive_wil_b:WIL-v3-rank-state
```

Phase folders:

``` text
Backfill to Genesis
Post Backfill Catch Up
Incremental
latest
```

Backup cadence:

``` text
0 */6 * * *
```

The backup script creates a consistent SQLite snapshot, compresses it
with `zstd`, writes a SHA-256 checksum, uploads a timestamped backup to
the current phase folder, and updates the `latest` pointer.

v3.7.0 backup validation confirmed:

``` text
snapshot_integrity_check = ok
upload_enabled = true
selected_remote = gdrive_wil_a
version = v3.7.0
```

GitHub does not upload the heavy state to Google Drive. The local
environment performs backups. GitHub stores source and public rank
artifacts; Google Drive stores external heavy-state recovery snapshots.

------------------------------------------------------------------------

## Local Development Workspace

Canonical repository:

``` text
https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup
```

Daily working clone:

``` text
~/dac-contribution/DEV-SPACE
```

WIL project source:

``` text
DAC-Contributions/
└── dac-wallet-intelligence-layer/
    └── wallet-intelligence-layer-v3/
```

Heavy operational state is outside the repository:

``` text
~/wil-v3-rank-state/
```

Worker and benchmark logs are outside the repository:

``` text
~/wil-v3-worker-logs/
```

Explicit file staging is preferred over broad commands such as:

``` text
git add .
```

------------------------------------------------------------------------

## Security and Trust Model

Wallet Intelligence Layer v3.7.0 keeps the same safety principles as
earlier versions:

``` text
No private key handling
No forced wallet connection for checking
No backend account system
No custody
No hidden eligibility claim
No official reward claim
No fabricated score output
```

The wallet check flow uses public DAC Testnet information and public
rank artifacts.

The local worker reads blockchain data and updates local intelligence
state. It does not require private keys for wallet checking.

The system should be treated as a transparent community analytics layer,
not an official DAC scoring or eligibility system.

------------------------------------------------------------------------

## Validation Status

The v3.7.0 rebuild work was validated in stages.

### Fresh state reset validation

A fresh SQLite state was created with schema version `22` and zero stale
data rows before rebuild start.

Expected fresh state properties:

``` text
checkpoint_rows = 0
counters_rows = 0
state_meta_rows = 0
wallet_metrics_rows = 0
indexed_block_coverage_rows = 0
indexed_transaction_ledger_rows = 0
staking_metrics_rows = 0
official_inception_nft_tokens_rows = 0
```

### Deterministic anchor validation

Initial v3.7.0 dry-run/short-run validation confirmed anchor behavior at
block `15,000,000`.

Expected anchor fields:

``` text
historical_backfill_anchor_block = 15000000
historical_backfill_anchor_source = V3_7_0_DETERMINISTIC_REBUILD_ANCHOR
sync_phase = HISTORICAL_BACKFILL_IN_PROGRESS
```

### First real cycle validation

A first production rebuild cycle processed 5,000 blocks from block
`15,000,000` down to block `14,995,001`.

Representative healthy parity values:

``` text
coverage_rows = 5000
min_block = 14995001
max_block = 15000000
tx_sum = 579058
processed_sum = 579058
ledger_rows = 579058
wallet_rows = 247085
next_backfill_block = 14995000
state_meta_project = Wallet Intelligence Layer v3.7.0
state_meta_status = REBUILDING
```

This confirmed:

``` text
SUM(tx_count) == SUM(processed_tx_count)
COUNT(indexed_transaction_ledger) == SUM(processed_tx_count)
```

### Script label normalization validation

v3.7.0 script labels were normalized after detecting stale v3.3.0/v3.6.0
release labels in scripts that describe public status, backup, rank
builder, and publisher workflow.

Validated outcome:

``` text
syntax_ok = YES
final_stale_scan = NONE
```

Scoring/model markers are intentionally preserved separately in the
public UI.

### Public UI validation

The hosted UI `index.html` was updated only in the public release
display areas:

``` text
browser title
brand topbar
hero heading
```

Updated visible release label:

``` text
Wallet Intelligence Layer v3.7.0
```

Preserved model markers:

``` text
EOH-v3.6.0
DIB-v3.6.0
WIL-v3.6.0
```

### Google Drive backup validation

After reconnecting `rclone` OAuth tokens, a manual GDrive backup
succeeded.

Validated remote path:

``` text
gdrive_wil_a:WIL-v3-rank-state/Backfill to Genesis
gdrive_wil_a:WIL-v3-rank-state/latest
```

Validated files:

``` text
wil-v3-rank-state-2026-06-26T14-11-08Z.sqlite.zst
wil-v3-rank-state-2026-06-26T14-11-08Z.sqlite.zst.sha256
wil-v3-rank-state.latest.sqlite.zst
wil-v3-rank-state.latest.sqlite.zst.sha256
```

### Current operational status

At the time of this README update, v3.7.0 rebuild is expected to be
running through:

``` text
HISTORICAL_BACKFILL_IN_PROGRESS
↓
POST_BACKFILL_CATCH_UP
↓
INCREMENTAL
```

The full dedicated rank snapshot should remain disabled until rebuild
parity is complete.

------------------------------------------------------------------------

## Changelog

### v3.7.0 --- Parity-Safe Rebuild

-   Reset the authoritative local SQLite rank state for a clean rebuild.
-   Added deterministic rebuild anchor at block `15,000,000`.
-   Added `V3_7_0_DETERMINISTIC_REBUILD_ANCHOR` as the anchor source
    marker.
-   Added `indexed_block_coverage` as block-level parity evidence.
-   Added `indexed_transaction_ledger` as processed transaction
    evidence.
-   Required complete blocks to satisfy
    `tx_count == processed_tx_count`.
-   Derived processed transaction totals from coverage/ledger state.
-   Kept state status as `REBUILDING` during historical backfill and
    catch-up.
-   Prevented premature completed/incremental public status during
    rebuild.
-   Reset public JSON artifacts to v3.7.0 rebuild pending/progress
    state.
-   Confirmed first 5,000-block production cycle with matching coverage
    and ledger counts.
-   Preserved v3.6.0 normal wallet-quality scoring policy.
-   Preserved `WIL-v3.6.0`, `wallet-quality-scoring-v3.6.0-normal`,
    `DIB-v3.6.0`, and `EOH-v3.6.0` as scoring/model markers.
-   Updated public UI title/topbar/hero labels to
    `Wallet Intelligence Layer v3.7.0`.
-   Normalized worker/status/backup/rank-builder script labels to v3.7.0
    where they represent release or workflow status.
-   Reconnected Google Drive `rclone` remotes after OAuth token
    expiration/revocation.
-   Verified GDrive rollover backup to `gdrive_wil_a:WIL-v3-rank-state`.
-   Preserved low-storage temp-clone workflow and adaptive 5,000-block
    chunk guard.
-   Preserved phase-aware backfill → catch-up → incremental workflow.

### v3.6.0 --- Back to Normal Scoring and Phase-Aware Worker Hardening

-   Restored normal Native Funds Score using current live native DACC
    balance.
-   Restored normal DACC Stake Score using current stake/unstake flow.
-   Removed Conviction Locked from active web UI.
-   Removed Conviction Timeliness from active DIB metadata.
-   Removed Conviction/cutoff scoring from active reputation logic.
-   Normalized public rank UI stake label to `DACC Stake`.
-   Removed visible `Estimated Stake Before Conviction` and
    `Conviction Locked` labels from Wallet Rank Intelligence.
-   Updated WIL web label to `v3.6.0`.
-   Updated policy label to `WIL-v3.6.0`.
-   Updated scoring model to `wallet-quality-scoring-v3.6.0-normal`.
-   Updated Dynamic Intelligence Badge label to `DIB-v3.6.0`.
-   Updated Explorer-only Sybil Heuristics label to `EOH-v3.6.0`.
-   Preserved Dynamic Intelligence Badge monotonic update behavior.
-   Added v3.5.0 localStorage fallback for preserved badge tier.
-   Updated worker public status version to `v3.6.0`.
-   Updated rank publisher version to `v3.6.0`.
-   Updated public worker staking metadata to `ESTIMATED_CURRENT_STAKE`.
-   Updated public worker staking source to
    `DAC_STAKE_UNSTAKE_TRANSACTION_FLOW`.
-   Disabled active Conviction worker processing with
    `CONVICTION_METRICS_ACTIVE = False`.
-   Preserved legacy Conviction SQLite state only for backward
    compatibility.
-   Added SQLite health escalation guard.
-   Added adaptive chunk checkpoint worker mode.
-   Validated the `50,000/1000/180` adaptive ceiling while preserving
    5,000-block safety behavior.
-   Added phase-aware runner presets for historical backfill,
    post-backfill catch-up, and incremental sync.
-   Added incremental micro-sync behavior with normal `10` block cycles
    and `60s` sleep.
-   Added pending-rank UI guards so unavailable rank data is shown as
    `Pending` / `Rank pending` / `Percentile pending` instead of
    user-facing `NaN`.
-   Added RAW OUTPUT enrichment for Wallet Rank Intelligence.

### v3.5.0 --- Conviction-aware Web Schema

-   Added Compact V3 public rank records.
-   Added Conviction Locked as a comparative public rank metric.
-   Renamed the stake-era metric to Estimated Stake Before Conviction.
-   Added Conviction cutover metadata to public rank summary output.
-   Added Conviction SQLite event and aggregate state.
-   Preserved backward-compatible Compact V2 browser decoding.
-   Completed Conviction-aware live reputation scoring.
-   Added monotonic Dynamic Intelligence Badge behavior.

### v3.4.0 --- Worker Acceleration & Operational Hardening

-   Optimized Local RPC worker counterparty tracking.
-   Improved historical backfill throughput through sorted counterparty
    lookup.
-   Benchmarked production worker presets.
-   Added backup wrapper cleanup after successful Google Drive upload.
-   Added terminal phase monitoring.

### v3.3.0 --- Stable

-   Introduced the LiteSQLite architecture.
-   Introduced compact public rank sharding for browser lookup.
-   Finalized the global rank builder.
-   Finalized the dedicated public snapshot publisher.
-   Added Estimated Current Stake.
-   Added Official Testnet Inception NFT ownership tracking.
-   Added consistent compressed SQLite backup to Google Drive A/B.
-   First production-ready v3 release.

### v3.2.0 --- Beta

-   Introduced the Google Drive storage backend.
-   Externalized heavy rank state outside GitHub.
-   Added Google Drive A/B rollover behavior.

### v3.1.0 --- Beta

-   Switched processing to Local Node.
-   Added Linux primary and Windows fallback RPC sources.
-   Added historical backfill, post-backfill catch-up, and incremental
    phases.

### v3.0.0 --- Beta

-   Initial rewrite using GitHub Actions.
-   Introduced Wallet Rank Intelligence as the v3 direction.
-   Added the global comparative rank concept.

------------------------------------------------------------------------

## License

This project is part of the
[`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup)
repository and is covered by the root repository license.

------------------------------------------------------------------------

## Author

**JERUZZALEM**\
DAC Infra Tester

Built by Communities for Communities.
