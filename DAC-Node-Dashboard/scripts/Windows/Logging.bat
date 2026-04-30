@echo off
cd /d "D:\AE - 903\APP\Miner\Airdrop\DAC\Windows"
echo Starting Win DAC Logger...

powershell -ExecutionPolicy Bypass -File "%~dp0logging.ps1"
