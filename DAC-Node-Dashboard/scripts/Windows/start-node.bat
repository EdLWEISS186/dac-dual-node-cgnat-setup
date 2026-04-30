@echo off
REM ============================================================
REM  DAC Node Dashboard - Windows Node Launcher
REM  Edit the values below before running
REM ============================================================
REM  NODE_PATH   : Full path to your Windows dacnode folder
REM  ETHERBASE   : Your DAC wallet address
REM  DATADIR     : Full path to your chaindata folder
REM  PORT        : P2P port for Windows node (default: 30303)
REM  MAXPEERS    : Maximum peer connections
REM  NAT_IP      : Your LAN IP address
REM               Run 'ipconfig' and look for IPv4 Address
REM               Change this every time you switch networks
REM ============================================================

set NODE_PATH=D:\YOUR_NODE_PATH\Windows
set ETHERBASE=0xYourWalletAddressHere
set DATADIR=D:\YOUR_NODE_PATH\Windows\chaindata
set PORT=30303
set MAXPEERS=12
set NAT_IP=YOUR_LAN_IP

cd /d "%NODE_PATH%"

:loop
echo Starting DAC Node...

dacnode.exe ^
--testnet ^
--syncmode fast ^
--miner.etherbase %ETHERBASE% ^
--datadir "%DATADIR%" ^
--port %PORT% ^
--maxpeers %MAXPEERS% ^
--nat extip:%NAT_IP%

echo.
echo Node stopped or crashed. Restarting in 5 seconds...
ping -n 6 127.0.0.1 >nul
goto loop
