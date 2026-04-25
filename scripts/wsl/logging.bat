@echo off
echo Starting WSL Monitor (Logging)...

:loop
for /f "delims=" %%i in ('wsl bash -c "date +%%H:%%M:%%S"') do set t=%%i
for /f "delims=" %%i in ('wsl bash -c "cd YOUR_WSL_NODE_PATH && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec eth.syncing"') do set s=%%i
for /f "delims=" %%i in ('wsl bash -c "cd YOUR_WSL_NODE_PATH && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec eth.blockNumber"') do set b=%%i
for /f "delims=" %%i in ('wsl bash -c "cd YOUR_WSL_NODE_PATH && ./dacnode attach ~/dac-chaindata-wsl/gdacnode.ipc --exec net.peerCount"') do set p=%%i

echo TIME: %t% ^| syncing: %s% ^| block: %b% ^| peers: %p%
echo %date% %time% ^| syncing: %s% ^| block: %b% ^| peers: %p% >> monitor_wsl.log

timeout /t 5 >nul
goto loop
