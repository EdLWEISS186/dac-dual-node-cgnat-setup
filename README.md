# DAC Dual Node Setup (Windows + WSL)

A dual-node configuration for the DAC testnet running on **Windows host** and **WSL (Linux)**, with a CGNAT workaround using static peering and internal LAN routing.

---

## Table of Contents

- [Overview](#overview)
- [Goals](#goals)
- [Current Status](#current-status)
- [Network Topology](#network-topology)
- [Node Configuration](#node-configuration)
- [Startup Commands](#startup-commands)
- [Verification](#verification)
- [Notes](#notes)

---

## Overview

This setup enables stable DAC testnet participation from a CGNAT-constrained environment by running two nodes simultaneously:

| Node         | Platform        | Port  | Address           |
|--------------|-----------------|-------|-------------------|
| Windows Node | Windows Host    | 28657 | 192.168.100.7     |
| WSL Node     | WSL (Linux)     | 30304 | via Windows host  |

---

## Goals

- Stable node operation under CGNAT (no inbound connectivity)
- Inter-node connectivity between Windows and WSL
- Connection to official DAC testnet authority nodes
- Redundant peer paths for consistent uptime

---

## Current Status `v0.1`

| Item                        | Status       |
|-----------------------------|--------------|
| Node operation              | ✅ Stable     |
| Static peering              | ✅ Configured |
| DAC authority node sync     | ✅ Connected  |
| Chain sync                  | ✅ Completed  |

---

## Network Topology

```
                  [ DAC Official Nodes ]
                            ↑
                            |
             ┌──────────────┴──────────────┐
             ↑                             ↑
     [ Windows Node ]       ⇄        [ WSL Node ]
   192.168.100.7:28657            192.168.100.7:30304
```

### Connection Summary

| From          | To                  | Type           |
|---------------|---------------------|----------------|
| Windows Node  | DAC Official Nodes  | Outbound       |
| WSL Node      | DAC Official Nodes  | Outbound       |
| Windows Node  | WSL Node            | Internal LAN   |
| WSL Node      | Windows Node        | Internal LAN   |

---

## Node Configuration

| Component      | Address               | Role                        |
|----------------|-----------------------|-----------------------------|
| Windows Node   | `192.168.100.7:28657` | Primary outbound node       |
| WSL Node       | `192.168.100.7:30304` | Secondary, routed via host  |
| Official Nodes | Public enodes         | Static peers (authority)    |

---

## Startup Commands

### Windows Node

```powershell
.\dacnode.exe `
  --testnet `
  --syncmode fast `
  --miner.etherbase YOUR_ADDRESS `
  --datadir "YOUR_DATADIR_PATH" `
  --port 28657 `
  --nat extip:192.168.100.7
```

### WSL Node

```bash
cd "/mnt/d/YOUR_PATH" && \
./dacnode \
  --testnet \
  --syncmode fast \
  --miner.etherbase YOUR_ADDRESS \
  --datadir ~/dac-chaindata-wsl \
  --port 30304 \
  --nat extip:192.168.100.7
```

> **Note:** Replace `YOUR_ADDRESS`, `YOUR_DATADIR_PATH`, and `/mnt/d/YOUR_PATH` with your actual values.

---

## Verification

Run the following inside the node console to verify connectivity:

```javascript
eth.syncing     // Expected: false
net.peerCount   // Expected: >= 1
admin.peers     // Expected: list of connected enodes
```

| Check         | Expected Value |
|---------------|----------------|
| `eth.syncing` | `false`        |
| `net.peerCount` | `≥ 1`        |
| `admin.peers` | Non-empty list |

---

## Notes

- CGNAT is handled via internal IP peering — no inbound port forwarding required.
- Static nodes are configured to ensure stable, persistent peer connections.
- Do **not** use `127.0.0.1` for inter-node peering between Windows and WSL.
- WSL must advertise the Windows host IP using `--nat extip:192.168.100.7`.
