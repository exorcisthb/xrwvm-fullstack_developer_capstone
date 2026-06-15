#!/usr/bin/env bash
# ============================================================
# Capstone Project - One-shot setup for IBM SkillsBuild Lab
# Run this ONCE in the lab terminal.
# ============================================================
set -e

cd ~

echo "=== [1/6] Cloning repository ==="
if [ ! -d "xrwvm-fullstack_developer_capstone" ]; then
    git clone https://github.com/exorcisthb/xrwvm-fullstack_developer_capstone.git
fi
cd xrwvm-fullstack_developer_capstone

echo "=== [2/6] Pulling latest changes ==="
git pull origin main

echo "=== [3/6] Installing Python dependencies ==="
python3 -m pip install --quiet --user --upgrade pip
python3 -m pip install --quiet --user -r server/requirements.txt
python3 -c "import django; print('Django version:', django.__version__)" || { echo "Django install FAILED"; exit 1; }

echo "=== [4/6] Running migrations and seeding data ==="
cd server
python3 manage.py migrate --noinput
python3 manage.py seed_data
cd ..

echo "=== [5/6] Downloading cloudflared (free, no signup) ==="
if [ ! -x "./cloudflared" ]; then
    rm -f cloudflared
    # Use a specific known release to avoid 302/HTML redirects
    URL="https://github.com/cloudflare/cloudflared/releases/download/2024.12.2/cloudflared-linux-amd64"
    echo "Downloading from: $URL"
    curl -fsSL -o cloudflared "$URL"
    chmod +x cloudflared
    ls -la cloudflared
    file cloudflared || true
    ./cloudflared --version || { echo "cloudflared not executable or corrupt"; exit 1; }
fi

echo "=== [6/6] Installing Playwright (for screenshots) ==="
python3 -m pip install --quiet --user playwright
python3 -m playwright install --with-deps chromium 2>/dev/null || python3 -m playwright install chromium

echo "=== Setup complete ==="
echo ""
echo "To run the app + capture deployment URL, use:"
echo "  bash start_cloudflared.sh"
echo "To capture submission screenshots (Tasks 25-28), use:"
echo "  python3 take_screenshots.py"
echo ""
