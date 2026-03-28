param(
    [string]$Host = "pi@192.168.137.142",
    [string]$RemotePath = "/home/pi/plant",
    [int]$Ticks = 10,
    [string]$LogFile = "",
    [switch]$SkipPull
)

$pullStep = ""
if (-not $SkipPull) {
    $pullStep = "git pull --ff-only origin main"
}

$logArgument = ""
if ($LogFile) {
    $logArgument = "--log-file '$LogFile'"
}

$remoteScript = @"
set -euo pipefail
cd '$RemotePath'

if [ ! -d .venv ]; then
  echo '.venv is missing. Run bash scripts/bootstrap_pi.sh first.'
  exit 1
fi

$pullStep
source .venv/bin/activate
python main.py --ticks $Ticks $logArgument
"@

$remoteScript | ssh $Host "bash -s"
