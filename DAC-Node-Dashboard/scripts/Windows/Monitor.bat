@echo off
REM Edit NODE_PATH to match your Windows dacnode folder
cd /d "D:\YOUR_NODE_PATH\Windows"
echo Starting Win DAC Monitor...

:loop
echo [CLR]
echo === %date% %time% ===
echo.
echo [Sync Status]
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.syncing" 2>nul
echo.
echo [Block]
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.blockNumber" 2>nul
echo.
echo [Peers]
dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "net.peerCount" 2>nul
echo.
ping -n 6 127.0.0.1 >nul
goto loop
