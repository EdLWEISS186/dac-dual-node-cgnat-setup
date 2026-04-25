@echo off
cd /d "YOUR_WINDOWS_NODE_PATH"

:loop
cls
echo === %date% %time% ===

echo Sync Status:
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.syncing"

echo Block:
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.blockNumber"

echo Peers:
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "net.peerCount"

timeout /t 5 >nul
goto loop
