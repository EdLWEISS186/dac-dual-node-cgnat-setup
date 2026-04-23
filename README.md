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
Windows Node (192.168.100.7:28657)
        ↕
WSL Node (30304)
        ↕
DAC Official Nodes

## Commands

### Windows
