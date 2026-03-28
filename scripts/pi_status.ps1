param(
    [string]$Host = "pi@192.168.137.142",
    [string]$RemotePath = "/home/pi/plant"
)

$remoteScript = @"
set -euo pipefail
printf 'timestamp='; date --iso-8601=seconds
printf 'hostname='; hostname
printf 'user='; whoami
printf 'kernel='; uname -srmo
printf 'python='; python3 --version
printf 'ip='; hostname -I
printf 'uptime='; uptime -p
printf 'load='; uptime | awk -F'load average: ' '{print $2}'
printf 'memory='; free -h | awk 'NR==2 {print $3 "/" $2 " used"}'
printf 'disk='; df -h / | awk 'NR==2 {print $3 "/" $2 " used (" $5 ")"}'
printf 'venv='; if [ -d '$RemotePath/.venv' ]; then echo present; else echo missing; fi
printf 'repo='; if [ -d '$RemotePath/.git' ]; then echo present; else echo missing; fi
printf 'repo_head='; if [ -d '$RemotePath/.git' ]; then git -C '$RemotePath' rev-parse HEAD; else echo missing; fi
printf 'i2c_nodes='; ls /dev/i2c* 2>/dev/null | tr '\n' ' ' || true; echo
printf 'spi_nodes='; ls /dev/spidev* 2>/dev/null | tr '\n' ' ' || true; echo
printf 'gpiochip='; ls /dev/gpiochip* 2>/dev/null | tr '\n' ' ' || true; echo
printf 'logs='; ls '$RemotePath/logs' 2>/dev/null | tr '\n' ' ' || true; echo
"@

$remoteScript | ssh $Host "bash -s"
