#!/usr/bin/env bash
# ============================================================
# Start Django + ngrok for public URL
# ============================================================
set -e

cd ~/xrwvm-fullstack_developer_capstone

# Find user site-packages where pip installed the packages
USER_SITE=$(python3 -c "import site; print(site.getusersitepackages())" 2>/dev/null)
USER_BASE=$(python3 -c "import site; print(site.getuserbase())" 2>/dev/null)
export PATH="$USER_BASE/bin:$PATH"
export PYTHONPATH="$USER_SITE:$PYTHONPATH"

# Start Django in the background
echo "=== Starting Django on port 8000 ==="
echo "PYTHONPATH=$PYTHONPATH"
cd server
nohup python3 manage.py runserver 0.0.0.0:8000 > ~/django.log 2>&1 &
DJANGO_PID=$!
echo "Django PID: $DJANGO_PID"
sleep 4

# Check Django is alive
if ! kill -0 $DJANGO_PID 2>/dev/null; then
    echo "ERROR: Django failed to start. Last log lines:"
    tail -20 ~/django.log
    exit 1
fi
echo "Django is running at http://localhost:8000"

cd ..

# Start ngrok
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "Note: NGROK_AUTHTOKEN not set. URL will be random."
    echo "Get a free authtoken at: https://dashboard.ngrok.com/get-started/your-authtoken"
fi

echo "=== Starting ngrok ==="
nohup ./ngrok http 8000 --log=stdout > ~/ngrok.log 2>&1 &
NGROK_PID=$!
echo "ngrok PID: $NGROK_PID"
sleep 5

# Get public URL from ngrok API
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for t in data.get('tunnels', []):
        if t.get('proto') == 'https':
            print(t['public_url'])
            break
except Exception as e:
    print('', file=sys.stderr)
")
if [ -z "$PUBLIC_URL" ]; then
    echo "ERROR: Could not get ngrok URL. Last ngrok log lines:"
    tail -20 ~/ngrok.log
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
echo "Press Ctrl+C to stop Django and ngrok."
echo ""

# Save URL to file for screenshot script
echo "$PUBLIC_URL" > ~/deployed_url.txt

# Wait for both
wait
