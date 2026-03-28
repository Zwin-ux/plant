param(
    [string]$Host = "pi@192.168.137.142",
    [string]$RemotePath = "/home/pi/plant"
)

$repoRoot = Split-Path -Parent $PSScriptRoot
$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("plant-sync-" + [guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $tempRoot "plant-sync.tar.gz"
$remoteArchive = "/tmp/plant-sync.tar.gz"
$destination = "${Host}:$remoteArchive"

New-Item -ItemType Directory -Path $tempRoot | Out-Null

try {
    tar -czf $archivePath `
        --exclude=".git" `
        --exclude=".venv" `
        --exclude="__pycache__" `
        --exclude="logs" `
        --exclude=".vscode" `
        --exclude=".idea" `
        --exclude="*.pyc" `
        --exclude="*.log" `
        -C $repoRoot .

    scp $archivePath $destination

    $remoteScript = @"
set -euo pipefail
mkdir -p '$RemotePath'
find '$RemotePath' -mindepth 1 -maxdepth 1 \
  ! -name '.git' \
  ! -name '.venv' \
  ! -name 'logs' \
  ! -name '.env' \
  -exec rm -rf {} +
tar -xzf '$remoteArchive' -C '$RemotePath'
rm -f '$remoteArchive'
"@

    $remoteScript | ssh $Host "bash -s"
}
finally {
    if (Test-Path $tempRoot) {
        Remove-Item -Recurse -Force $tempRoot
    }
}
