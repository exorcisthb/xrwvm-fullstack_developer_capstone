# Deployment Guide (Tasks 24-28)

This guide explains how to deploy the Django app for Tasks 24-28.

## IMPORTANT CONFIGURATION

This repo is set up to deploy from the **root directory** (not from `server/`):
- `build.sh` at the repo root runs `pip install -r requirements.txt`, then `cd server && python manage.py collectstatic/migrate`
- `requirements.txt` at the repo root is a copy of `server/requirements.txt`
- `render.yaml` is at the repo root
- `Procfile` inside `server/` is also kept for Heroku compatibility

The Django `settings.py` already has:
- `ALLOWED_HOSTS = ['*']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- `whitenoise` in `MIDDLEWARE` for serving static files

---

## Option 1: Render.com (recommended, free tier)

### Step-by-step

1. Make sure your latest code is pushed to GitHub:
   ```bash
   git push origin main
   ```

2. Go to https://render.com and sign in (with GitHub).

3. Click **New +** → **Web Service**.

4. Choose **Build and deploy from a Git repository** → **Next**.

5. Find your repo `xrwvm-fullstack_developer_capstone` and click **Connect**.

6. Fill in:
   - **Name:** `cardealer-capstone` (or any name)
   - **Region:** Oregon (US West) - free tier default
   - **Branch:** `main`
   - **Root Directory:** *(leave empty)*
   - **Runtime:** `Python 3`
   - **Build Command:** `bash build.sh`
   - **Start Command:** `cd server && gunicorn djangoproject.wsgi:application --log-file -`
   - **Instance Type:** `Free`

7. Click **Deploy Web Service**.

8. Watch the **Logs** tab. Build takes 2-5 minutes. When you see
   `==> Your service is live 🎉`, the deploy is done.

9. Copy the URL at the top, e.g. `https://cardealer-capstone.onrender.com`.
   Save it in `deploymentURL.txt`.

10. Open a Shell in Render (left menu → Shell) and seed data:
    ```bash
    cd server
    python manage.py seed_data
    ```
    (If you skip this, the page will be empty.)

11. Take screenshots (Task 25-28):
    ```powershell
    $env:DEPLOY_URL = "https://cardealer-capstone.onrender.com"
    python capture_deployment_screenshots.py
    ```

---

## What `build.sh` does

```bash
#!/usr/bin/env bash
set -o errexit
pip install --upgrade pip
pip install -r requirements.txt
cd server
python manage.py check
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

This is also the same sequence the GitHub Actions workflow runs in CI, so
what passes in CI will pass on Render.

---

## Required Files (already in this repo)

- `build.sh` - build script for Render
- `render.yaml` - Render Blueprint (alternative way to deploy)
- `requirements.txt` - root-level dependencies
- `server/Procfile` - process declaration (Heroku/Railway compatible)
- `server/runtime.txt` - Python version pin
- `server/requirements.txt` - duplicate of root requirements.txt
- `server/djangoproject/settings.py` - already configured

---

## Notes

- Default database is SQLite (perfect for free deploys).
- Static files served by `whitenoise`, no extra CDN needed.
- For the `deployed_loggedin.png` screenshot to show `testuser`, you must run
  `python manage.py seed_data` so that user exists in the deployed database.
- Free Render instances sleep after 15 minutes of inactivity; the first
  request will take ~30s to wake up.
