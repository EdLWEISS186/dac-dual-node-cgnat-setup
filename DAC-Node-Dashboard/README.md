# DAC Node Dashboard

A desktop application to run, monitor, and log both DAC nodes — Windows and WSL — from a single interface.

---

## Requirements

- **Windows 10/11** with WSL enabled
- **Node.js** v18 or higher — [https://nodejs.org](https://nodejs.org)
- **npm** v9 or higher (included with Node.js)
- **DAC Node binary** — download from the official source:
  👉 [https://download.dachain.tech/](https://download.dachain.tech/)

---

## Installation

```bash
# 1. Clone the parent repository
git clone https://github.com/EdLWEISS186/dac-dual-node-cgnat-setup.git

# 2. Navigate to the app folder
cd dac-dual-node-cgnat-setup/DAC-Node-Dashboard

# 3. Install dependencies
npm install

# 4. Start the application
npm start
```

---

## Configuration

Before running, edit the script files to match your local setup. All scripts are located in the `scripts/` folder.

---

### ⚙️ Windows Node — `scripts/Windows/start-node.bat`

Open with any text editor and edit the variables at the top of the file:

```bat
set NODE_PATH=D:\YOUR_NODE_PATH\Windows
set ETHERBASE=0xYourWalletAddressHere
set DATADIR=D:\YOUR_NODE_PATH\Windows\chaindata
set PORT=30303
set MAXPEERS=12
set NAT_IP=YOUR_LAN_IP
```

| Variable | Description | How to Obtain |
|----------|-------------|---------------|
| `NODE_PATH` | Path to your Windows dacnode folder | Where `dacnode.exe` is located |
| `ETHERBASE` | Your DAC wallet address | From your DAC wallet |
| `DATADIR` | Path to chaindata folder | Usually `NODE_PATH\chaindata` |
| `PORT` | P2P port for Windows node | Default `30303` |
| `MAXPEERS` | Max peer connections | Recommended: `12` |
| `NAT_IP` | Your LAN IP address | Run `ipconfig` → **IPv4 Address** |

---

### ⚙️ WSL Node — `scripts/WSL_Linux/start-node.bat`

Open with any text editor and edit the values inside the script:

```
/mnt/d/YOUR_NODE_PATH/Linux    ← WSL path to your Linux dacnode folder
0xYourWalletAddressHere         ← Your DAC wallet address
YOUR_NODE_IDENTITY              ← Display name shown in peer list
YOUR_LAN_IP                     ← Your LAN IP (same as Windows)
```

> **WSL Path format:** Windows `D:\DAC\Linux` → WSL `/mnt/d/DAC/Linux`

---

### ⚙️ Monitor & Logging Scripts

Update the node paths in these files to match your setup:

| File | Path to update |
|------|---------------|
| `scripts/Windows/Monitor.bat` | `cd /d "YOUR_WINDOWS_NODE_PATH"` |
| `scripts/WSL_Linux/Monitor.bat` | WSL path inside `wsl bash -c` |
| `scripts/Windows/logging.ps1` | `$NodeDir` variable |
| `scripts/WSL_Linux/logging.sh` | `DACDIR` variable |

---

### 🌐 Changing Networks

`NAT_IP` must match your current LAN IP. Update it every time you switch networks.

Run `ipconfig` in PowerShell and look for **IPv4 Address** under your active network adapter.

Files to edit when switching networks:
- `scripts/Windows/start-node.bat` → `set NAT_IP=YOUR_NEW_IP`
- `scripts/WSL_Linux/start-node.bat` → `--nat extip:YOUR_NEW_IP`

---

## Features

| Feature | Description |
|---------|-------------|
| Dual node control | Start and stop both Windows and WSL nodes simultaneously |
| Live node logs | Real-time log streaming with ANSI color support |
| Monitoring | Live sync status, block number, and peer count — refreshes every 5 seconds |
| Logging | Continuous logging to file with 5-second intervals |
| Zoom per panel | `Ctrl+Scroll` or `+`/`−` buttons per panel |
| Auto-restart | Nodes automatically restart on crash |

---

## Log Files

Logs are saved inside the app folder:

```
DAC-Node-Dashboard/
└── logs/
    ├── monitor_windows.log
    └── monitor_wsl.log
```
