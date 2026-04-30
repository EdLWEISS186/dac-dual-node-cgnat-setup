@echo off
REM ============================================================
REM  DAC Node Dashboard - WSL Node Launcher
REM  Edit the values below before running
REM ============================================================
REM  WSL_PATH    : WSL path to your Linux dacnode folder
REM               Format: /mnt/d/YOUR_PATH/Linux
REM  ETHERBASE   : Your DAC wallet address
REM  DATADIR     : WSL chaindata directory (relative to home)
REM  IDENTITY    : Node display name shown in peer list
REM  PORT        : P2P port for WSL node (default: 30304)
REM  MAXPEERS    : Maximum peer connections
REM  NAT_IP      : Your LAN IP address (same as Windows)
REM               Change this every time you switch networks
REM ============================================================

echo Starting WSL DAC Node (auto-restart mode)...

:loop
wsl bash -c "cd '/mnt/d/YOUR_NODE_PATH/Linux' && ./dacnode --testnet --syncmode fast --miner.etherbase 0xYourWalletAddressHere --datadir ~/dac-chaindata-wsl --identity 'YOUR_NODE_IDENTITY' --port 30304 --maxpeers 8 --nat extip:YOUR_LAN_IP"

echo.
echo WSL node stopped or crashed. Restarting in 5 seconds...
ping -n 6 127.0.0.1 >nul
goto loop
