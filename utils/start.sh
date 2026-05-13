#!/bin/bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CSS_INPUT="$ROOT_DIR/static/css/input.css"
CSS_OUTPUT="$ROOT_DIR/static/css/output.css"

cd "$ROOT_DIR"

echo "[1/3] Starting Docker containers..."
docker compose up -d --build
echo "      OK — app at http://localhost:8000"

echo "[2/3] Checking Node/npm..."
if ! command -v npm &>/dev/null; then
  echo "      WARNING: npm not found, skipping CSS build."
  exit 0
fi
echo "      OK — $(node --version) / npm $(npm --version)"

echo "[3/3] Checking CSS..."
if [ ! -f "$CSS_OUTPUT" ] || [ "$CSS_INPUT" -nt "$CSS_OUTPUT" ]; then
  echo "      output.css missing or outdated, building..."
  if [ ! -d "$ROOT_DIR/node_modules" ]; then
    echo "      node_modules not found, running npm install..."
    npm install
  fi
  npm run build:css
  echo "      CSS built successfully."
else
  echo "      output.css is up to date, nothing to do."
fi

echo ""
echo "Done! Visit http://localhost:8000"
