# Sender-Web

A lightweight, client-side web interface for dispatching native DACC token transactions on the DAC Quantum Chain Testnet. Designed for rapid airdrop execution, node operator tooling, and community-facing testnet interaction without requiring a backend server or centralized infrastructure.

## Overview

This tool provides a browser-based transaction interface that communicates directly with an EVM-compatible wallet (Rabby, MetaMask, or equivalent). All transaction signing occurs client-side — no private keys are transmitted or stored. The application is stateless and requires no build step, dependency installation, or server runtime.

**Live deployment:**
> `https://EdLWEISS186.github.io/dac-dual-node-cgnat-setup/Sender-Web/`

---

## Network Configuration

| Parameter | Value |
|---|---|
| Network Name | DAC Testnet |
| Chain ID | `21894` |
| RPC Endpoint | `https://rpctest.dachain.tech` |
| Currency Symbol | `DACC` |
| Block Explorer | `https://exptest.dachain.tech` |

The wallet is auto-prompted to switch to or register the DAC Testnet network upon connection. Users operating a local node may override the RPC endpoint directly within their wallet settings — the application remains chain-agnostic as long as the Chain ID matches.

---

## Features

- **EVM Wallet Integration** — Connects to any `window.ethereum`-compatible wallet via the standard provider API
- **Live Balance Fetching** — Retrieves and displays the connected account's native DACC balance on load
- **Quick Amount Presets** — One-click shortcuts for common transaction amounts (`0.001`, `0.01`, `0.1`, `MAX`)
- **Random Address Dispatch** — Selects a pseudorandom recipient from a predefined target address pool, suitable for bulk airdrop operations
- **Transaction Log Panel** — Displays real-time transaction status (`PENDING` → `SUCCESS` / `FAILED`) with direct block explorer links per hash
- **Auto Network Switch** — Issues `wallet_switchEthereumChain` / `wallet_addEthereumChain` requests automatically on connect

---

## Usage

### Public Access (No Setup Required)

Navigate to the live URL above using any Chromium-based browser with an EVM wallet extension installed. The interface will prompt for wallet connection on load.

### Local Usage

Serve the file over HTTP — do not open directly via `file://` protocol, as browser wallet extensions do not inject `window.ethereum` into file-scheme pages.

```bash
# Node.js
npx serve .

# Python
python -m http.server 8080
```

Then open `http://localhost:3000/Sender-Web/` or `http://localhost:8080/Sender-Web/`.

---

## Address Pool Configuration

The target address list is defined as a static array within `index.html`:

```js
const RANDOM_ADDRESSES = [
  "0xFb93EED6c4BC0686513c2d585fD54d7e517Da32c",
  "0x10100e4f09066DbF80296e76a5749fae3BcB71EF",
  // ...
];
```

To modify the pool, edit the array directly and redeploy. The Random dispatch function selects addresses using `Math.random()` — distribution is uniform across the full array.

---

## Technical Notes

- **No build toolchain** — single `index.html` file; zero npm dependencies at runtime
- **Transaction signing** — delegated entirely to the connected wallet; the application constructs and submits unsigned transaction objects via `ethers.js v6` (`BrowserProvider` + `Signer`)
- **Gas estimation** — handled by the wallet and node; no manual gas configuration is exposed to the user
- **Decimal precision** — native DACC uses 18 decimal places (EVM standard); all amount parsing uses `ethers.parseEther()` to prevent floating-point truncation
- **Hosted via GitHub Pages** — static file serving with HTTPS enforced; no server-side logic

---

## Repository Context

This tool is part of a broader operational setup documented in the parent repository, which covers dual-node single-machine deployment under CGNAT, automated node management, and Prometheus + Grafana monitoring for the DAC Quantum Chain Testnet.

---

*Authored by **JERUZZALEM** — DAC Infra Tester*
