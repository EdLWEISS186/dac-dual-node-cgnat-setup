# Testnet (Inception) — Technical Reports

The following reports document technical findings from field testing conducted during active contribution to the **DAC Testnet (Inception)** campaign. Each report covers a distinct infrastructure, compatibility, application-layer, or on-chain tooling issue identified through independent observation, diagnostics, development, and validation testing.

---

## Table of Contents

| # | Report | Date |
|---|--------|------|
| 1 | [Critical RPC Availability Issue & Network Access Bottleneck](./1.%20Critical%20RPC%20Availability%20Issue%20%26%20Network%20Access%20Bottleneck.pdf) | May 5, 2026 |
| 2 | [Testnet Infrastructure Validation Report](./2.%20Testnet%20Infrastructure%20Validation%20Report.pdf) | May 7, 2026 |
| 3 | [EIP-1559 Compatibility & Txpool Analysis](./3.%20EIP-1559%20Compatibility%20%26%20Txpool%20Analysis.pdf) | May 9, 2026 |
| 4 | [Frontend–Blockchain State Desynchronization After Successful NFT Mint](./4.%20Frontend%E2%80%93Blockchain%20State%20Desynchronization%20After%20Successful%20NFT%20Mint.pdf) | May 10, 2026 |
| 5 | [Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation](./5.%20Official%20Enode%20Evolution%20Analysis%20%E2%80%94%20Infrastructure%20Rotation%20%26%20Network%20Maturation.pdf) | May 11, 2026 |
| 6 | [DAC SENDER — Testnet Transaction Interface](./6.%20DAC%20SENDER%20%E2%80%94%20Testnet%20Transaction%20Interface.pdf) | May 22, 2026 |
| 7 | [Wallet Intelligence Layer — Wallet Intelligence, Dynamic Wallet Status SBT, and DAC Sender Launchpad Integration](./7.%20Wallet%20Intelligence%20Layer%20%E2%80%94%20Wallet%20Intelligence%2C%20Dynamic%20Wallet%20Status%20SBT%2C%20and%20DAC%20Sender%20Launchpad%20Integration.pdf) | May 28, 2026 |

---

## Report Summaries

**1. Critical RPC Availability Issue & Network Access Bottleneck** — *May 5, 2026*
> Initiated after widespread community reports of wallets stuck on "Still connecting to DAC Chain Testnet…". Direct JSON-RPC probing of all official enodes revealed that 6 of 7 nodes were unresponsive, and the public RPC endpoint (rpctest.dachain.tech) was returning 504 Gateway Time-out. The P2P/consensus layer remained operational — the bottleneck was isolated to the RPC layer.

**2. Testnet Infrastructure Validation Report** — *May 7, 2026*
> Follow-up validation using a dual-node single-machine setup (Windows + WSL Ubuntu) to test RPC stability, wallet interoperability, and transaction propagation. Localhost RPC endpoints significantly outperformed the public endpoint. OKX Wallet and Rabby Wallet transacted successfully, while MetaMask transactions remained pending — pointing to an EIP-1559 compatibility issue at the node level.

**3. EIP-1559 Compatibility & Txpool Analysis** — *May 9, 2026*
> Root cause investigation into persistent MetaMask transaction failures. Inspection via `eth.getTransaction()` confirmed that MetaMask submits Type-2 (EIP-1559) transactions with `gasPrice: 0`, which DAC Testnet validators do not reliably include. Repeated `eth_feeHistory` unmarshal errors in node logs confirmed incomplete EIP-1559 implementation. Network-wide txpool congestion (4,600–5,600 pending) was identified as a secondary contributing factor.

**4. Frontend–Blockchain State Desynchronization After Successful NFT Mint** — *May 10, 2026*
> Investigation into a community-reported issue where the DAC Inception dashboard continued displaying badges as unminted despite successful on-chain execution. On-chain verification via the DAC blockchain explorer confirmed NFT ownership, while the frontend UI retained stale pre-mint state. Findings point to delayed or incomplete synchronization between the backend indexer and the dashboard rendering system — a discrepancy between blockchain truth and application-layer state.

**5. Official Enode Evolution Analysis — Infrastructure Rotation & Network Maturation** — *May 11, 2026*
> Infrastructure analysis documenting the evolution of the official DAC Testnet enode registry since before the Inception campaign began and continuing through the campaign. The enode list followed the pattern 2 → 5 → 9 → 10 → 8 (current), reflecting a deliberate infrastructure lifecycle of bootstrap, expansion, and consolidation. Active peer topology data captured via `admin.peers` revealed official node identities (DAC Testnet Authority 1/2/3, DAC Testnet RPC 03), a previously undocumented internal node (84.46.253.182), and confirmed that removed nodes may continue peering beyond their removal from the published list. A real-time enode count change from 6 to 8 — observed precisely while this report was being prepared — directly validated the dynamic nature of the registry.

**6. DAC SENDER — Testnet Transaction Interface** — *May 22, 2026*
> Application development report documenting the design, deployment, and operational validation of **DAC•SENDER v1.4.3**, a static no-build, no-backend client-side web interface built to support DAC Quantum Chain Testnet infrastructure testing. The tool generates diverse, measurable EVM activity across native transfers, proxy transfers, multi-send batch transfers, contract deployment, NFT deployment, registry registration, and NFT minting. The report also documents technical findings observed during development, including the 2,824 Gwei gas price anomaly, the DACSendProxy protocol fee cap bug and fix, EVM London compatibility constraints caused by the absence of the PUSH0 opcode, recurring public RPC 502/504 failures, and the implementation of an on-chain NFT registry architecture for the NFT Launchpad. This report marks a transition from pure infrastructure diagnostics into community-built on-chain tooling for reproducible testnet activity generation and application-layer validation.

**7. Wallet Intelligence Layer — Wallet Intelligence, Dynamic Wallet Status SBT, and DAC Sender Launchpad Integration** — *May 28, 2026*
> Application development report documenting the completion of DAC Wallet Intelligence Layer across two development tracks: v1 (up to v1.5.4) and v2 (up to v2.0.2). v1 provides a read-only, no-connect wallet checker that converts public DAC Testnet explorer and RPC data into a structured wallet profile — covering native funds, asset holdings, activity analytics, NFT portfolio, reputation scoring, Sybil heuristics, and DAC Inception Rank signals. v2 extends the foundation into a dynamic wallet-bound SBT system: each wallet can mint one evolving ERC-5192 locked badge reflecting its verified on-chain profile, dynamically rendered as an SVG tied to live contract reads. The Wallet Status SBT is integrated into the DAC Sender NFT Launchpad registry, making it discoverable and mintable through the existing community launchpad. Technical findings during v2 finalization include inline SVG rendering as the resolution for dynamic artwork compatibility and UI-layer filtering as the approach for managing deprecated development registry entries.

---

*Prepared by: JERUZZALEM — DAC Infra Tester*
