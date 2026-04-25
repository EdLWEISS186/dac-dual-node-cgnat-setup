@echo off
cd /d "YOUR_WINDOWS_NODE_PATH"

:loop
echo Starting DAC Node...

dacnode.exe --testnet --syncmode fast --miner.etherbase YOUR_WALLET_ADDRESS --datadir "YOUR_WINDOWS_NODE_PATH\chaindata" --maxpeers 12

echo.
echo Node stopped or crashed. Restarting in 5 seconds...
timeout /t 5 >nul

goto loop
