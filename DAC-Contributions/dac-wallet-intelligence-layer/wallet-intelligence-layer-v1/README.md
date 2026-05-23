# DAC Wallet Intelligence Layer v1.2.0 — Community Wallet Checker

A client-side wallet intelligence interface for the DAC Quantum Chain Testnet.

This tool allows users to paste a wallet address and generate a read-only wallet profile from public DAC testnet data: native funds, NFT ownership, activity metrics, portfolio behavior, reputation scoring, and Sybil-risk estimation.

> **Important:** This is a community-built checker by **JERUZZALEM — DAC Infra Tester**.  
> It is **not an official DAC checker**, not an official Sybil detector, and not an official reputation system.  
> The naming, scoring labels, thresholds, and interpretation logic are experimental community-defined heuristics created for testnet observation, reporting, and infrastructure research.

**Live:**  
- [DAC•Wallet Intelligence Layer](https://EdLWEISS186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1/)

![Version](https://img.shields.io/badge/version-v1.2.0-blue?style=flat-square)
![License](https://img.shields.io/badge/license-see%20root-lightgrey?style=flat-square)
![Testnet Only](https://img.shields.io/badge/network-testnet%20only-yellow?style=flat-square)
![Static Site](https://img.shields.io/badge/hosted-GitHub%20Pages-blue?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Read Only](https://img.shields.io/badge/mode-read%20only-brightgreen?style=flat-square)
![No Wallet Connect](https://img.shields.io/badge/wallet%20connect-not%20required-brightgreen?style=flat-square)

---

## Latest Version

### v1.2.0 — Versioned Scoring Policy

This release introduces a versioned scoring policy layer on top of the Transparent Scoring UI.

The purpose of this update is to make scoring easier to audit over time. If thresholds or scoring logic change in the future, older results can still be interpreted according to the policy version that generated them.

This version introduces:

- **Policy ID:** `WIL-2026-05-v1.2.0`
- **Policy Version:** `WIL-v1.2.0`
- **Policy Status:** `LOCKED`
- **Scoring Engine:** `versioned-reputation-scoring-v1.2.0`
- **Max Score:** `100`
- **Versioned scoring metadata in Raw JSON**
- **Locked threshold definitions for score components and labels**

The v1.1.1 NFT Participation percentage display remains included.


---

## Table of Contents

- [Overview](#overview)
- [Why This Exists](#why-this-exists)
- [Community Disclaimer](#community-disclaimer)
- [Interface Overview](#interface-overview)
- [Architecture](#architecture)
- [Scoring and Label Definitions](#scoring-and-label-definitions)
- [Transparent Scoring UI](#transparent-scoring-ui)
- [Versioned Scoring Policy](#versioned-scoring-policy)
- [Failure Handling Policy](#failure-handling-policy)
- [Network Configuration](#network-configuration)
- [Features](#features)
- [Local Usage](#local-usage)
- [Technical Notes](#technical-notes)
- [Security](#security)
- [Future Work](#future-work)
- [Changelog](#changelog)
- [License](#license)
- [Repository Context](#repository-context)

---

## Overview

The DAC Testnet is not only a transaction environment; it is also a behavioral data environment.

Transaction generators such as `DAC•SENDER` help create activity.  
This tool takes the opposite side of that workflow: it reads public activity and turns it into a structured wallet profile.

In simple terms:

```text
DAC•SENDER
→ helps create testnet activity

DAC Wallet Intelligence Layer
→ helps observe, classify, and document wallet activity
```

The checker is designed for community-level testnet analysis. It reads public explorer data, processes it in the browser, and presents a structured view of a wallet's activity and asset footprint.

No backend is used. No wallet connection is required. No private key is requested.

---

## Why This Exists

The idea behind this tool comes from ongoing DAC infrastructure contributions and from the function-task concept developed for the DAC / Truebit Etherscan API task library.

The related contribution introduced a `dac_wallet_intelligence` function task that takes pre-fetched wallet metrics and converts them into:

- wallet activity analytics
- NFT portfolio intelligence
- reputation scoring
- Sybil-risk estimation
- DAC testnet wallet profiling

This web interface extends that idea into a user-facing client-side checker.

The purpose is not to create an official ranking system.  
The purpose is to make wallet behavior easier to observe, explain, and document during testnet participation.

---

## Community Disclaimer

This project is a **community-built experimental checker**.

It is not:

- an official DAC product
- an official DAC reputation system
- an official DAC Sybil detector
- an eligibility checker for rewards, airdrops, incentives, or allowlists
- a final authority on wallet quality

All labels such as:

```text
VERY HIGH
ADVANCED TESTNET USER
ECOSYSTEM PARTICIPANT
NFT HEAVY
ADVANCED ECOSYSTEM USER
ELITE
LOW SYBIL RISK
```

are **community-defined interpretation labels** created by **JERUZZALEM — DAC Infra Tester**.

The same applies to the thresholds used to generate those labels.  
They are not official DAC thresholds.

This tool should be understood as an experimental observation layer for testnet analytics, not as a formal identity, ranking, or reward mechanism.

---

## Interface Overview

Screenshots are stored in the local `assets/` folder.

### Initial Interface

The default interface when the page is first opened.

![UI Interface](assets/UIInterface.png)

### Check Pending

The state after a user enters a wallet address and presses the check button.

![Check Pending](assets/CheckPending.png)

### Full Intelligence Ready

The state after the DAC Explorer returns all required wallet data and the full profile is generated.

![Full Intelligence Ready](assets/FullIntelligence-Ready.png)

### Wallet Output

The main wallet output panel containing balance, transaction metrics, activity analytics, portfolio intelligence, reputation scoring, scoring breakdown, and versioned scoring policy metadata.

![Wallet Output](assets/WalletOutput.png)

### Proof of Assets Engine

The NFT ownership panel generated from DAC Explorer `tokenlist` data.

![Proof of Assets Engine](assets/ProofOfAssetEngine.png)

### Raw Output

The raw JSON output generated by the checker.

![Raw Output](assets/RAWOutput.png)

---

## Architecture

The tool follows a modular client-side architecture.  
The current web implementation is shipped as static files, but the internal logic is organized around the following conceptual modules.

```text
┌──────────────────────────────────────────────────────────────┐
│ wallet-intelligence.html                                     │
│ UI input wallet address + result dashboard                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ wallet-intelligence.js                                       │
│ orchestration layer                                          │
│ coordinates explorer reads, fallback handling, and rendering │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ proof-native-funds.js                                        │
│ eth_getBalance / native tDACC balance                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ proof-assets-engine.js                                       │
│ NFT ownership / collections / assets                         │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ activity-analytics.js                                        │
│ transaction count + NFT transfer behavior                    │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ portfolio-intelligence.js                                    │
│ collection diversity + NFT concentration                     │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ reputation-scoring.js                                        │
│ score + level + Sybil risk                                   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│ Wallet Intelligence Layer                                    │
│ final wallet profile + raw JSON output                       │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```text
User pastes wallet address
        │
        ▼
wallet-intelligence.html
        │
        ▼
wallet-intelligence.js
        │
        ├── DAC Explorer API
        │   ├── balance
        │   ├── tokenlist
        │   ├── txlist
        │   └── tokennfttx
        │
        ├── Proof of Native Funds
        ├── Proof of Assets Engine
        ├── Activity Analytics v1
        ├── Portfolio Intelligence v1
        └── Reputation Scoring v1
        │
        ▼
Wallet Intelligence Layer output
```

### Primary Data Source

```text
https://exptest.dachain.tech/api
```

Used for:

```text
balance     → native DAC testnet balance
tokenlist   → ERC-721 NFT ownership
txlist      → transaction history count
tokennfttx  → NFT transfer activity count
```

### RPC Fallback

```text
https://rpctest.dachain.tech/
```

Used only when the explorer is unavailable.

RPC fallback can provide:

```text
eth_getBalance          → native balance
eth_getTransactionCount → outgoing transaction count / nonce
```

RPC fallback cannot fully replace the explorer because standard RPC does not provide complete NFT inventory or NFT transfer history.

---

## Scoring and Label Definitions

The scoring system is intentionally simple and transparent.

It is designed to turn observable testnet metrics into a readable wallet profile.

### Input Metrics

The full score requires all of the following verified explorer data:

| Metric | Source | Description |
|---|---|---|
| Native Balance | `balance` | Native DAC testnet token balance |
| Transaction Count | `txlist` | Number of explorer-indexed transactions |
| NFT Transfers | `tokennfttx` | Number of NFT transfer events involving the wallet |
| Total Collections | `tokenlist` | Number of ERC-721 collections held |
| Total NFT Holdings | `tokenlist` | Total ERC-721 items held across collections |

If one or more required explorer modules fail, the full reputation score is not generated.

---

### Activity Level

Activity level is based on total transaction count.

| Condition | Label |
|---|---|
| `txCount >= 1000` | `VERY HIGH` |
| `txCount >= 500` | `HIGH` |
| `txCount >= 100` | `MEDIUM` |
| below `100` | `LOW` |

These labels are not official DAC labels. They are community-defined categories for testnet observation.

---

### Engagement Type

Engagement type combines transaction activity with NFT participation.

| Condition | Label |
|---|---|
| `txCount > 1000` and `totalNFTs > 100` | `ADVANCED TESTNET USER` |
| `txCount > 500` and `totalCollections >= 10` | `ECOSYSTEM PARTICIPANT` |
| otherwise | `CASUAL USER` |

The label `ADVANCED TESTNET USER` means the wallet has shown high activity and broad NFT interaction under this scoring model. It does not imply official DAC recognition.

---

### NFT Participation

NFT Participation is shown as a percentage.

```text
nftParticipation = nftTransfers / txCount * 100
```

Example:

```text
0.19 ratio → 19.00%
```

If `txCount` is zero, the value is shown as `0.00%`.

This value is meant to show how much of the wallet's total activity is related to NFT transfer behavior.

---

### Diversity Score

Diversity score is based on the number of ERC-721 collections held.

| Condition | Label |
|---|---|
| `totalCollections >= 10` | `HIGH` |
| `totalCollections >= 5` | `MEDIUM` |
| below `5` | `LOW` |

This is a simple collection-diversity heuristic. It does not evaluate rarity, quality, legitimacy, floor price, or official collection status.

---

### Portfolio Style

Portfolio style is based on NFT holdings and collection count.

| Condition | Label |
|---|---|
| `totalNFTs > 100` and `totalCollections > 10` | `NFT HEAVY` |
| `totalNFTs > 0` | `BALANCED` |
| `totalNFTs = 0` | `NO NFT ASSETS` |

`NFT HEAVY` means the wallet has a large testnet NFT footprint under this model.

---

### Wallet Archetype

Wallet archetype combines native balance and NFT holdings.

| Condition | Label |
|---|---|
| `nativeBalance > 5` and `totalNFTs > 100` | `ADVANCED ECOSYSTEM USER` |
| otherwise | `STANDARD USER` |

This label is observational and not official.

---

### Concentration

Collection concentration measures how dominant the top NFT collection is inside the wallet.

```text
concentration = topCollectionAmount / totalNFTs * 100
```

| Condition | Label |
|---|---|
| `concentration >= 50%` | `HIGH` |
| `concentration >= 25%` | `MEDIUM` |
| below `25%` | `LOW` |

A higher concentration means the wallet's NFT holdings are more heavily focused on a single collection.

---

### Reputation Score

The reputation score is a 100-point community heuristic.

#### Transaction Score

| Condition | Points |
|---|---:|
| `txCount >= 1000` | `40` |
| `txCount >= 500` | `30` |
| `txCount >= 100` | `20` |
| below `100` | `10` |

#### NFT Diversity Score

| Condition | Points |
|---|---:|
| `totalCollections >= 10` | `25` |
| `totalCollections >= 5` | `15` |
| below `5` | `5` |

#### NFT Holdings Score

| Condition | Points |
|---|---:|
| `totalNFTs >= 200` | `20` |
| `totalNFTs >= 100` | `15` |
| below `100` | `5` |

#### Native Balance Score

| Condition | Points |
|---|---:|
| `nativeBalance >= 5` | `15` |
| `nativeBalance >= 1` | `10` |
| below `1` | `5` |

---

### Reputation Level

| Score | Label |
|---|---|
| `>= 90` | `ELITE` |
| `>= 75` | `HIGH` |
| `>= 50` | `MEDIUM` |
| below `50` | `LOW` |

Again, these are community-defined labels for testnet analytics only.

---

### Trust Profile

| Condition | Label |
|---|---|
| `txCount > 1000` and `totalCollections > 10` | `ADVANCED TESTNET PARTICIPANT` |
| otherwise | `STANDARD USER` |

This is not an identity verification system. It only summarizes observable activity under the current scoring logic.

---

### Sybil Risk

| Score | Label |
|---|---|
| `>= 90` | `LOW` |
| `>= 70` | `MEDIUM` |
| below `70` | `HIGH` |

This Sybil-risk label is a lightweight heuristic.  
It should not be treated as a definitive Sybil detection result.

The model does not inspect:

- wallet funding graph
- shared funding sources
- timing clusters
- gas behavior similarity
- device/IP data
- social identity
- off-chain proof
- official campaign rules

It only uses the public wallet metrics available through the DAC Explorer modules listed above.

---

## Transparent Scoring UI

Version `v1.1.0` introduced a transparent scoring panel.  
Version `v1.1.1` improved NFT Participation readability by changing decimal ratio output into percentage format.  
Version `v1.2.0` keeps both improvements and adds a versioned scoring policy layer.

The UI shows how the reputation score is built from four visible components:

```text
Transaction Score      /40
NFT Diversity Score    /25
NFT Holdings Score     /20
Native Balance Score   /15
```

Each component displays:

- points earned
- maximum possible points
- metric value used
- rule/condition matched

This makes the score easier to audit and reduces ambiguity for users reviewing their wallet status.

---

## Versioned Scoring Policy

Version `v1.2.0` introduces a locked scoring policy object.

The purpose is to make future scoring changes auditable. If a future version changes thresholds, labels, or point allocation, older outputs can still be interpreted according to the policy version that produced them.

Current policy metadata:

```text
Policy ID      : WIL-2026-05-v1.2.0
Policy Version : WIL-v1.2.0
Status         : LOCKED
Engine         : versioned-reputation-scoring-v1.2.0
Max Score      : 100
```

The raw JSON output includes scoring policy metadata:

```json
{
  "scoringPolicy": {
    "version": "WIL-v1.2.0",
    "policyId": "WIL-2026-05-v1.2.0",
    "status": "LOCKED",
    "model": "versioned-reputation-scoring-v1.2.0",
    "maxScore": 100,
    "components": {
      "transactionScore": {
        "maxPoints": 40,
        "thresholds": [
          { "condition": "txCount >= 1000", "points": 40 },
          { "condition": "txCount >= 500", "points": 30 },
          { "condition": "txCount >= 100", "points": 20 },
          { "condition": "txCount < 100", "points": 10 }
        ]
      },
      "nftDiversityScore": {
        "maxPoints": 25
      },
      "nftHoldingsScore": {
        "maxPoints": 20
      },
      "nativeBalanceScore": {
        "maxPoints": 15
      }
    },
    "labels": {
      "reputationLevel": "versioned label thresholds",
      "sybilRisk": "versioned label thresholds"
    }
  }
}
```

This policy is still a **community-defined heuristic** and should not be interpreted as an official DAC reputation, eligibility, or Sybil system.

---

## Failure Handling Policy

This tool follows a strict fail-safe rule:

```text
No verified data → no score
Partial data     → partial profile only
Full data        → full wallet intelligence
```

### Full Explorer Data

If all required explorer modules return valid data:

```text
balance
tokenlist
txlist
tokennfttx
```

the tool generates the full wallet intelligence profile.

### Partial Explorer Data

If only some explorer modules return valid data, the UI displays the available fields and marks the output as partial.

The full reputation score is not generated.

### Explorer Down

If the DAC Explorer is unavailable, the tool attempts RPC fallback.

### RPC Fallback

RPC fallback can only generate a limited native proof:

```text
native balance
outgoing transaction count / nonce
```

The following are not generated in RPC fallback mode:

```text
NFT portfolio
NFT transfer count
full activity analytics
portfolio intelligence
reputation score
Sybil-risk label
```

### Explorer and RPC Down

If both data sources fail, the tool displays an error state and a retry button.

No random score, mock score, or fabricated wallet profile is generated.

---

## Network Configuration

| Parameter | Value |
|---|---|
| Network Name | DAC Testnet |
| Chain ID | `21894` |
| RPC Endpoint | `https://rpctest.dachain.tech/` |
| Explorer | `https://exptest.dachain.tech` |
| Explorer API | `https://exptest.dachain.tech/api` |
| Native Symbol | `DACC` |
| Displayed Testnet Token | `tDACC` |

---

## Features

- **No wallet connection required** — users paste an address only.
- **Read-only design** — no transaction signing, no wallet prompt, no private key access.
- **Proof of Native Funds** — reads native balance from DAC Explorer.
- **Proof of Assets Engine** — reads ERC-721 ownership from `tokenlist`.
- **Activity Analytics v1** — generates activity level, engagement type, NFT participation percentage, and diversity score.
- **Portfolio Intelligence v1** — generates portfolio style, wallet archetype, top collection, concentration, and holdings summary.
- **Reputation Scoring v1** — generates a community-defined score from verified data.
- **Transparent Scoring UI** — displays each score component, matched rule, and earned points.
- **Versioned Scoring Policy** — includes locked policy metadata, policy ID, engine version, and threshold definitions in the raw JSON output.
- **Sybil-risk estimation** — lightweight score-based label, clearly marked as experimental.
- **Raw JSON Output** — export-ready structured profile for reporting.
- **Live Chain Stats** — block height, TPS estimate, block time, RPC latency, and gas price.
- **Retry Handling** — user can retry when explorer/RPC data fails.
- **GitHub Pages Ready** — static HTML/CSS/JS, no build step.

---

## Local Usage

Serve over HTTP. Do not test only through `file://`, because browser behavior can differ.

```bash
# From repository root
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1/
```

Example test wallet:

```text
0x870ad63acc507cdfd878F170606d19ae78988AFE
```

---

## Technical Notes

- Static client-side application.
- No backend.
- No database.
- No wallet provider required.
- Uses DAC Explorer API as the primary data source.
- Uses DAC RPC only as a limited fallback.
- Does not use random/mock data in production.
- All scoring is performed locally in the browser.
- `Proof of Assets Engine` currently focuses on ERC-721 ownership.
- There is currently only one primary DAC Explorer endpoint used by this checker.
- Raw JSON now includes versioned scoring policy metadata.
- The current implementation is shipped in `index.html`, `wallet-intelligence.css`, and `wallet-intelligence.js`; the module names in the architecture section describe the conceptual separation of logic.

---

## Security

- **No private keys.** The tool never requests or accesses private keys.
- **No wallet connection.** The tool does not call `eth_requestAccounts`.
- **No signing.** The tool does not submit transactions or request signatures.
- **No backend data collection.** The tool is hosted as a static GitHub Pages interface.
- **Public data only.** The profile is built only from public explorer/RPC responses.
- **No official eligibility claim.** The result should not be interpreted as qualification for rewards, incentives, or official recognition.

---

## Future Work

Potential future directions, depending on available explorer data, contract design, and verification requirements.

- **Known collection registry** — supplement explorer data with curated DAC NFT collection metadata, beginning with known official/community-visible collections such as DAC Inception Rank when appropriate.
- **Historical activity windowing** — classify recent activity separately from lifetime activity.
- **Explorer-only Sybil heuristics** — improve Sybil-risk estimation using logic derived from public explorer data, without depending on a custom backend.
- **Mintable / dynamic intelligence badge** — optional future NFT badge layer based on wallet status, preferably designed as an updateable or evolving badge rather than a static one.
- **Truebit function-task mode** — optionally compare browser output with a verified function-task execution path.

---

## Changelog

### v1.2.0 — Versioned Scoring Policy

- Added locked scoring policy metadata.
- Added Policy ID: `WIL-2026-05-v1.2.0`.
- Added policy status: `LOCKED`.
- Added scoring engine label: `versioned-reputation-scoring-v1.2.0`.
- Added versioned component thresholds and label definitions to raw JSON output.
- Added policy metadata panel to the scoring breakdown section.

### v1.1.1 — NFT Participation Percentage Display Fix

- Changed NFT Participation display from decimal ratio to percentage format.
- Example: `0.19` → `19.00%`.
- Updated scoring policy metadata to `WIL-v1.1.1`.

### v1.1.0 — Transparent Scoring UI

- Added visible scoring breakdown panel.
- Added per-category score components.
- Added rule/condition display for each score component.
- Added scoring policy metadata to raw JSON output.

### v1 — Initial Release

Initial release of the community-built DAC Wallet Intelligence Layer.

---

## License

This project is part of the [`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the root repository license.

---

## Repository Context

This tool is part of a broader DAC infrastructure contribution archive.

The `Sender-Web` folder focuses on testnet transaction generation and user-facing interaction tooling.

This folder, under:

```text
DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1/
```

is intended as an archive and continuation of DAC contribution work related to wallet intelligence, explorer-based analytics, and the related function-task concept from the DAC / Truebit Etherscan API task library.

---

*Authored by **JERUZZALEM** — DAC Infra Tester*  
