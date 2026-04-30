@echo off
echo Starting WSL DAC Logger...

wsl bash -c "cp '/mnt/d/dac-node-dashboard/scripts/WSL_Linux/logging.sh' /tmp/daclogging.sh && chmod +x /tmp/daclogging.sh && bash /tmp/daclogging.sh"
