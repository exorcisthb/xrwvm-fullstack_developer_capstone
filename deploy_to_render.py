"""
Auto-deployment helper for Capstone Project to Render.com

This script automates the deployment process. Before running:
1. Create a Render.com account (free): https://render.com
2. Get your Render API key: https://dashboard.render.com/u/settings#api-keys
3. Set environment variables:
   - RENDER_API_KEY
   - GITHUB_REPO (e.g. exorcisthb/xrwvm-fullstack_developer_capstone)

Usage:
  python deploy_to_render.py
"""
import os
import sys
import json
import time
import urllib.request
import urllib.error


RENDER_API_BASE = "https://api.render.com/v1"


def get_headers():
    api_key = os.environ.get("RENDER_API_KEY", "")
    if not api_key:
        print("ERROR: RENDER_API_KEY environment variable is not set.")
        print("Get one at: https://dashboard.render.com/u/settings#api-keys")
        sys.exit(1)
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def http_request(method, path, body=None):
    url = f"{RENDER_API_BASE}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=get_headers())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        print(f"HTTP {e.code}: {body}")
        raise


def list_services():
    return http_request("GET", "/services?limit=50")


def create_web_service(repo):
    """Create a new Web Service on Render pointing at the given GitHub repo."""
    body = {
        "type": "web_service",
        "name": "cardealer-capstone",
        "ownerId": os.environ.get("RENDER_OWNER_ID", ""),
        "repo": repo,
        "branch": "main",
        "rootDir": "",
        "runtime": "python",
        "plan": "free",
        "buildCommand": "bash build.sh",
        "startCommand": "cd server && gunicorn djangoproject.wsgi:application --log-file -",
        "envVars": [
            {"key": "PYTHON_VERSION", "value": "3.11.10"},
            {"key": "WEB_CONCURRENCY", "value": "2"},
            {"key": "DATABASE_URL", "value": "sqlite:///db.sqlite3"},
        ],
        "autoDeploy": True,
    }
    return http_request("POST", "/services", body)


def find_existing_service(name="cardealer-capstone"):
    data = list_services()
    for s in data:
        if s.get("service", {}).get("name") == name:
            return s["service"]
    return None


def main():
    repo = os.environ.get("GITHUB_REPO", "exorcisthb/xrwvm-fullstack_developer_capstone")
    print(f"Looking for existing service 'cardealer-capstone' in repo {repo}...")
    existing = find_existing_service()
    if existing:
        print(f"Service exists: id={existing['id']}")
        print(f"URL: https://{existing.get('serviceDetails', {}).get('url', 'unknown')}")
        return
    print("Creating new Web Service on Render.com...")
    resp = create_web_service(repo)
    print(json.dumps(resp, indent=2))
    print("\nService creation initiated. Monitor at https://dashboard.render.com")


if __name__ == "__main__":
    main()
