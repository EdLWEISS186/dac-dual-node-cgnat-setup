# DAC Sender — Testnet Transaction Interface

A client-side web interface for submitting native DACC token transactions on the DAC Quantum Chain Testnet. Built as part of an ongoing infrastructure testing effort to evaluate network behavior under realistic transaction load prior to mainnet deployment.

**Live:**
- [DAC•SENDER](https://EdLWEISS186.github.io/dac-dual-node-cgnat-setup/Sender-Web/) — Main interface: Send, Deploy Contract, Deploy NFT
- [DAC•SENDER NFT Launchpad](https://EdLWEISS186.github.io/dac-dual-node-cgnat-setup/Sender-Web/mint.html) — Browse and mint NFT collections deployed through DAC•SENDER

![Version](https://img.shields.io/badge/version-v1.4.3-orange?style=flat-square)
![License](https://img.shields.io/badge/license-see%20root-lightgrey?style=flat-square)
![Testnet Only](https://img.shields.io/badge/network-testnet%20only-yellow?style=flat-square)
![Static Site](https://img.shields.io/badge/hosted-GitHub%20Pages-blue?style=flat-square)
![Chain ID](https://img.shields.io/badge/chain%20ID-21894-blueviolet?style=flat-square)
![ethers.js](https://img.shields.io/badge/ethers.js-v6-green?style=flat-square)
![No Build](https://img.shields.io/badge/build-none%20required-brightgreen?style=flat-square)
![Last Commit](https://img.shields.io/github/last-commit/EdLWEISS186/dac-dual-node-cgnat-setup?style=flat-square)

---

## Latest Version

### v1.4.3 — Real-time Stats & NFT Launchpad Polish

This patch release completes the NFT Launchpad infrastructure and adds live network monitoring across both `index.html` and `mint.html`.

**Real-time Stats Bar** — Block height, TPS (averaged from last 5 blocks), block time, RPC latency with color-coded health indicators (green/yellow/red), and live gas price in Gwei. Pre-loads 5 blocks on init for immediate data without waiting for the next polling cycle.

**NFT Launchpad** (`mint.html`) — Rebuilt with a proper two-tab interface: Collections (reads from on-chain `DACNFTRegistry`) and My Collections (reads `mintedPerWallet` for the connected address across all registered collections). Includes a connect wallet overlay consistent with `index.html`, improved error handling for RPC failures with retry, and a contextual empty state for wallets with no mints.

**Connect Overlay** — Both `index.html` and `mint.html` now open with a consistent blur overlay showing `DAC•SENDER`, version, and connect prompt. `mint.html` adds an NFT Launchpad subtitle and a "Browse without connecting" option.

---

### v1.3.0 — Multi-Send & Metrics Export

**Multi-Send**
Batch token distribution to multiple recipients in a single signed transaction. Users configure the recipient count, enter or randomize each address individually, set a per-address amount, and submit — the `DACMultiSend` smart contract handles distribution within a single block execution. No repeated signing. Directly applicable for generating high-volume, multi-destination transaction load on the testnet.

**Metrics Export**
Session transaction history is exportable as a CSV file at any point during an active session. Fields include transaction type, hash, recipient addresses, amount, total dispatched, confirmation status, ISO timestamp, and gas consumed.

---

### v1.2.0

**Deploy Contract**
One-click smart contract deployment directly from the browser. No Hardhat, no Remix, no CLI. Connect wallet, click Deploy, sign — contract is live on DAC Testnet.

**Protocol Fee Toggle**
An opt-in protocol fee mechanism available on both Send and Deploy tabs. When enabled, transactions are routed through a proxy smart contract that applies a 5% fee on gas cost. Disclosed transparently via the ⓘ indicator. Users retain full control over whether to enable it.

**Why this feature exists**

Beyond the fee mechanism itself, routing transactions through a proxy smart contract serves a direct infrastructure testing purpose. A direct native token transfer (`EOA → EOA`) is the simplest possible transaction type — it exercises only the most basic execution path on the EVM. When transactions are routed through a smart contract intermediary, the execution profile changes significantly: the EVM must parse and execute contract bytecode, process internal calls, handle state writes, emit events, and manage value forwarding across contract boundaries. This produces a fundamentally different load pattern on the network.

In practice, this means the Protocol Fee toggle enables the collection of behavioral data that a plain transfer cannot provide — specifically around smart contract execution performance, internal transaction handling, gas accounting under contract call overhead, and the accuracy of block explorer indexing for complex transaction types. Validator nodes must process not just the outer transaction but also resolve the internal call stack, which stresses the execution layer in ways that are representative of how real dApp interactions will behave on mainnet.

The Deploy Contract feature follows the same reasoning: deploying a contract generates a contract creation transaction, which exercises a different and heavier EVM code path than any transfer or call. Combined, these features allow testnet participants to contribute transaction load that spans the full spectrum of EVM execution types — native transfers, contract calls, and contract creation — producing a more complete picture of network readiness before mainnet.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Screenshots](#screenshots)
- [Why Transaction Volume Matters on Testnet](#why-transaction-volume-matters-on-testnet)
  - [1. Network Throughput and Stability](#1-network-throughput-and-stability)
  - [2. RPC Infrastructure Resilience](#2-rpc-infrastructure-resilience)
  - [3. Consensus Under Pressure](#3-consensus-under-pressure)
  - [4. Block Propagation and Network Latency](#4-block-propagation-and-network-latency)
  - [5. Smart Contract and dApp Ecosystem Validation](#5-smart-contract-and-dapp-ecosystem-validation)
  - [6. Mainnet Simulation](#6-mainnet-simulation)
  - [7. Bug Discovery Beyond Internal Testing](#7-bug-discovery-beyond-internal-testing)
  - [8. Telemetry Collection](#8-telemetry-collection)
  - [9. Geographic Distribution Testing](#9-geographic-distribution-testing)
  - [10. Tokenomics and UX Verification](#10-tokenomics-and-ux-verification)
- [Why Multi-Wallet Traffic Specifically](#why-multi-wallet-traffic-specifically)
- [What This Gives the Development Team](#what-this-gives-the-development-team)
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

The DAC Testnet is not just a staging environment — it is an active stress-testing ground. A blockchain behaves fundamentally differently under real multi-user traffic compared to isolated internal testing. The goal of this tool is to make it easy for community members to contribute genuine transaction activity, which directly supports pre-mainnet engineering validation objectives.


---

## Interface Overview

### DAC•SENDER — index.html

**Send DACC — native token transfer with single and batch (Multi-Send) dispatch:**

![Send DACC Tab](assets/index-send.png)

**Deploy Contract — one-click `DACInception` contract deployment:**

![Deploy Contract Tab](assets/index-deploySC.png)

**Deploy NFT — ERC-721 collection deployment with IPFS upload and mint link generation:**

![Deploy NFT Tab](assets/index-DeployNFT.png)

**Bridge — pending DAC team infrastructure, documentation and status disclosed:**

![Bridge Tab](assets/index-Bridge.png)

---

### DAC•SENDER NFT Launchpad — mint.html

**Collections — all NFT collections deployed through DAC•SENDER, read from on-chain registry with live supply data:**

![Collections Tab](assets/mint-collection.png)

**My Collections — NFTs minted by the connected wallet, resolved against the on-chain registry:**

![My Collections Tab](assets/mint-mycollection.png)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                         │
│                                                             │
│   ┌──────────────┐        ┌──────────────────────────────┐  │
│   │ EVM Wallet   │◄──────►│     DAC Sender (index.html)  │  │
│   │ Rabby/MM     │  sign  │  ethers.js v6 · static HTML  │  │
│   └──────────────┘        └──────────────┬───────────────┘  │
└──────────────────────────────────────────┼──────────────────┘
                                           │
          ┌──────────────────────────┬─────┴────────────┬─────────────────┐
          │                          │                  │                 │
          ▼                          ▼                  ▼                 ▼
          ┌─────────────┐  ┌──────────────────┐  ┌──────────────┐  ┌─────────────┐
          │ Direct Send │  │  Proxy Contract  │  │   Deploy     │  │  Deploy NFT │
          │  EOA → EOA  │  │  DACSendProxy    │  │  Contract    │  │  ERC-721    │
          └──────┬──────┘  └────────┬─────────┘  └──────┬───────┘  └──────┬──────┘
                 │                  │                   │                 │
                 └────────────────────────────┴───────────────────────────┘
                                         │
                                         ▼
                            ┌────────────────────────┐
                            │    DAC Testnet (EVM)   │
                            │    Chain ID: 21894     │
                            │    RPC: rpctest...     │
                            └────────────┬───────────┘
                                         │
                                         ▼
                            ┌────────────────────────┐
                            │   Block Explorer       │
                            │   exptest.dachain.tech │
                            └────────────────────────┘
```

---

## Screenshots

### Direct Send

**Pending — transaction submitted, awaiting confirmation:**

![Direct Sending Pending](assets/DirectSending-Pending.png)

**Success — transaction confirmed:**

![Direct Sending Success](assets/DirectSending-Success.png)

**Block Explorer — confirmed on-chain:**

![Direct Sending Explorer](assets/DirectSending-Success-Exp.png)

---

### Send via Protocol Contract

**Pending — transaction routed through proxy smart contract:**

![Smart Contract Send Pending](assets/SendingThroughSmartContract-Pending.png)

**Success — confirmed, internal fee transfer visible:**

![Smart Contract Send Success](assets/SendingThroughSmartContract-Success.png)

**Block Explorer — internal transactions visible:**

![Smart Contract Send Explorer](assets/SendingThroughSmartContract-Success-Exp.png)

---

### Deploy Contract

**Pending — DACInception deployment submitted:**

![Deploy Contract Pending](assets/DeployContract-Pending.png)

**Success — contract address returned:**

![Deploy Contract Success](assets/DeployContract-Success.png)

**Block Explorer — contract creation confirmed:**

![Deploy Contract Explorer](assets/DeployContract-Success-Exp.png)

---

### Deploy via Protocol Contract

**Pending — deployment routed through proxy:**

![Deploy Through Smart Contract Pending](assets/DeployContractThroughSmartContract-Pending.png)

**Success — contract deployed with fee processed:**

![Deploy Through Smart Contract Success](assets/DeployContractThroughSmartContract-Success.png)

**Block Explorer — internal transactions visible alongside deployment:**

![Deploy Through Smart Contract Explorer](assets/DeployContractThroughSmartContract-Success-Exp.png)


---

### Batch Send (Multi-Send)

**Pending — multi-send transaction submitted, one signature for all recipients:**

![Batch Send Pending](assets/SendingBatch-Pending.png)

**Success — all recipients confirmed in a single transaction:**

![Batch Send Success](assets/SendingBatch-Success.png)

**Block Explorer — internal transfers visible per recipient:**

![Batch Send Explorer](assets/SendingBatch-Success-Exp.png)

---

### Metrics Export

Sample export from an active session (`dac-sender-metrics.csv`):

| Type | Hash | Recipients | Amount | Total | Status | Gas Used |
|---|---|---|---|---|---|---|
| multi-send | `0x324d...79d9` | 10 addresses | 0.0001 DACC | 0.001 DACC | success | 132,053 |

Each row captures: transaction type, full hash, all recipient addresses, per-address amount, total dispatched, confirmation status, ISO timestamp, and gas consumed. Intended for structured documentation of testnet activity.

**Sample export file:** [dac-sender-metrics-1778672188075.csv](assets/dac-sender-metrics-1778672188075.csv)


---

### Deploy NFT

**Pending — DACInceptionNFT contract deployment submitted:**

![Deploy NFT Pending](assets/DeployNFT-Pending.png)

**Success — contract deployed, mint link generated:**

![Deploy NFT Success](assets/DeployNFT-Success.png)

**Block Explorer — contract creation confirmed:**

![Deploy NFT Explorer](assets/DeployNFT-Success-Exp.png)

---

### Deploy NFT via Protocol Contract

**Pending — deployment routed through proxy:**

![Deploy NFT Through Smart Contract Pending](assets/DeployNFT-ThroughSmartContract-Pending.png)

**Success — contract deployed with fee processed:**

![Deploy NFT Through Smart Contract Success](assets/DeployNFT-ThroughSmartContract-Success.png)

**Block Explorer — internal transactions visible:**

![Deploy NFT Through Smart Contract Explorer](assets/DeployNFT-ThroughSmartContract-Success-Exp.png)

---

### NFT Launchpad (mint.html)

**NFT Launchpad — the public-facing mint portal generated from a DAC•SENDER deploy. Each deployed collection automatically receives a shareable mint link that opens this interface, displaying collection metadata, live supply, and a mint form connected directly to the on-chain contract:**

![Launchpad](assets/Launchpad.png)

**Pending — mint transaction submitted:**

![Mint NFT Pending](assets/Launchpad-MintNFT-Pending.png)

**Success — mint confirmed:**

![Mint NFT Success](assets/Launchpad-MintNFT-Success.png)

**Block Explorer — mint transaction confirmed:**

![Mint NFT Explorer](assets/Launchpad-MintNFT-Success-Exp.png)

**Block Explorer — NFT token view:**

![Mint NFT Token Explorer](assets/Launchpad-MintNFT-Success-Exp-NFT.png)

**NFT visible in wallet:**

![Show on Wallet](assets/Show%20on%20wallet.png)

---

## Why Transaction Volume Matters on Testnet

### 1. Network Throughput and Stability
High transaction volume puts real pressure on validator nodes. Key metrics that only become visible under load:
- **TPS** (Transactions Per Second)
- **Finalization time**
- **Mempool behavior**
- **Block propagation latency**
- **Gas handling accuracy**

A network that performs cleanly with ten transactions may exhibit degradation at a thousand.

### 2. RPC Infrastructure Resilience
Every transaction submitted through a wallet touches the RPC layer. Under concurrent load, common failure modes include:
- RPC timeout / connection drops
- `"Still connecting..."` stalls
- Dropped transactions
- Nonce mismatch errors

This tool helps surface those failures in a controlled testnet context before they affect mainnet users.

### 3. Consensus Under Pressure
Each transaction forces the validator set to:
1. Receive and validate the transaction
2. Agree on transaction ordering
3. Commit the transaction to a block
4. Propagate the block to all peers

Testing with real traffic from multiple wallets exposes edge cases such as fork/reorg events, missed blocks, bad blocks, validator downtime, and peer instability.

### 4. Block Propagation and Network Latency
As block size grows with transaction volume, the cost of propagating blocks across the peer network increases. This helps measure:
- Block delay under load
- Network latency between nodes
- Peer-to-peer connection stability

### 5. Smart Contract and dApp Ecosystem Validation
Transaction activity is not limited to token transfers. Testnet traffic validates the full application layer — DEX swaps, NFT minting, staking contracts, governance interactions — ensuring the entire ecosystem functions correctly on top of the chain.

### 6. Mainnet Simulation
On mainnet, thousands of users will interact with the network simultaneously from different wallets, regions, and devices. The testnet must replicate that usage pattern as closely as possible before launch.

### 7. Bug Discovery Beyond Internal Testing
Certain classes of bugs only manifest under real multi-user conditions:
- Race conditions
- Memory leaks
- RPC bottlenecks
- Database corruption
- Sync lag
- Chain reorganization

Internal testing with a single developer and a few wallets will not surface these.

### 8. Telemetry Collection
Active transaction load generates the data that infrastructure operators need:
- CPU, RAM, and disk I/O under stress
- Network bandwidth consumption
- Error log frequency and patterns
- Block time consistency

### 9. Geographic Distribution Testing
Transactions submitted from users across different regions test:
- Global latency
- Peer discovery quality
- Cross-region connectivity

### 10. Tokenomics and UX Verification
Even with no economic value, testnet transactions validate:
- Fee calculation accuracy
- Wallet UX and edge cases
- Block explorer indexing
- Balance update propagation

---

> **Analogy:** A blockchain is like a highway. Internal testing is a few cars on an empty road. Community testnet is thousands of vehicles from different cities. Mainnet is production traffic. If congestion appears at the testnet stage, it can be resolved before it affects real users.

---

## Why Multi-Wallet Traffic Specifically

Sending repeated transactions from a single developer wallet does not produce representative results. Real traffic requires:
- **Different wallets** — different nonce sequences and state paths
- **High transaction count** — sustained mempool pressure
- **Non-uniform timing** — irregular block fill patterns
- **Geographic spread** — latency variation across peers

This tool enables community members to contribute that traffic without requiring technical setup beyond a browser and a wallet.

---

## What This Gives the Development Team

| Signal | What It Reveals |
|---|---|
| RPC response time under load | Infrastructure capacity |
| Validator sync consistency | Consensus stability |
| Block time variance | Network reliability |
| Chain reorganization events | Fork resistance |
| Explorer data accuracy | Indexing pipeline health |

---

## Network Configuration

| Parameter | Value |
|---|---|
| Network Name | DAC Testnet |
| Chain ID | `21894` |
| RPC Endpoint | `https://rpctest.dachain.tech` |
| Currency Symbol | `DACC` |
| Block Explorer | `https://exptest.dachain.tech` |

The wallet is automatically prompted to switch to or register the DAC Testnet network upon connection. Users operating a local full node may override the RPC endpoint within their wallet settings — the application operates against whichever endpoint the wallet uses, provided the Chain ID is `21894`.

---

## Features

- **EVM Wallet Integration** — Connects to any `window.ethereum`-compatible wallet via the standard provider API
- **Live Balance Display** — Fetches and displays the connected account's native DACC balance
- **Quick Amount Presets** — One-click shortcuts for `0.001`, `0.01`, `0.1`, and `MAX`
- **Random Recipient Selection** — Picks a recipient from a curated address pool on demand
- **Transaction Log Panel** — Real-time status tracking (`PENDING` → `SUCCESS` / `FAILED`) with per-hash block explorer links
- **Auto Network Switch** — Issues `wallet_switchEthereumChain` / `wallet_addEthereumChain` automatically on connect
- **Disconnect Wallet** — Click the wallet address in the topbar to reveal the disconnect option
- **Deploy Contract** — One-click deployment of the `DACInception` contract directly from the browser
- **Protocol Fee Toggle** — Opt-in mechanism on both Send and Deploy tabs; routes transactions through a proxy smart contract when enabled
- **Multi-Send (Batch)** — Send to multiple recipients in a single signed transaction via `DACMultiSend` contract; each recipient address is individually configurable or randomized from the pool
- **Metrics Export** — Download session transaction history as CSV (hash, recipients, amount, status, timestamp, gas used)
- **Deploy NFT** — Full ERC-721 collection deployment with IPFS artwork and metadata upload via Pinata
- **NFT Launchpad** (`mint.html`) — Shared public page for browsing and minting all NFT collections deployed through DAC•Sender, powered by an on-chain registry contract
- **Real-time Network Stats** — Live TPS, block time, RPC latency, gas price, and block height displayed in the stats bar

---

## Local Usage

This is a static single-file application. Serve over HTTP — do not open via `file://` protocol, as wallet extensions do not inject `window.ethereum` into file-scheme pages.

```bash
# Node.js
npx serve .

# Python
python -m http.server 8080
```

---

## Node-Level Evidence

The following is an excerpt from the local node log captured during an active testing session using this tool. The node was running with a local RPC endpoint; however, once transactions are broadcast to the network they propagate to all peers including official DAC validator and RPC nodes, producing equivalent log entries across the network.

```
INFO Imported new chain segment  blocks=1  txs=39  mgas=1.994  elapsed=144ms   number=14,825,499
INFO Submitted transaction        hash=0xc519...bf15  from=0x870a...8AFE  nonce=604  recipient=0x06eB...7565  value=1,000,000,000,000,000
INFO Imported new chain segment  blocks=1  txs=35  mgas=1.690  elapsed=58ms    number=14,825,501
INFO Imported new chain segment  blocks=1  txs=46  mgas=2.232  elapsed=62ms    number=14,825,502
INFO Imported new chain segment  blocks=1  txs=66  mgas=3.009  elapsed=120ms   number=14,825,503
INFO Submitted transaction        hash=0x474d...6e0d  from=0x870a...8AFE  nonce=605  recipient=0x2674...2090  value=1,000,000,000,000,000
INFO Chain reorg detected         number=14,825,505  hash=d5db8b..cc5b82  drop=1  add=1
INFO Imported new chain segment  blocks=1  txs=64  mgas=2.925  elapsed=53ms    number=14,825,506
INFO Submitted contract creation  hash=0x5e35...0f02  from=0x870a...8AFE  nonce=606  contract=0xF1b5...FB18  value=0
INFO Imported new chain segment  blocks=1  txs=62  mgas=4.010  elapsed=206ms   number=14,825,510
INFO Submitted contract creation  hash=0x6c39...eaca  from=0x870a...8AFE  nonce=607  contract=0xc1a6...A63f  value=0
```

Key observations from this session:

- **Block load:** 35–66 transactions per block, 1.69–4.01 mgas per block — consistent with active mempool pressure
- **Block time:** approximately 10–20 seconds between imports — within expected range for the current validator set
- **Chain reorganization at block 14,825,505** — a fork event where one block was dropped and replaced. This is precisely the type of consensus-layer behavior that only becomes observable under real multi-user transaction load. The network resolved it within one block
- **Contract creation confirmed** — two `DACInception` deployments visible in the same session, demonstrating the full range of transaction types generated by this tool

---

## Technical Notes

- Single `index.html` — no build step, no npm dependencies at runtime
- Transaction signing delegated entirely to the connected wallet via `ethers.js v6` (`BrowserProvider` + `Signer`)
- Gas estimation handled by the wallet and RPC node — no manual configuration exposed
- Amount parsing uses `ethers.parseEther()` — correct handling of 18-decimal EVM precision
- Contract bytecode compiled with `evmVersion: london` — compatible with chains that have not implemented the Shanghai hard fork (`PUSH0` opcode not present)
- JavaScript logic obfuscated — source is not human-readable on inspection
- Hosted on GitHub Pages — HTTPS enforced, no server-side logic

---

## Security

- **Private keys never leave the wallet.** The application never requests, stores, or transmits private keys. All transaction signing is performed exclusively by the connected wallet extension.
- **No backend.** This is a fully static application. There is no server, no database, and no data collection of any kind.
- **No external dependencies at runtime.** The only external resource loaded is `ethers.js` from a CDN and Google Fonts. No analytics, no tracking scripts.
- **Smart contract interactions are transparent.** When the Protocol Fee toggle is enabled, the proxy contract address and its internal transactions are fully visible on the block explorer. Users can verify all on-chain behavior independently.

---

## Future Work

### v1.5.0 — Bridge (Pending DAC Team Infrastructure)

Cross-chain bridging between DAC Testnet and external testnets (e.g., Ethereum Sepolia) requires infrastructure that cannot be built at the application layer alone. Specifically:

- **Bridge smart contracts** must be deployed on both chains by the DAC development team, as they require coordinated deployment with privileged administrative access.
- **A relayer service** — a backend process running 24/7 that monitors events on both chains and triggers cross-chain message execution — must be operated by a party with persistent uptime, which is beyond the scope of a community-hosted static frontend.
- **Liquidity provisioning** on both sides of the bridge must be initialized and maintained.

This feature is planned for implementation once the DAC team publishes their official bridge contract addresses and relayer infrastructure. The frontend integration can be completed on this end once those dependencies are available.

---

## Changelog

### v1.4.3
- Added **Real-time Stats Bar** to both `index.html` and `mint.html` — TPS, block time, RPC latency, gas price
- **NFT Launchpad** (`mint.html`) rebuilt with two-tab layout: Collections + My Collections
- Added **Connect Wallet overlay** to `mint.html` matching `index.html` style
- Improved error handling for RPC failures with Retry button
- Fixed transaction log panel height — viewport-based, scrollable inside fixed frame
- Stats bar repositioned to below topbar on both pages

### v1.4.2
- Added **Deploy NFT** tab with IPFS upload via Pinata and ERC-721 deployment
- Added **NFT Launchpad** (`mint.html`) with on-chain registry (`DACNFTRegistry`)
- Added **Mint Link** generation after NFT deploy
- Added "Built by Communities for Communities" subtitle in topbar
- Updated proxy contract fee cap to 1 DACC absolute maximum

### v1.4.1
- Fixed protocol fee proxy contract — replaced percentage-based cap with 1 DACC absolute cap
- Prevents excessive fees during gas price spikes

### v1.4.0
- Added **Deploy NFT** tab — ERC-721 collection deployment with IPFS artwork upload via Pinata
- Added **NFT Launchpad** (`mint.html`) with on-chain `DACNFTRegistry` contract
- Added **Mint Link** generation post-deploy
- Added **MY COLLECTIONS** tab in `mint.html`
- Added **Connect Wallet overlay** to `mint.html`
- Added "Built by Communities for Communities" subtitle in topbar

### v1.3.1
- Fixed Multi-Send address row alignment — CSS Grid layout applied for consistent column structure

### v1.3.0
- Added **Multi-Send** — batch dispatch to N recipients via `DACMultiSend` smart contract, single wallet signature
- Per-row address inputs with individual and bulk randomize options
- Added **Metrics Export** — CSV download of full session transaction history

### v1.2.0
- Added **Deploy Contract** tab — one-click `DACInception` contract deployment
- Added **Protocol Fee toggle** on Send and Deploy tabs — opt-in proxy routing with ⓘ disclosure tooltip
- Added **Disconnect Wallet** — click wallet pill in topbar to disconnect
- Fixed decimal separator — amount input now correctly uses `.` regardless of system locale
- Added version indicator in topbar
- JavaScript obfuscation applied

### v1.1.0
- Random recipient selection from curated address pool
- Transaction log panel with block explorer links
- Auto network switch to DAC Testnet on connect
- Deployed to GitHub Pages

### v1.0.0
- Initial release — native DACC token send interface

---

## License

This project is part of the [dac-dual-node-cgnat-setup](https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup) repository and is covered by the [LICENSE](../LICENSE) file in the root of that repository.

---

## Repository Context

This tool is part of a broader infrastructure testing setup documented in the parent repository, covering dual-node single-machine deployment under CGNAT, automated node management with process monitoring and logging, and a Prometheus + Grafana observability stack for the DAC Quantum Chain Testnet.

---

*Authored by **JERUZZALEM** — DAC Infra Tester*
