# DAC Dual Node Setup (Windows + WSL)

Dual node setup (Windows + WSL) for DAC testnet — operating under CGNAT with static peering, internal LAN routing, and verified stability.

---

## Table of Contents

- [Overview](#overview)
- [Network Topology](#network-topology)
- [Node Configuration](#node-configuration)
- [Startup Commands](#startup-commands)
- [CGNAT Constraints](#cgnat-constraints)
- [Why This Setup Matters](#why-this-setup-matters)
- [Observations](#observations)
- [Future Improvements](#future-improvements)

---

## Overview

This repository documents a dual-node DAC testnet setup running simultaneously on a **Windows host** and **WSL (Linux)** — both operating under a **CGNAT-constrained network** where inbound connectivity is unavailable.

The architecture is designed around a fundamental constraint: the ISP operates Carrier-Grade NAT, making traditional inbound peer discovery impossible. Every design decision in this setup — static peers, internal LAN routing, dual-node redundancy — exists as a direct response to that constraint.

| Node         | Platform     | Role          | Port  | Address           |
|--------------|--------------|---------------|-------|-------------------|
| Windows Node | Windows Host | Hub / Anchor  | 28657 | 192.168.100.7     |
| WSL Node     | WSL (Linux)  | Support Node  | 30304 | via Windows host  |

---

## Network Topology

```
                    ┌─────────────────────────┐
                    │      Official Nodes      │
                    │  DAC Testnet · Static    │
                    │      Enode Set           │
                    └────────────┬────────────┘
                                 │
                         outbound only
                       (CGNAT — no inbound)
                                 │
               ┌─────────────────┴────────────────────┐
               │                                      │
    ┌──────────▼──────────┐            ┌──────────────▼──────────┐
    │    Windows Node      │           │       WSL Node           │
    │   Hub · Anchor       │◄────────► │   Support · Secondary    │
    │   .bat scripts       │ static ·  │   shell scripts          │
    │  192.168.100.7:28657 │ persist   │  192.168.100.7:30304     │
    └──────────────────────┘           └──────────────────────────┘

    ── outbound peer       ◄──► internal peering       • junction point
```

> For detailed architectural diagrams, see [`assets/`](assets/).

---

## Node Configuration

| Component      | Address               | Role                          |
|----------------|-----------------------|-------------------------------|
| Windows Node   | `192.168.100.7:28657` | Primary anchor, hub node      |
| WSL Node       | `192.168.100.7:30304` | Secondary, routed via host    |
| Official Nodes | Public enodes         | Static peers (authority)      |

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

> Replace `YOUR_ADDRESS`, `YOUR_DATADIR_PATH`, and `/mnt/d/YOUR_PATH` with your actual values.

---

## CGNAT Constraints

This setup operates under **Carrier-Grade NAT (CGNAT)** — a network condition imposed at the ISP level where multiple subscribers share a single public IP. The consequence is that **no inbound connections are possible**, regardless of local router configuration.

### Evidence

Port forwarding was configured on the router (Huawei HG8145V5) — mapping external port `28657` to internal host `192.168.100.7` — yet inbound peer connections remain unreachable. This confirms CGNAT is active at the ISP level, upstream of the local router.

![Router Port Mapping — CGNAT Evidence](assets/WAN1.png)

### Implications

| Constraint | Impact | Workaround Applied |
|------------|--------|--------------------|
| No inbound connections | Peer discovery fails | Static peers only |
| Shared public IP | Port forwarding ineffective | Internal LAN routing |
| Dynamic peer reliance | Unstable connections | `--nat extip` + static nodes |

### Key Rules

- Do **not** use `127.0.0.1` for inter-node peering
- Both nodes must advertise the Windows host IP: `--nat extip:192.168.100.7`
- WSL routes all external traffic through the Windows host

---

## Why This Setup Matters

Most node documentation assumes a clean network environment with inbound connectivity. This setup proves that **stable, productive DAC testnet participation is achievable under CGNAT** — without a VPS, without port tunneling, and without any inbound access.

The dual-node architecture also goes beyond basic participation. By running two nodes on the same machine — one as anchor, one as support — this setup creates a **minimal P2P cluster** that demonstrates:

- Redundant sync paths under constrained conditions
- Persistent internal peering without relying on discovery
- Stable block propagation with quality-over-quantity peer selection

This is directly applicable to anyone running nodes on residential ISPs, mobile broadband, or shared infrastructure where CGNAT is common.

---

## Observations

All observations recorded on **April 24, 2026**, with both nodes running simultaneously.

---

### Both Nodes Running Simultaneously

![Both Nodes Side-by-Side](assets/Both_Log.png)

Windows and WSL nodes running in parallel, importing chain segments and processing transactions concurrently. Both terminals show consistent block numbers and hash progression — confirming synchronized operation.

---

### Windows Node — Sync & Peer Status

![Windows Node — eth.syncing + net.peerCount](assets/Windows_Status.png)

```
eth.syncing   → false
net.peerCount → 4
```

Windows node fully synced with **4 active peers** — 3 official DAC authority nodes and 1 internal WSL peer.

---

### Windows Node — Active Peers (admin.peers)

![Windows Node — admin.peers](assets/Windows_Peers.png)

Confirmed connections to:
- `157.173.127.30:28657` — DAC Testnet Authority 2
- `157.173.127.21:28657` — DAC Testnet Authority 3
- `157.173.127.31:28657` — DAC Testnet Authority 1
- `192.168.100.7`        — WSL Node (internal, static)

---

### WSL Node — Sync & Peer Status

![WSL Node — eth.syncing + net.peerCount](assets/WSL_Status.png)

```
eth.syncing   → false
net.peerCount → 2
```

WSL node fully synced with **2 active peers** — the Windows host node and 1 official DAC authority node.

---

### WSL Node — Active Peers (admin.peers)

![WSL Node — admin.peers](assets/WSL_Peers.png)

Confirmed connections to:
- `192.168.100.7:28657`  — Windows Node (internal, static)
- `157.173.127.22:28657` — DAC Testnet RPC Node (official)

---

### Internal Peering — Persistent & Static

![Internal Peering Proof](assets/Internal_Peering.jpg)

WSL ↔ Windows bidirectional connection confirmed active. Both nodes show each other in `admin.peers` with `static: true` on the WSL side — confirming the internal peer connection is persistent and does not depend on discovery.

---

### Windows Node — Live Log

![Windows Node Terminal](assets/Windows_Log.png)

Continuous block imports with consistent `mgas`, `elapsed`, and `dirty` values — indicating stable chain processing with no sync interruptions.

---

### WSL Node — Live Log

![WSL Node Terminal](assets/WSL_Log.png)

WSL node mirrors Windows block progression within seconds — confirming that internal peering is actively propagating blocks between both nodes.

---

### Summary

| Metric              | Windows Node | WSL Node    |
|---------------------|-------------|-------------|
| `eth.syncing`       | `false`     | `false`     |
| `net.peerCount`     | 4           | 2           |
| Official peers      | 3           | 1           |
| Internal peers      | 1 (WSL)     | 1 (Win)     |
| Internal peer type  | —           | `static`    |
| Sync status         | ✅ Complete | ✅ Complete  |

---

## Future Improvements

| Item | Description |
|------|-------------|
| Startup automation | `.bat` / shell scripts to launch both nodes with one command |
| Auto-restart | Service wrapper (NSSM / systemd) for node recovery on crash |
| Monitoring | Basic peer count and sync status logging over time |
| WSL peer count | Investigate increasing WSL peer connections beyond 2 |
| Mermaid topology | Upgrade ASCII diagram to rendered Mermaid diagram |
