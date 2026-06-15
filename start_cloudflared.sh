#!/usr/bin/env bash
# ============================================================
# Start Django + Cloudflare Tunnel (free, no signup needed)
# ============================================================
set -e

# Allow override but default to /home/theia (the actual HOME for theia user)
TARGET_HOME="${HOME:-/home/theia}"
cd "$TARGET_HOME/xrwvm-fullstack_developer_capstone" 2>/dev/null || {
    cd /home/project/xrwvm-fullstack_developer_capstone
}

# Sanity check
if ! python3 -c "import django" 2>/dev/null; then
    echo "ERROR: Django not installed. Run: bash lab_setup.sh"
    exit 1
fi

# Kill any prior Django/ngrok, but NOT cloudflared yet (use a precise match
# against the binary, not the script name, so this script itself isn't killed).
echo "=== Cleaning up old processes on port 8000 ==="
fuser -k 8000/tcp 2>/dev/null || true
pkill -f "manage.py runserver" 2>/dev/null || true
pkill -x ngrok 2>/dev/null || true
sleep 2

REPO_DIR="$(pwd)"
LOG_DIR="$TARGET_HOME"

# Start Django in background
echo "=== Starting Django on port 8000 ==="
cd "$REPO_DIR/server"
nohup python3 manage.py runserver 0.0.0.0:8000 > "$LOG_DIR/django.log" 2>&1 &
DJANGO_PID=$!
disown $DJANGO_PID 2>/dev/null || true
echo "Django PID: $DJANGO_PID"
sleep 4

if ! kill -0 $DJANGO_PID 2>/dev/null; then
    echo "ERROR: Django failed to start. Last log lines:"
    tail -20 "$LOG_DIR/django.log"
    exit 1
fi
if curl -sf http://localhost:8000/ -o /dev/null; then
    echo "Django is running at http://localhost:8000"
else
    echo "WARNING: Django started but not responding. Last log lines:"
    tail -20 "$LOG_DIR/django.log"
fi

cd "$REPO_DIR"

# Start cloudflared quick tunnel (no auth needed)
echo "=== Starting Cloudflare Tunnel ==="
# Detach completely so the script can exit and leave cloudflared running.
setsid nohup ./cloudflared tunnel --no-autoupdate --url http://localhost:8000 </dev/null >"$LOG_DIR/cloudflared.log" 2>&1 &
CF_PID=$!
disown $CF_PID 2>/dev/null || true
echo "cloudflared PID: $CF_PID"
sleep 10

# Extract public URL from log
PUBLIC_URL=$(grep -oE "https://[a-z0-9-]+\.trycloudflare\.com" "$LOG_DIR/cloudflared.log" | head -1)
if [ -z "$PUBLIC_URL" ]; then
    echo "ERROR: Could not get Cloudflare URL. Last log lines:"
    tail -30 "$LOG_DIR/cloudflared.log"
    exit 1
fi

echo ""
echo "============================================================"
echo "DEPLOYED URL: $PUBLIC_URL"
echo "============================================================"
echo ""
echo "Save this URL in deploymentURL.txt:"
echo "  $PUBLIC_URL"
echo ""

# Save URL
echo "$PUBLIC_URL" > "$LOG_DIR/deployed_url.txt"
echo "$PUBLIC_URL" > "$REPO_DIR/deploymentURL.txt"

# Test the URL works
echo "Testing the URL..."
if curl -sf "$PUBLIC_URL/" -o /dev/null --max-time 10; then
    echo "URL is working."
else
    echo "URL returned non-2xx (might still be fine for screenshots)."
fi
echo ""
echo "Both Django and cloudflared are detached and still running."
echo "You can close this terminal or run: pkill -f manage.py && pkill -x cloudflared"
