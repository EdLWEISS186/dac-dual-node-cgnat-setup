# Testnet (Inception) — Technical Reports

The following reports document technical findings from field testing conducted during active contribution to the **DAC Testnet (Inception)** campaign. Each report covers a distinct infrastructure or compatibility issue identified through independent observation, diagnostics, and validation testing.

---

## Table of Contents

| # | Report | Date |
|---|--------|------|
| 1 | [Critical RPC Availability Issue & Network Access Bottleneck](./1.%20Critical%20RPC%20Availability%20Issue%20%26%20Network%20Access%20Bottleneck.pdf) | May 5, 2026 |
| 2 | [Testnet Infrastructure Validation Report](./2.%20Testnet%20Infrastructure%20Validation%20Report.pdf) | May 7, 2026 |
| 3 | [EIP-1559 Compatibility & Txpool Analysis](./3.%20EIP-1559%20Compatibility%20%26%20Txpool%20Analysis.pdf) | May 9, 2026 |

---

## Report Summaries

**1. Critical RPC Availability Issue & Network Access Bottleneck** — *May 5, 2026*
> Initiated after widespread community reports of wallets stuck on "Still connecting to DAC Chain Testnet…". Direct JSON-RPC probing of all official enodes revealed that 6 of 7 nodes were unresponsive, and the public RPC endpoint (rpctest.dachain.tech) was returning 504 Gateway Time-out. The P2P/consensus layer remained operational — the bottleneck was isolated to the RPC layer.

**2. Testnet Infrastructure Validation Report** — *May 7, 2026*
> Follow-up validation using a dual-node single-machine setup (Windows + WSL Ubuntu) to test RPC stability, wallet interoperability, and transaction propagation. Localhost RPC endpoints significantly outperformed the public endpoint. OKX Wallet and Rabby Wallet transacted successfully, while MetaMask transactions remained pending — pointing to an EIP-1559 compatibility issue at the node level.

**3. EIP-1559 Compatibility & Txpool Analysis** — *May 9, 2026*
> Root cause investigation into persistent MetaMask transaction failures. Inspection via `eth.getTransaction()` confirmed that MetaMask submits Type-2 (EIP-1559) transactions with `gasPrice: 0`, which DAC Testnet validators do not reliably include. Repeated `eth_feeHistory` unmarshal errors in node logs confirmed incomplete EIP-1559 implementation. Network-wide txpool congestion (4,600–5,600 pending) was identified as a secondary contributing factor.

---

*Prepared by: JERUZZALEM — DAC Infra Tester*
