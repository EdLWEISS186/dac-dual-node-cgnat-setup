# DAC Domain

![status](https://img.shields.io/badge/status-v1%20deployed-brightgreen)
![registry](https://img.shields.io/badge/registry-explorer--friendly-blue)
![network](https://img.shields.io/badge/network-DAC%20Testnet-orange)
![chain](https://img.shields.io/badge/chain%20id-21894%20%7C%200x5586-yellow)
![tld](https://img.shields.io/badge/TLD-.dac-purple)
![frontend](https://img.shields.io/badge/frontend-GitHub%20Pages-black)
![author](https://img.shields.io/badge/author-JERUZZALEM-gold)

**DAC Domain** is an experimental on-chain `.dac` domain registry for the DAC Testnet.

The project provides a wallet-name identity layer where readable `.dac` names can resolve to DAC Testnet wallet addresses.

```text
jeruzzalem.dac -> 0x870ad63acc507cdfd878F170606d19ae78988AFE
```

> DAC Domain is a community-built testnet infrastructure experiment. It is not an official DAC name service.

---

## Live Links

| Resource | Link |
|---|---|
| Live Frontend | https://edlweiss186.github.io/dac-dual-node-cgnat-setup/DAC-Domain/ |
| Repository Folder | https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup/tree/main/DAC-Domain |
| Active v1 Registry | https://exptest.dachain.tech/address/0x90F07E7EFa772c40B90d68BB54267Ea0658a090F |
| v1 Deployment TX | https://exptest.dachain.tech/tx/0x4e3ab77b099bb7e2149f17dc9465e5e760c0d3dd96790df11aafce482eeb1c90 |
| v1 Domain Registration TX | https://exptest.dachain.tech/tx/0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce |
| v1 Primary Domain TX | https://exptest.dachain.tech/tx/0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a |
| DAC Public RPC | https://rpctest.dachain.tech/ |
| DAC Explorer | https://exptest.dachain.tech/ |
| DAC Explorer API | https://exptest.dachain.tech/api |

---

## Table of Contents

- [Overview](#overview)
- [Network](#network)
- [Current Status](#current-status)
- [v1 Explorer-Friendly Registry](#v1-explorer-friendly-registry)
- [v0.5 Archived Prototype](#v05-archived-prototype)
- [Architecture Topology](#architecture-topology)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Local Development](#local-development)
- [Useful Commands](#useful-commands)
- [Deployment Notes](#deployment-notes)
- [Explorer Visibility Notes](#explorer-visibility-notes)
- [Archive Notes](#archive-notes)
- [Disclaimer](#disclaimer)
- [Author](#author)

---

## Overview

DAC Domain started as a lightweight `.dac` registry prototype and evolved into a deployed explorer-friendly registry for DAC Testnet.

The project includes:

- A static GitHub-hosted frontend.
- A DAC-themed domain registration UI.
- Wallet connection and DACC balance display.
- Smart contract based `.dac` domain registration.
- Owned-domain management.
- Primary domain selection.
- CLI scripts for deployment, registration, resolution, and event decoding.
- Archive notes for technical reporting and infrastructure observation.

The current active version is **v1.0.0 — Explorer-Friendly Registry**.

---

## Network

| Item | Value |
|---|---|
| Network | DAC Testnet |
| Public RPC | `https://rpctest.dachain.tech/` |
| Local RPC used for deployment/testing | `http://127.0.0.1:8546` |
| Chain ID | `21894` / `0x5586` |
| Explorer | `https://exptest.dachain.tech` |
| Explorer API | `https://exptest.dachain.tech/api` |
| Native Currency | DACC |
| TLD | `.dac` |

---

## Current Status

```text
v0.5: Archived Prototype
v1: Deployed and validated
Active Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Test Domain: jeruzzalem.dac
Primary Domain: jeruzzalem.dac
```

v0.5 proved the core `.dac` registry flow.  
v1 improved event readability by emitting readable domain names in decoded event logs.

---

## v1 Explorer-Friendly Registry

| Item | Value |
|---|---|
| Version | v1.0.0 — Explorer-Friendly Registry |
| Registry Contract | `0x90F07E7EFa772c40B90d68BB54267Ea0658a090F` |
| Deployment TX | `0x4e3ab77b099bb7e2149f17dc9465e5e760c0d3dd96790df11aafce482eeb1c90` |
| Deployer | `0x870ad63acc507cdfd878F170606d19ae78988AFE` |
| Registered Test Domain | `jeruzzalem.dac` |
| Registration TX | `0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce` |
| Primary Domain TX | `0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a` |
| NameHash | `0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246` |
| Status | Deployed and validated |

### v1 Validation Result

v1 successfully registered and resolved `jeruzzalem.dac`.

```text
Domain: jeruzzalem.dac
Registry: 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F
Owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Target: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Registered At: 2026-06-05T16:26:17.000Z
Updated At: 2026-06-05T16:26:17.000Z
Expires At: 2027-06-05T16:26:17.000Z
Registration Years: 1
Active: true
```

Decoded v1 event logs confirmed readable domain data:

```text
Event: DomainRegistered
nameHash: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
name: jeruzzalem.dac
owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
target: 0x870ad63acc507cdfd878F170606d19ae78988AFE
registrationYears: 1
pricePaid: 5000000000000000000
```

```text
Event: PrimaryDomainSet
owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
nameHash: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
name: jeruzzalem.dac
```

### v1 Event Model

v1 emits both an indexed hash and a readable domain name:

```solidity
bytes32 indexed nameHash
string name
```

This makes the event useful for both filtering/indexing and human-readable reporting.

---

## v0.5 Archived Prototype

| Item | Value |
|---|---|
| Version | v0.5 — Archived Prototype |
| Registry Contract | `0x72BD75723ADA5e37F6bA4b8909864c3bbaBccB63` |
| Deployment TX | `0xe97e92b860257dacdbb791ad5d12862127d9e8d0b74c28e063df44f2f68968e5` |
| Replaced Pending TX | `0x0514ff8cf8949c4885f34da793f4a2ada8b10b3dc02c15be80bd3b981b992af6` |
| Deployer | `0x870ad63acc507cdfd878F170606d19ae78988AFE` |
| Registered Test Domain | `jeruzzalem.dac` |
| Registration Duration | 1 Year |
| Registration Price | 5 DACC |
| Primary Domain Test | Successful |
| Status | Archived prototype |

### Why v0.5 Was Archived

v0.5 worked functionally, but its event schema was not ideal for explorer-readable domain logs.

The main limitation was:

```text
string indexed name
```

For indexed dynamic types like `string`, event topics store hashes rather than readable text. This made `jeruzzalem.dac` harder to inspect directly in logs.

v1 replaced that pattern with:

```text
bytes32 indexed nameHash
string name
```

This keeps the event filterable while also preserving the domain name as readable event data.

---

## Architecture Topology

DAC Domain uses a lightweight static dApp architecture connected to a custom on-chain `.dac` registry contract on DAC Testnet.

```text
                           ┌──────────────────────────────┐
                           │          End User            │
                           │  Wallet + Browser Interface  │
                           └──────────────┬───────────────┘
                                          │
                                          │ Connect wallet
                                          │ Sign tx / read state
                                          ▼
┌────────────────────────────────────────────────────────────────────┐
│                         DAC Domain Frontend                        │
│                                                                    │
│  index.html                                                        │
│  ├─ Register Domain UI                                             │
│  ├─ Domain Management UI                                           │
│  ├─ Primary Domain UI                                              │
│  └─ Advanced Settings fallback                                     │
│                                                                    │
│  src/app.js                                                        │
│  ├─ Wallet connection                                              │
│  ├─ Domain input normalization                                     │
│  ├─ Availability checking                                          │
│  ├─ Registration tx builder                                        │
│  ├─ Owned-domain loader                                            │
│  ├─ Primary-domain setter                                          │
│  └─ Registry contract binding                                      │
│                                                                    │
│  src/style.css + assets/background                                 │
│  └─ DAC visual identity, rotating background, glass UI             │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               │ ethers.js
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                      Wallet Provider Layer                         │
│                                                                    │
│  Browser wallet / MetaMask-compatible provider                     │
│  ├─ Account: 0x870ad63...988AFE                                    │
│  ├─ Network: DAC Testnet                                           │
│  ├─ Chain ID: 21894 / 0x5586                                       │
│  └─ Native currency: DACC                                          │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               │ JSON-RPC
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                         RPC Access Layer                           │
│                                                                    │
│  Public RPC                                                        │
│  └─ https://rpctest.dachain.tech/                                  │
│                                                                    │
│  Local RPC used for deployment/testing                             │
│  └─ http://127.0.0.1:8546                                          │
│                                                                    │
│  Local RPC was used because public RPC showed instability during   │
│  deployment preparation.                                           │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                           DAC Testnet                              │
│                                                                    │
│  DACDomainRegistry v1                                              │
│  └─ 0x90F07E7EFa772c40B90d68BB54267Ea0658a090F                     │
│                                                                    │
│  Registry State                                                    │
│  ├─ records[name]                                                  │
│  │  ├─ owner                                                       │
│  │  ├─ target                                                      │
│  │  ├─ registeredAt                                                │
│  │  ├─ updatedAt                                                   │
│  │  ├─ expiresAt                                                   │
│  │  └─ registrationYears                                           │
│  ├─ ownerDomains[wallet]                                           │
│  └─ primaryDomainByOwner[wallet]                                   │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                    Explorer / Reporting Layer                      │
│                                                                    │
│  DAC Explorer                                                      │
│  ├─ Transaction inspection                                         │
│  ├─ Contract address inspection                                    │
│  ├─ Event/log visibility                                           │
│  └─ Address activity                                               │
│                                                                    │
│  v1 Improvement                                                    │
│  └─ Domain names are emitted as readable event data together with  │
│     an indexed nameHash for filtering/indexing.                    │
│                                                                    │
│  Future Integration Goal                                           │
│  └─ Explorer/indexer-level .dac name-service support.              │
└────────────────────────────────────────────────────────────────────┘
```

### Development and Deployment Topology

```text
Developer / DAC Infra Tester
        │
        │ Hardhat scripts
        ▼
DAC-Domain/scripts/
├─ deploy.js              -> deploy registry contract
├─ deploy-v1.js           -> deploy v1 registry with manual gas settings
├─ replace-deploy.js      -> replace pending deployment tx by nonce
├─ register.js            -> register .dac domain from CLI
├─ resolve.js             -> inspect registry state from CLI
└─ decode-events.js       -> decode registry events from tx receipts

        │
        │ Uses .env
        ▼
hardhat.config.js
├─ network: dacTestnet
├─ chainId: 21894
└─ rpc: DAC_RPC_URL

        │
        │ Sends tx through
        ▼
Local DAC RPC Node
└─ http://127.0.0.1:8546

        │
        ▼
DAC Testnet
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `index.html` | Main static UI structure for registration and domain management. |
| `src/style.css` | DAC visual identity, rotating background support, glass UI, layout styling. |
| `src/app.js` | Wallet connection, domain normalization, availability check, registration, owned-domain loading, primary-domain actions. |
| Browser Wallet | Provides account, balance, chain connection, and transaction signing. |
| RPC Layer | Sends reads and transactions to DAC Testnet. Local RPC was used for reliable deployment/testing. |
| `DACDomainRegistry.sol` | Stores `.dac` records, owner mappings, expiry data, primary domain state, and readable event data. |
| Hardhat Scripts | Compile, deploy, replace pending deploy tx, register domains, resolve registry records, and decode events. |
| DAC Explorer | Used for transaction, address, and contract inspection. Explorer-wide name replacement still requires explorer/indexer integration. |

---

## Features

### Frontend

- DAC-themed static web interface
- GitHub-hosting friendly structure
- rotating 3-image DAC background slideshow
- 10-second fade transition
- 10% dark overlay
- glass-style readability panels
- wallet connection
- DACC balance display
- short wallet address display
- `.dac` domain input
- availability check
- registration duration selector
- dynamic price display
- Domain Management screen
- owned domain list
- primary domain selection
- primary domain clearing
- renewal button
- Advanced Settings for registry contract fallback

### Smart Contract

- `.dac` name validation
- wallet target resolution
- registration pricing
- expiry tracking
- domain renewal
- owned domain listing
- primary domain selection
- readable domain event data
- indexed name hash for filtering/indexing
- contract owner withdrawal

### Pricing

| Duration | Price |
|---|---:|
| 1 Year | 5 DACC |
| 2 Years | 8 DACC |
| 3 Years | 10 DACC |

---

## Folder Structure

```text
DAC-Domain/
├── assets/
│   └── background/
│       ├── bg-1.png
│       ├── bg-2.png
│       └── bg-3.png
├── contracts/
│   └── DACDomainRegistry.sol
├── deployments/
│   ├── dac-testnet.json
│   └── archive/
│       └── v0.5/
│           └── dac-testnet-v0.5.json
├── docs/
│   └── archive/
│       ├── dac-domain-v0.5-archive-note.md
│       ├── dac-domain-v1-explorer-friendly-archive-note.md
│       └── v0.5/
│           ├── DACDomainRegistry-v0.5.sol
│           └── README.md
├── scripts/
│   ├── decode-events.js
│   ├── deploy.js
│   ├── deploy-v1.js
│   ├── register.js
│   ├── replace-deploy.js
│   └── resolve.js
├── src/
│   ├── app.js
│   └── style.css
├── hardhat.config.js
├── index.html
├── package.json
├── package-lock.json
├── .env.example
├── .gitignore
└── README.md
```

---

## Local Development

Install dependencies:

```bash
npm install
```

Compile contract:

```bash
npm run compile
```

Run local frontend:

```bash
python3 -m http.server 8081
```

Open:

```text
http://localhost:8081
```

---

## Useful Commands

Compile:

```bash
npm run compile
```

Deploy v1 registry:

```bash
GAS_PRICE_GWEI=100 npx hardhat run scripts/deploy-v1.js --network dacTestnet
```

Register a domain:

```bash
DOMAIN_NAME=jeruzzalem.dac REGISTRATION_YEARS=1 npm run register:dac
```

Resolve a domain:

```bash
DOMAIN_NAME=jeruzzalem.dac npm run resolve:dac
```

Decode v1 events:

```bash
npm run decode-events:dac -- \
  0xb8524d29a47261be3ea65eefe9fe089a11d4a806d8e9b3ace5359c9ad9e110ce \
  0x0c093b06cfb5525d4734bb5af2539a970f6ab1b280cdbb763a6728d9a1fdf82a
```

---

## Deployment Notes

The v0.5 and v1 deployments used the user's local DAC node RPC:

```text
http://127.0.0.1:8546
```

This was used because the official public RPC showed instability during deployment preparation.

v0.5 required a replacement deployment transaction because the first contract creation became pending due to low gas price. v1 was deployed directly with manual gas settings:

```bash
GAS_PRICE_GWEI=100 npx hardhat run scripts/deploy-v1.js --network dacTestnet
```

---

## Explorer Visibility Notes

DAC Domain v1 improves explorer-facing data by emitting readable names in event data:

```text
nameHash: 0x25992959442c572a45da6926192bd643f9c52487d3bc370bfa8fb24a5f52f246
name: jeruzzalem.dac
```

This does not automatically make DAC Explorer replace every wallet address with `.dac` names in normal transactions. Explorer-wide address replacement requires explorer/indexer-level name-service integration.

---

## Archive Notes

Detailed archive notes:

```text
docs/archive/dac-domain-v0.5-archive-note.md
docs/archive/dac-domain-v1-explorer-friendly-archive-note.md
```

v0.5 remains as an archived proof-of-concept. v1 is the active deployed registry version.

---

## Disclaimer

This is an independent community-built DAC Testnet infrastructure experiment.

It is not an official DAC name service and does not represent official DAC infrastructure policy.

The `.dac` registry data is stored in a custom smart contract deployed on DAC Testnet. Explorer-wide name replacement, such as displaying `jeruzzalem.dac` instead of a wallet address on every transaction page, requires explorer-side or indexer-side name-service integration.

Availability, ownership, primary-domain status, and event logs are based on the deployed DAC Domain registry contract and should be interpreted as experimental testnet data.

---

## Author

**JERUZZALEM — DAC Infra Tester**

Built by Communities for Communities
