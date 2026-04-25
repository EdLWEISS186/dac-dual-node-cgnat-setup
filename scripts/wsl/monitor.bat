@echo off
echo Starting WSL DAC Monitor...

:loop
cls
echo === %date% %time% ===

wsl bash -c "cd YOUR_WSL_NODE_PATH; echo Sync Status:; ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'eth.syncing'; echo Block:; ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'eth.blockNumber'; echo Peers:; ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'net.peerCount'"

timeout /t 5 >nul
goto loop
