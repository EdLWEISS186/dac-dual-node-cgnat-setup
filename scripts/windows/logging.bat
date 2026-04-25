@echo off
cd /d "YOUR_WINDOWS_NODE_PATH"

set lastPeers=

:loop
set "sync="
set "block="
set "peers="

for /f "delims=" %%i in ('dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.syncing"') do set sync=%%i
for /f "delims=" %%i in ('dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.blockNumber"') do set block=%%i
for /f "delims=" %%i in ('dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "net.peerCount"') do set peers=%%i

REM default color white
set color=07

REM compare with previous peer count if available
if defined lastPeers (
    if %peers% GTR %lastPeers% set color=0A
    if %peers% LSS %lastPeers% set color=0C
)

REM apply color
color %color%

echo TIME: %time% ^| syncing: %sync% ^| block: %block% ^| peers: %peers%
echo TIME: %date% %time% ^| syncing: %sync% ^| block: %block% ^| peers: %peers% >> monitor.log

REM reset color to white for next loop
color 07

set lastPeers=%peers%

timeout /t 5 >nul
goto loop
