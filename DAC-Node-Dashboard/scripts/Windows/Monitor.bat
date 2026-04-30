@echo off
cd /d "D:\AE - 903\APP\Miner\Airdrop\DAC\Windows"
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
