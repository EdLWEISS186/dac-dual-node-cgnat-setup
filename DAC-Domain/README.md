# DAC Domain

DAC Domain is an experimental on-chain `.dac` domain registry for the DAC Testnet.

The project provides a wallet-name identity layer where readable `.dac` names can resolve to DAC Testnet wallet addresses.

Example:

```text
jeruzzalem.dac -> 0x870ad63acc507cdfd878F170606d19ae78988AFE
```

> DAC Domain is a community-built testnet infrastructure experiment. It is not an official DAC name service.

---

## Current Project Direction

DAC Domain is moving from **v0.5 Archived Prototype** into **v1 Explorer-Friendly Registry**.

The v0.5 prototype successfully proved the full end-to-end flow:

- smart contract deployment
- wallet connection
- `.dac` domain availability checking
- `.dac` domain registration
- domain management UI
- primary domain selection
- script-based resolution
- local RPC deployment through a self-hosted DAC node

However, v0.5 is archived because its event schema is not optimized for explorer readability. v1 will improve the contract events so registered domain names are easier to inspect in explorer logs and technical reports.

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

### v0.5 Result

The v0.5 registry was successfully deployed and tested on DAC Testnet.

Resolution test result:

```text
Domain: jeruzzalem.dac
Owner: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Target: 0x870ad63acc507cdfd878F170606d19ae78988AFE
Registered At: 2026-06-05T15:02:17.000Z
Updated At: 2026-06-05T15:02:17.000Z
Expires At: 2027-06-05T15:02:17.000Z
Registration Years: 1
Active: true
```

### Why v0.5 Was Archived

v0.5 works functionally, but the event schema is not ideal for explorer-readable domain logs.

The main limitation:

```text
string indexed name
```

For indexed dynamic types like `string`, the event topic stores a hash rather than the readable text. This means explorer logs may not clearly show `jeruzzalem.dac` as plain text.

v1 will replace this pattern with an explorer-friendlier event structure:

```text
bytes32 indexed nameHash
string name
```

This keeps the event filterable while also making the domain name visible as readable event data.

---

## Architecture Topology

DAC Domain uses a lightweight static dApp architecture connected to a custom on-chain `.dac` registry contract on DAC Testnet.

```text
                           ┌──────────────────────────────┐
                           │          End User             │
                           │  Wallet + Browser Interface  │
                           └──────────────┬───────────────┘
                                          │
                                          │ Connect wallet
                                          │ Sign tx / read state
                                          ▼
┌────────────────────────────────────────────────────────────────────┐
│                         DAC Domain Frontend                         │
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
│  └─ DAC visual identity, rotating background, glass UI              │
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
│  Local RPC was used because public RPC showed instability during    │
│  deployment preparation.                                           │
└──────────────────────────────┬─────────────────────────────────────┘
                               │
                               ▼
┌────────────────────────────────────────────────────────────────────┐
│                           DAC Testnet                              │
│                                                                    │
│  DACDomainRegistry v0.5                                            │
│  └─ 0x72BD75723ADA5e37F6bA4b8909864c3bbaBccB63                     │
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
│  v0.5 Limitation                                                   │
│  └─ Domain names are functionally stored, but not ideal for         │
│     explorer-readable logs because of indexed string events.        │
│                                                                    │
│  v1 Goal                                                           │
│  └─ Emit readable domain names in event data with indexed hashes.   │
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
├─ replace-deploy.js      -> replace pending deployment tx by nonce
├─ register.js            -> register .dac domain from CLI
└─ resolve.js             -> inspect registry state from CLI

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
| `DACDomainRegistry.sol` | Stores `.dac` records, owner mappings, expiry data, and primary domain state. |
| Hardhat Scripts | Compile, deploy, replace pending deploy tx, register domains, and resolve registry records. |
| DAC Explorer | Used for transaction, address, and contract inspection. |

---

## v1 Planned Direction

v1 will preserve the working features from v0.5 while improving event design and reportability.

Planned v1 goals:

- explorer-friendly `DomainRegistered` event
- plain readable domain names in event data
- indexed `nameHash` for filtering
- cleaner registration logs
- clearer primary domain logs
- improved deployment metadata
- frontend default registry update to the v1 contract
- re-register `jeruzzalem.dac` on the v1 registry
- validate registration, management, and primary domain flow again

Recommended v1 event direction:

```solidity
event DomainRegistered(
    bytes32 indexed nameHash,
    string name,
    address indexed owner,
    address indexed target,
    uint8 registrationYears,
    uint256 expiresAt,
    uint256 pricePaid,
    uint256 timestamp
);
```

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
│   └── dac-testnet.json
├── docs/
│   └── archive/
│       └── dac-domain-v0.5-archive-note.md
├── scripts/
│   ├── deploy.js
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

## Deployment Notes

The v0.5 deployment used the user's local DAC node RPC:

```text
http://127.0.0.1:8546
```

This was used because the official public RPC showed instability during deployment preparation.

The initial deployment transaction became pending due to low gas price and was replaced using the same nonce with a higher gas price.

Successful replacement command:

```bash
GAS_PRICE_GWEI=100 REPLACE_NONCE=2627 npx hardhat run scripts/replace-deploy.js --network dacTestnet
```

This preserved the deterministic contract creation address:

```text
0x72BD75723ADA5e37F6bA4b8909864c3bbaBccB63
```

---

## Archive

Detailed v0.5 archive note:

```text
docs/archive/dac-domain-v0.5-archive-note.md
```

v0.5 will remain as an archived proof-of-concept. v1 will be the next active development version.

---

## Status

```text
v0.5: Archived Prototype
v1: In development
```

Made by JERUZZALEM — DAC Infra Tester  
Built by Communities for Communities
