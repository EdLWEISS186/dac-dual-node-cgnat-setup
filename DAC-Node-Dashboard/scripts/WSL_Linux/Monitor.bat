@echo off
REM Edit WSL_PATH to match your Linux dacnode folder
echo Starting WSL DAC Monitor...

:loop
echo [CLR]
echo === %date% %time% ===
wsl bash -c "cd '/mnt/d/YOUR_NODE_PATH/Linux' && echo '' && echo '[Sync Status]' && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'eth.syncing' 2>/dev/null && echo '' && echo '[Block]' && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'eth.blockNumber' 2>/dev/null && echo '' && echo '[Peers]' && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec 'net.peerCount' 2>/dev/null"
ping -n 6 127.0.0.1 >nul
goto loop
