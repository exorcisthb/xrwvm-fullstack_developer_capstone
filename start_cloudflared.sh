#!/usr/bin/env bash
# ============================================================
# Start Django + Cloudflare Tunnel (free, no signup needed)
# ============================================================
set -e

cd ~/xrwvm-fullstack_developer_capstone

# Sanity check
if ! python3 -c "import django" 2>/dev/null; then
    echo "ERROR: Django not installed. Run: bash lab_setup.sh"
    exit 1
fi

# Start Django in background
echo "=== Starting Django on port 8000 ==="
cd server
nohup python3 manage.py runserver 0.0.0.0:8000 > ~/django.log 2>&1 &
DJANGO_PID=$!
echo "Django PID: $DJANGO_PID"
sleep 4

if ! kill -0 $DJANGO_PID 2>/dev/null; then
    echo "ERROR: Django failed to start. Last log lines:"
    tail -20 ~/django.log
    exit 1
fi
if curl -sf http://localhost:8000/ -o /dev/null; then
    echo "Django is running at http://localhost:8000"
else
    echo "WARNING: Django started but not responding. Last log lines:"
    tail -20 ~/django.log
fi

cd ..

# Start cloudflared quick tunnel (no auth needed)
echo "=== Starting Cloudflare Tunnel ==="
# --url flag creates a temporary public URL; no signup required
nohup ./cloudflared tunnel --no-autoupdate --url http://localhost:8000 > ~/cloudflared.log 2>&1 &
CF_PID=$!
echo "cloudflared PID: $CF_PID"
sleep 8

# Extract public URL from log
PUBLIC_URL=$(grep -oE "https://[a-z0-9-]+\.trycloudflare\.com" ~/cloudflared.log | head -1)
if [ -z "$PUBLIC_URL" ]; then
    echo "ERROR: Could not get Cloudflare URL. Last log lines:"
    tail -30 ~/cloudflared.log
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
echo "Press Ctrl+C to stop Django and cloudflared."
echo ""

# Save URL
echo "$PUBLIC_URL" > ~/deployed_url.txt

# Test the URL works
echo "Testing the URL..."
if curl -sf "$PUBLIC_URL/" -o /dev/null --max-time 10; then
    echo "URL is working."
else
    echo "URL returned non-2xx (might still be fine for screenshots)."
fi
echo ""

wait
