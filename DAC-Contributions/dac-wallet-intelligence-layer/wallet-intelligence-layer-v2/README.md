# DAC Wallet Intelligence Layer v2.0.2

Client-side wallet intelligence interface and dynamic Wallet Status SBT layer for the **DAC Quantum Chain Testnet**.

This version is a continuation of the previous [Wallet Intelligence Layer v1](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1) contribution.

The checker reads public DAC testnet data from explorer/RPC sources, converts a pasted wallet address into a structured wallet profile, and provides an optional mint/update path for a dynamic wallet-bound badge.

> This is a community-built engineering tool by **JERUZZALEM — DAC Infra Tester**.  
> It is not an official DAC product, not an official eligibility checker, not a definitive Sybil detection system, and not a financial scoring system.

**Live Interface**

- [Wallet Intelligence Layer v2](https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2/)

![Version](https://img.shields.io/badge/version-v2.0.2-blue?style=flat-square)
![Network](https://img.shields.io/badge/network-DAC%20testnet-yellow?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![Mode](https://img.shields.io/badge/mode-wallet%20intelligence%20%2B%20SBT-brightgreen?style=flat-square)
![Wallet Check](https://img.shields.io/badge/wallet%20check-no%20connect%20required-brightgreen?style=flat-square)
![Mint Mode](https://img.shields.io/badge/mint%2Fupdate-wallet%20signature%20required-orange?style=flat-square)
![Backend](https://img.shields.io/badge/backend-none-lightgrey?style=flat-square)

---

## Latest Version

### v2.0.2 — Dynamic Wallet Status SBT

Version `v2.0.2` is the current Wallet Intelligence Layer v2 release.

This release extends the read-only wallet intelligence interface into an optional dynamic SBT workflow. Users can paste a wallet address, check wallet status, preview the dynamic Wallet Status badge, and optionally mint one wallet-bound SBT.

Current active contract:

```text
Wallet Status SBT : 0xdE02dfbf28563f80733423678477357dF9040b14
Name              : Wallet Status SBT
Symbol            : Status
Token Type        : ERC-5192 locked SBT
Image Mode        : Dynamic SVG
Transferability   : Locked
Mint Price        : 1 DACC
Update Price      : 0.001 DACC
```

Key updates in v2.0.2:

- Added dynamic Wallet Status SBT preview.
- Added wallet-bound SBT minting flow.
- Added ERC-5192 locked badge behavior.
- Added dynamic `tokenURI()` metadata.
- Added dynamic SVG rendering per wallet.
- Added DAC logo placement inside the dynamic badge.
- Added DAC Sender NFT Launchpad registry compatibility.
- Added Launchpad filtering for deprecated Wallet Status test contracts.
- Added Launchpad dynamic artwork support for Wallet Status SBT.
- Kept wallet intelligence checking as a no-connect pasted-address flow.

GitHub project folder:

```text
https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2
```

---

## Table of Contents

- [Overview](#overview)
- [Project Context](#project-context)
- [Community and Engineering Disclaimer](#community-and-engineering-disclaimer)
- [Interface Overview](#interface-overview)
- [User Flow](#user-flow)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [Network Configuration](#network-configuration)
- [Wallet Intelligence Layer](#wallet-intelligence-layer)
- [Dynamic Wallet Status SBT](#dynamic-wallet-status-sbt)
- [Wallet Status SBT Contract](#wallet-status-sbt-contract)
- [Dynamic SVG Rendering](#dynamic-svg-rendering)
- [Token Metadata](#token-metadata)
- [DAC Sender NFT Launchpad Integration](#dac-sender-nft-launchpad-integration)
- [Deprecated Registry Entries](#deprecated-registry-entries)
- [Security Model](#security-model)
- [Failure Handling](#failure-handling)
- [Local Usage](#local-usage)
- [Technical Notes](#technical-notes)
- [Future Work](#future-work)
- [Changelog](#changelog)
- [License](#license)
- [Author](#author)

---

## Overview

The DAC Testnet is not only a transaction environment. It is also a public behavioral data environment.

`DAC•SENDER` helps generate testnet activity.  
`DAC Wallet Intelligence Layer` reads public wallet activity and converts it into structured wallet intelligence.  
`Wallet Status SBT` turns the resulting wallet profile into a dynamic, wallet-bound badge.

```text
DAC•SENDER
→ creates and routes testnet activity

DAC Wallet Intelligence Layer
→ observes, classifies, and documents wallet activity

Wallet Status SBT
→ represents the wallet profile as one evolving non-transferable badge
```

The wallet checker itself does not require a wallet connection. Users paste a wallet address and press `Check Status`.

A wallet popup is only triggered when the user chooses to mint or update the SBT. At that point, the browser wallet signs the transaction. The frontend never receives private keys and does not custody funds.

---

## Project Context

Wallet Intelligence Layer v2 continues the work started in [Wallet Intelligence Layer v1](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v1).

v1 focused on explorer-based wallet intelligence, scoring policy, NFT portfolio review, reputation scoring, Sybil heuristics, DAC Inception Rank signal, DACC stake signal, stress-testing links, and raw JSON output.

v2 extends the same concept with a dynamic badge layer:

```text
v1
→ read-only wallet intelligence checker

v2
→ read-only wallet intelligence checker
→ dynamic Wallet Status SBT preview
→ optional wallet-bound mint/update flow
→ DAC Sender NFT Launchpad visibility
```

Project location:

```text
DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2/
```

---

## Community and Engineering Disclaimer

This project is a **community-built engineering tool**.

It is not an official DAC product, official DAC eligibility checker, official DAC reputation system, official DAC Sybil detector, reward checker, airdrop checker, or allowlist verification tool.

All labels, thresholds, profile classifications, and interpretations are community-defined.

The checker does not prove whether a wallet is Sybil or non-Sybil. It only evaluates visible DAC testnet behavior patterns from a single-wallet point of view.

The Wallet Status SBT is a testnet identity and contribution experiment. It should not be interpreted as a financial score, credit score, security guarantee, or official DAC endorsement.

---

## Interface Overview

Screenshots should be stored in the local `assets/` folder.

### Initial Interface

Default interface state before a wallet check is executed.

```text
assets/InitialInterface.png
```

### Check Pending

State after a wallet address is pasted and the check process is running.

```text
assets/CheckPending.png
```

### Wallet Intelligence Ready

State after explorer/RPC modules return usable data and the wallet profile is generated.

```text
assets/WalletIntelligenceReady.png
```

### Dynamic Intelligence Badge

Wallet Status SBT preview panel with dynamic SVG output.

```text
assets/DynamicIntelligenceBadge.png
```

### Mint / Update Flow

Optional wallet-triggered transaction flow for minting or updating the Wallet Status SBT.

```text
assets/MintUpdateFlow.png
```

### DAC Sender NFT Launchpad

Final Wallet Status SBT collection and user-owned SBT visibility inside DAC Sender NFT Launchpad.

```text
assets/LaunchpadIntegration.png
```

---

## User Flow

The main wallet intelligence flow is read-only.

```text
Paste wallet address
↓
Click Check Status
↓
Frontend reads public explorer/RPC data
↓
Wallet profile is generated
↓
Dynamic badge preview appears
```

The optional mint/update flow starts only after the user decides to mint or update the SBT.

```text
User clicks Mint Badge / Update Badge
↓
Frontend prepares smart contract transaction
↓
Browser wallet popup appears
↓
User reviews and signs
↓
Transaction is submitted to DAC Testnet
↓
SBT becomes visible in explorer and Launchpad
```

Important wallet model:

```text
Wallet intelligence check : no wallet connection required
Mint/update transaction   : wallet popup and user signature required
Private key handling      : never exposed to the frontend
Backend custody           : none
```

---

## Architecture

The current implementation is shipped as static frontend files:

```text
index.html
wallet-intelligence.css
wallet-intelligence.js
README.md
assets/
```

Conceptual module layout:

```text
index.html
└── UI shell, wallet input, status cards, dynamic badge preview, mint/update actions

wallet-intelligence.js
├── explorer / RPC orchestration
├── native balance reads
├── NFT and Rank badge signal reads
├── wallet profile classification
├── activity analytics panels
├── portfolio intelligence panels
├── reputation scoring panels
├── dynamic badge preview
├── Wallet Status SBT contract calls
└── mint/update transaction trigger

wallet-intelligence.css
└── visual layout, dashboard styling, dynamic badge styling, responsive behavior
```

No build step is required.

---

## Data Sources

### Primary Explorer API

```text
https://exptest.dachain.tech/api
```

Used for public DAC testnet wallet data where explorer-indexed data is required.

### RPC Endpoint

```text
https://rpctest.dachain.tech/
```

Used for:

```text
eth_getBalance
eth_getTransactionCount
eth_getBlockByNumber
eth_call
contract read calls
```

### Smart Contract Reads

The v2 interface also reads Wallet Status SBT and DAC Inception Rank badge signals through contract calls.

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
| DAC Inception Rank Contract | `0xB36ab4c2Bd6aCfC36e9D6c53F39F4301901Bd647` |
| Wallet Status SBT Contract | `0xdE02dfbf28563f80733423678477357dF9040b14` |
| DACNFTRegistry | `0x34CDf37FeEb81877acabAD601AAaA3AE5a5029Ae` |

---

## Wallet Intelligence Layer

Wallet Intelligence Layer v2 continues the wallet profiling idea from v1.

The interface can display structured wallet information such as:

```text
Native DACC balance
Wallet activity summary
NFT-related signals
DAC Inception Rank badge count
Pattern health
Sybil risk estimate
Inception rank label
Wallet archetype
Native balance tier
Dynamic badge class
```

The output is designed for:

- infrastructure testing
- testnet participation review
- wallet behavior analysis
- community analytics
- public-data debugging
- dynamic testnet identity experiments

---

## Dynamic Wallet Status SBT

Wallet Status SBT is the dynamic badge layer of v2.0.2.

Each wallet can hold one evolving badge.

```text
1 wallet = 1 badge
```

The badge is designed to reflect:

```text
verified core on-chain status
DAC Inception Rank signal
native DACC balance tier
wallet profile state
```

The badge can be updated if the wallet profile changes.

---

## Wallet Status SBT Contract

Final active contract:

```text
0xdE02dfbf28563f80733423678477357dF9040b14
```

Contract constructor RankBadge source:

```text
0xB36ab4c2Bd6aCfC36e9D6c53F39F4301901Bd647
```

Key contract behavior:

```text
Name              : Wallet Status SBT
Symbol            : Status
Token Type        : ERC-5192 locked SBT
Transferability   : Locked
Mint Price        : 1 DACC
Update Price      : 0.001 DACC
Max Mint per Wallet: 1
```

Transfers and approvals are disabled.

```text
approve()
setApprovalForAll()
transferFrom()
safeTransferFrom()
```

These actions revert because the token is soulbound.

---

## Dynamic SVG Rendering

The badge image is generated dynamically.

The contract exposes:

```text
dynamicSvgOf(address)
dynamicImageOf(address)
tokenURI(uint256)
```

The web interface uses:

```text
dynamicSvgOf(address)
```

for the preview, because inline SVG rendering allows the DAC logo IPFS asset to display correctly in the browser.

Final approved DAC logo placement:

```text
logoCID : bafkreiehizlkhvgeayzghwtppno5wy3ynmxylwd2mtstomjlgtazt5x2xy
x       : 972.5
y       : 972.5
width   : 155
height  : 155
```

---

## Token Metadata

Final NFT description:

```text
Wallet Status is a dynamic DAC Testnet badge generated by the DAC Wallet Intelligence Layer v2. Each wallet can hold one evolving badge that reflects its verified core on-chain status, DAC Inception Rank signal, native DACC balance tier, and wallet profile state.
```

Typical metadata traits include:

```text
Main Badge Class
Pattern Health
Sybil Risk
Inception Rank
Archetype
Rank Badge Count
Native Balance Tier
Wallet Address
Version
Token Type
Transferability
Image Mode
Verification Mode
```

IPFS assets:

```text
DAC Logo without background:
bafkreiehizlkhvgeayzghwtppno5wy3ynmxylwd2mtstomjlgtazt5x2xy

Collection Cover Image:
bafkreihsmz6zxg5lhdtzmljclxyxxsth2p6qgnw2ozfpob3kwva3g5tssa

Collection Metadata:
bafkreihphts6njtszzbkg6p3ant7n4qr3vgtm345yzuipsrspmobfrqh2e
```

---

## DAC Sender NFT Launchpad Integration

Wallet Status SBT is registered into the existing DAC Sender NFT Launchpad registry.

```text
DACNFTRegistry:
0x34CDf37FeEb81877acabAD601AAaA3AE5a5029Ae
```

After registration, the collection appears in:

```text
DAC Sender NFT Launchpad
→ Collections
```

After a user mints, it also appears in:

```text
DAC Sender NFT Launchpad
→ My Collections
```

Launchpad compatibility functions include:

```text
name()
symbol()
totalSupply()
maxSupply()
maxMintPerWallet()
mintPrice()
mintedPerWallet(address)
mint(uint256)
```

The Launchpad was patched to support the dynamic artwork model used by Wallet Status SBT.

For the final Wallet Status SBT contract, the Launchpad can render:

```text
dynamicSvgOf(connected wallet address)
```

inside collection cards, detail pages, and user collection views.

---

## Deprecated Registry Entries

Two previous Wallet Status test entries are intentionally hidden from DAC Sender NFT Launchpad UI:

```text
0xC790a1f6b314267e88F6ef2FcB66537DD2C4e1a2
0x28aA8D67Bb4BeCF5ad6fc5E28f5B971FebB29cFf
```

They are not deleted from the on-chain registry because the registry appears append-only.

The Launchpad UI filters them out so only the final version is shown.

Final visible version:

```text
0xdE02dfbf28563f80733423678477357dF9040b14
```

---

## Security Model

### Wallet Intelligence Check

- No wallet connection required.
- No signature required.
- No private key access.
- No backend account.
- No server-side database.
- Public explorer/RPC data only.

### Mint / Update Transaction

- User action required.
- Browser wallet popup required.
- User signs transaction manually.
- Frontend only triggers the smart contract call.
- Private keys remain inside the user's wallet.

### General

- No backend custody.
- No off-chain identity scoring.
- No IP/device-based scoring.
- No hidden user account system.

The project is a static client-side application.

---

## Failure Handling

The checker follows a fail-safe output model:

```text
Verified data      → full profile
Partial data       → partial profile
RPC fallback only  → limited profile
No verified data   → no score
```

No random score, mock score, fabricated wallet profile, or placeholder analytics should be generated.

For the SBT preview:

```text
Valid dynamic SVG  → render preview
SVG unavailable    → fallback UI state
Contract mismatch  → no mint/update action
Wallet already has badge → show update state
```

---

## Local Usage

Run from the repository root:

```bash
python3 -m http.server 8080
```

Then open:

```text
http://localhost:8080/DAC-Contributions/dac-wallet-intelligence-layer/wallet-intelligence-layer-v2/
```

Example wallet:

```text
0x870ad63acc507cdfd878F170606d19ae78988AFE
```

---

## Technical Notes

- Static HTML/CSS/JS implementation.
- No build step.
- No backend service.
- GitHub Pages compatible.
- Explorer API is used for indexed public data.
- RPC is used for fallback and contract reads.
- Wallet check is pasted-address based.
- Mint/update uses browser wallet transaction signing.
- Wallet Status SBT is ERC-5192 locked.
- Dynamic SVG is generated by the smart contract.
- DAC logo is loaded from IPFS inside the dynamic SVG.
- Launchpad supports dynamic SBT artwork for the final contract.

---

## Future Work

Potential future directions:

- More precise on-chain activity categorization.
- Expanded known DAC ecosystem collection registry.
- Better historical activity visualization.
- Dedicated status update history.
- Optional badge evolution timeline.
- Additional dynamic badge styles for different wallet archetypes.
- Cleaner Launchpad-level support for dynamic token artwork.
- More complete explorer-side metadata indexing if available.

---

## Changelog

### v2.0.2 — Dynamic Wallet Status SBT

- Added final Wallet Status SBT contract.
- Added ERC-5192 locked SBT behavior.
- Added one badge per wallet rule.
- Added dynamic `tokenURI()`.
- Added dynamic SVG badge rendering.
- Added DAC logo IPFS asset support.
- Added final approved v8 logo placement.
- Added Wallet Intelligence Layer web preview for dynamic SVG.
- Added mint/update frontend trigger.
- Added DAC Sender NFT Launchpad registry support.
- Added Launchpad dynamic artwork rendering.
- Added filtering for deprecated Wallet Status registry entries.
- Updated README and project documentation.

### v2.0.1 — Wallet Status Badge Prototype

- Added initial Wallet Status badge interface.
- Added badge preview layout.
- Added preliminary on-chain profile reads.
- Added test deployment workflow.

### v2.0.0 — Wallet Intelligence Layer v2 Foundation

- Started v2 folder structure.
- Extended v1 wallet intelligence concept.
- Added Dynamic Intelligence Badge section.
- Prepared SBT-oriented workflow.

---

## License

This project is part of the [`dac-dual-node-cgnat-setup`](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the root repository license.

---

## Author

**JERUZZALEM**  
DAC Infra Tester

Built by Communities for Communities.
