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
# /usr/local/lib is not writable. Use --user to install into ~/.local/.
# Older pip on this lab doesn't support --break-system-packages, so --user is the safe path.
python3 -m pip install --quiet --user --upgrade pip
python3 -m pip install --quiet --user -r server/requirements.txt
# Sanity check
python3 -c "import django; print('Django version:', django.__version__)" || { echo "Django install FAILED"; exit 1; }

echo "=== [4/6] Running migrations and seeding data ==="
cd server
python3 manage.py migrate --noinput
python3 manage.py seed_data
cd ..

echo "=== [5/6] Downloading ngrok binary ==="
if [ ! -f "ngrok" ]; then
    curl -sL https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -o ngrok.tgz
    tar -xzf ngrok.tgz
    rm ngrok.tgz
    chmod +x ngrok
fi

echo "=== [6/6] Setup complete ==="
echo ""
echo "To run the app, use:"
echo "  bash start_ngrok.sh"
echo ""
