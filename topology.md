# 🔗 DAC Dual-Node Topology (CGNAT Setup)

## 🎯 Overview
This setup uses a **dual-node architecture (Windows + WSL)** under **CGNAT conditions (no inbound connectivity)** with the following approach:
- Outbound-only connectivity
- Static peers for stability
- Internal peering for redundancy

---

## 🧭 Network Topology

         [ DAC Official Nodes ]
                  ↑
                  │
    ┌─────────────┴─────────────┐
    │                           │
    [ Windows Node ] ⇄ [ WSL Node ]

---

## 🔌 Connection Rules

### Windows Node
- Connects to:
  - ✅ Official nodes
  - ✅ WSL node (internal LAN)

### WSL Node
- Connects to:
  - ✅ Official nodes
  - ✅ Windows node (via host IP)

---

## ⚙️ Address Mapping

| Node     | Enode Address Source | External IP Used        |
|----------|---------------------|--------------------------|
| Windows  | Native              | `192.168.100.7:28657`    |
| WSL      | NAT via Windows     | `192.168.100.7:30304`    |

---

## ⚠️ Important Notes

- Do NOT use `127.0.0.1` for inter-node peering
- WSL must expose its external IP using:
  ```bash
  --nat extip:192.168.100.7
  
Static peers are required to:
Maintain stable connections
Reduce reliance on discovery

🔁 Connectivity Model
Windows ⇄ WSL → internal redundancy
Windows → Official → primary sync path
WSL → Official → secondary sync path

🚀 Design Goals
✔ Stable under CGNAT conditions
✔ No dependency on inbound connections
✔ Redundant peer paths
✔ Consistent long-running node behavior

🧠 Insight

This is not just a dual-node setup, but:

A minimal P2P cluster simulation under constrained network conditions (CGNAT)

Suitable for:

Infrastructure testing
Peer stability observation
Network behavior analysis
