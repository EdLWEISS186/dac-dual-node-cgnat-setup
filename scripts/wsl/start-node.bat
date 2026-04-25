@echo off
echo Starting WSL DAC Node (auto-restart mode)...

wsl bash -c "while true; do cd \"YOUR_WSL_NODE_PATH\" && ./dacnode --testnet --syncmode fast --miner.etherbase YOUR_WALLET_ADDRESS --datadir ~/dac-chaindata-wsl --identity \"YOUR_NODE_IDENTITY\" --port 30304 --maxpeers 8; echo 'Node crashed. Restarting in 5s...'; sleep 5; done"

pause
