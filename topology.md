# DAC Dual-Node Topology (CGNAT Setup)

## Overview

This document describes the network topology for running a dual DAC node setup (Windows + WSL) under **CGNAT conditions**, where inbound connectivity is unavailable. The architecture relies on outbound-only connections, static peering, and internal LAN routing for redundancy.

---

## Network Diagram

```
                 [ DAC Official Nodes ]
                           ↑
             ┌─────────────┴─────────────┐
             ↑                           ↑
     [ Windows Node ]      ⇄       [ WSL Node ]
   192.168.100.7:28657          192.168.100.7:30304
         (Primary)                  (Secondary)
```

---

## Connection Rules

### Windows Node

| Destination       | Status    | Description              |
|-------------------|-----------|--------------------------|
| DAC Official Nodes | ✅ Active | Primary sync path        |
| WSL Node          | ✅ Active | Internal LAN redundancy  |

### WSL Node

| Destination        | Status    | Description              |
|--------------------|-----------|--------------------------|
| DAC Official Nodes  | ✅ Active | Secondary sync path      |
| Windows Node        | ✅ Active | Via host IP, internal LAN |

---

## Address Mapping

| Node         | Enode Source   | Advertised Address        | Port  |
|--------------|----------------|---------------------------|-------|
| Windows Node | Native         | `192.168.100.7`           | 28657 |
| WSL Node     | NAT via Windows | `192.168.100.7`          | 30304 |

---

## Connectivity Model

```
Windows ⇄ WSL          →  Internal redundancy
Windows → Official     →  Primary sync path
WSL     → Official     →  Secondary sync path
```

---

## Configuration Requirements

### NAT Setting (Both Nodes)

WSL must explicitly advertise the Windows host IP to avoid using the WSL-internal address:

```bash
--nat extip:192.168.100.7
```

### Static Peers

Static peers are required on both nodes to:

- Maintain persistent connections without relying on discovery
- Reduce connection instability under CGNAT
- Ensure both internal and external paths remain active

> ⚠️ Do **not** use `127.0.0.1` for inter-node peering. Always use `192.168.100.7`.

---

## Design Goals

| Goal                                  | Status       |
|---------------------------------------|--------------|
| Stable operation under CGNAT          | ✅ Achieved   |
| No dependency on inbound connections  | ✅ Achieved   |
| Redundant peer paths                  | ✅ Achieved   |
| Consistent long-running node behavior | ✅ Achieved   |

---

## Architecture Insight

This setup functions as a **minimal P2P cluster simulation under constrained network conditions**. Beyond basic testnet participation, it is suitable for:

- **Infrastructure testing** — validating node behavior in restricted environments
- **Peer stability observation** — monitoring connection persistence over time
- **Network behavior analysis** — studying sync and propagation under CGNAT
