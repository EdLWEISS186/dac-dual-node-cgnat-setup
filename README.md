# dac-dual-node-cgnat-setup
Dual node setup (Windows + WSL) for DAC testnet with CGNAT workaround, static peering, and stability testing

# DAC Dual Node Setup (Windows + WSL)

This repository documents my setup running dual DAC nodes on:
- Windows host
- WSL (Linux)

## Goals
- Stable node operation under CGNAT
- Inter-node connectivity (Windows ↔ WSL)
- Connection to official DAC testnet nodes

## Current Status (v0.1)
- Nodes running stable
- Static peering configured
- Connected to DAC authority nodes
- Sync completed

## Topology

## 🧭 Topology

               +----------------------+
               |  DAC Official Nodes |
               +----------+-----------+
                          ↑
                          │
    +---------------------+-------------------+
    |      Windows Node         WSL Node      |
    |     192.168.100.7   ⇄   port: 30304     |
    |      port: 28657        via Windows     |
    |                                         |
    +---------------------+-------------------+


### 🔌 Connection Summary

- Windows Node → DAC Official Nodes  
- WSL Node → DAC Official Nodes  
- Windows Node ⇄ WSL Node (internal LAN)  

### ⚙️ Network Details

| Component      | Address             | Notes               |
|----------------|---------------------|---------------------|
| Windows Node   | 192.168.100.7:28657 | Main outbound node |
| WSL Node       | 192.168.100.7:30304 | Routed via Windows |
| Official Nodes | Public enodes       | Static peers       |

## Commands

### Windows
.\dacnode.exe --testnet --syncmode fast --miner.etherbase YOUR_ADDRESS --datadir "YOUR_PATH" --port 28657 --nat extip:192.168.100.7

### WSL
cd "/mnt/d/..." && ./dacnode --testnet --syncmode fast --miner.etherbase YOUR_ADDRESS --datadir ~/dac-chaindata-wsl --port 30304

## Notes
- CGNAT handled via internal IP peering
- Static nodes used for stability
