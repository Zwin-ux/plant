#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/Zwin-ux/plant.git}"
REPO_DIR="${REPO_DIR:-/home/pi/plant}"
BRANCH="${BRANCH:-main}"

ensure_python_venv() {
  if python3 -m venv --help >/dev/null 2>&1; then
    return
  fi

  echo "python3-venv is missing. Installing it with apt..."
  sudo apt install -y python3-venv
}

if [ ! -d "$REPO_DIR/.git" ]; then
  mkdir -p "$(dirname "$REPO_DIR")"
  git clone "$REPO_URL" "$REPO_DIR"
fi

cd "$REPO_DIR"
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"

ensure_python_venv

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo "Plant Creature Alpha bootstrap complete in $REPO_DIR"
