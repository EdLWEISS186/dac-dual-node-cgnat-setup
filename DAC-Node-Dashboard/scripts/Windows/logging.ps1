$AppDir = "D:\dac-node-dashboard"
$LogDir = "$AppDir\logs"
$NodeDir = "D:\AE - 903\APP\Miner\Airdrop\DAC\Windows"
if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
Set-Location $NodeDir
while ($true) {
    try {
        $s = .\dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.syncing" 2>$null | Where-Object { $_ -notmatch 'Welcome|instance|coinbase|at block|datadir|modules|To exit|^>' } | Select-Object -Last 1
        $b = .\dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "eth.blockNumber" 2>$null | Where-Object { $_ -notmatch 'Welcome|instance|coinbase|at block|datadir|modules|To exit|^>' } | Select-Object -Last 1
        $p = .\dacnode.exe attach ipc:\\.\pipe\gdacnode.ipc --exec "net.peerCount" 2>$null | Where-Object { $_ -notmatch 'Welcome|instance|coinbase|at block|datadir|modules|To exit|^>' } | Select-Object -Last 1
        $t = Get-Date -Format 'HH:mm:ss'
        $line = "LOG: $t | syncing: $s | block: $b | peers: $p"
        Write-Host $line
        Add-Content -Path "$LogDir\monitor_windows.log" -Value $line
    } catch {}
    Start-Sleep -Seconds 5
}
