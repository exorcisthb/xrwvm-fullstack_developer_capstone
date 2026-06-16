#!/usr/bin/env bash
# Diagnose Python environment
echo "=== which python3 ==="
which python3
echo ""
echo "=== python3 --version ==="
python3 --version
echo ""
echo "=== which pip ==="
which pip
echo ""
echo "=== which pip3 ==="
which pip3
echo ""
echo "=== python3 -m pip --version ==="
python3 -m pip --version
echo ""
echo "=== python3 -c 'import sys; print(sys.executable); print(sys.path)' ==="
python3 -c "import sys; print(sys.executable); print(sys.path)"
echo ""
echo "=== ls /home/theia/.local/lib/ ==="
ls /home/theia/.local/lib/ 2>/dev/null
echo ""
echo "=== Check for django anywhere ==="
find / -name "django" -type d 2>/dev/null | head -5
echo ""
echo "=== Try to import django from python3 ==="
python3 -c "import django; print(django.__file__)" 2>&1
echo ""
echo "=== Try with explicit PYTHONPATH to 3.10 user site ==="
PYTHONPATH=/home/theia/.local/lib/python3.10/site-packages python3 -c "import django; print(django.__file__)" 2>&1
echo ""
echo "=== Try with explicit PYTHONPATH to 3.11 user site ==="
PYTHONPATH=/home/theia/.local/lib/python3.11/site-packages python3 -c "import django; print(django.__file__)" 2>&1
