#!/bin/bash
DACDIR="/mnt/d/AE - 903/APP/Miner/Airdrop/DAC/Linux"
IPC="$HOME/dac-chaindata-wsl/gdacnode.ipc"
LOGDIR="/mnt/d/dac-node-dashboard/logs"
LOG="$LOGDIR/monitor_wsl.log"
mkdir -p "$LOGDIR"
cd "$DACDIR"
while true; do
    T=$(date +'%H:%M:%S')
    S=$(./dacnode attach "$IPC" --exec 'eth.syncing' 2>/dev/null | grep -v 'Welcome\|instance\|coinbase\|at block\|datadir\|modules\|To exit\|^>' | tail -1)
    B=$(./dacnode attach "$IPC" --exec 'eth.blockNumber' 2>/dev/null | grep -v 'Welcome\|instance\|coinbase\|at block\|datadir\|modules\|To exit\|^>' | tail -1)
    P=$(./dacnode attach "$IPC" --exec 'net.peerCount' 2>/dev/null | grep -v 'Welcome\|instance\|coinbase\|at block\|datadir\|modules\|To exit\|^>' | tail -1)
    LINE="LOG: $T | syncing: $S | block: $B | peers: $P"
    echo "$LINE"
    echo "$LINE" >> "$LOG"
    sleep 5
done
