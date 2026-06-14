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
if [ ! -f "cloudflared" ]; then
    curl -sL -o cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x cloudflared
fi

echo "=== [6/6] Setup complete ==="
echo ""
echo "To run the app, use:"
echo "  bash start_cloudflared.sh"
echo ""
