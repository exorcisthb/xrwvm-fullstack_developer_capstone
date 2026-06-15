#!/usr/bin/env python3
"""
Auto-capture screenshots for Capstone submission (Tasks 25-28).

Run on the IBM SkillsBuild lab terminal AFTER bash start_cloudflared.sh
has produced a working public URL.

URL resolution order:
  1. Command-line argument
  2. /home/theia/deployed_url.txt (written by start_cloudflared.sh)
  3. ~/deployed_url.txt
  4. /home/project/deploymentURL.txt
  5. Hard-coded fallback

Usage:
    python3 take_screenshots.py
    python3 take_screenshots.py https://your-deployment-url
"""
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Test user created by seed_data
USERNAME = "testuser"
PASSWORD = "TestPass123"

# Save into the lab user's home so the user can pull/scp them out
OUT_DIR = Path.home() / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

VIEWPORT = {"width": 1366, "height": 850}


def resolve_url() -> str:
    if len(sys.argv) > 1:
        return sys.argv[1].rstrip("/")

    candidates = [
        Path("/home/theia/deployed_url.txt"),
        Path.home() / "deployed_url.txt",
        Path("/home/theia/xrwvm-fullstack_developer_capstone/deploymentURL.txt"),
        Path("/home/project/deploymentURL.txt"),
        Path("/home/project/xrwvm-fullstack_developer_capstone/deploymentURL.txt"),
    ]
    for p in candidates:
        try:
            if p.exists():
                txt = p.read_text().strip()
                if txt:
                    return txt.rstrip("/")
        except Exception:
            continue

    print("ERROR: No deployment URL found. Pass it as argv[1] or run start_cloudflared.sh first.")
    sys.exit(1)


def shoot(page, name: str):
    path = OUT_DIR / name
    page.screenshot(path=str(path), full_page=True)
    size = path.stat().st_size
    print(f"  [OK] {path}  ({size:,} bytes)")
    return str(path)


def main():
    URL = resolve_url()
    print(f"Deployment URL: {URL}")
    print(f"Output dir:     {OUT_DIR}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        context = browser.new_context(viewport=VIEWPORT, ignore_https_errors=True)
        page = context.new_page()

        # ---------------- Task 25: landing page ----------------
        print("[Task 25] Landing page ...")
        page.goto(f"{URL}/", wait_until="domcontentloaded", timeout=60000)
        # Give the SPA/JS time to render the dealer grid
        time.sleep(5)
        shoot(page, "deployed_landingpage.png")

        # ---------------- Login ----------------
        print("[Login] Signing in as testuser ...")
        logged_in = False
        try:
            page.goto(f"{URL}/login-page/", wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            page.fill("input[name=username]", USERNAME)
            page.fill("input[name=password]", PASSWORD)
            page.click("button[type=submit], input[type=submit]")
            page.wait_for_load_state("networkidle", timeout=20000)
            logged_in = True
        except Exception as exc:
            print(f"  Form login path failed ({exc}); trying API login ...")
            try:
                csrf = context.cookies()
                csrf_token = next(
                    (c["value"] for c in csrf if c["name"] == "csrftoken"), ""
                )
                api_resp = context.request.post(
                    f"{URL}/djangoapp/login",
                    headers={"X-CSRFToken": csrf_token, "Referer": URL + "/"},
                    form={"userName": USERNAME, "password": PASSWORD},
                )
                print(f"  API login status: {api_resp.status}")
                if api_resp.ok:
                    logged_in = True
            except Exception as exc2:
                print(f"  API login also failed: {exc2}")

        if not logged_in:
            print("  WARNING: Could not confirm login; continuing anyway.")

        # ---------------- Task 26: logged-in page ----------------
        print("[Task 26] Logged-in home ...")
        page.goto(f"{URL}/", wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)
        shoot(page, "deployed_loggedin.png")

        # ---------------- Task 27: dealer detail page ----------------
        print("[Task 27] Dealer detail (id=1) ...")
        page.goto(
            f"{URL}/djangoapp/dealer/1/", wait_until="domcontentloaded", timeout=30000
        )
        time.sleep(5)
        shoot(page, "deployed_dealer_detail.png")

        # ---------------- Task 28: review displayed ----------------
        print("[Task 28] Add a review and capture it ...")
        review_text = "Absolutely fantastic experience with this dealer. Highly recommended!"
        submitted = False
        try:
            # Try UI form first
            try:
                page.fill("form#review-form textarea[name=review]", review_text)
                page.select_option("form#review-form select[name=car_make]", index=1)
                page.click("form#review-form button[type=submit]")
                page.wait_for_load_state("networkidle", timeout=20000)
                submitted = True
            except Exception:
                pass

            if not submitted:
                # Try the generic review form (any form with a review textarea)
                try:
                    page.fill("textarea[name=review]", review_text)
                    selects = page.query_selector_all("form select")
                    if selects:
                        selects[0].select_option(index=1)
                    page.click("form button[type=submit]")
                    page.wait_for_load_state("networkidle", timeout=20000)
                    submitted = True
                except Exception:
                    pass

            if not submitted:
                # Fallback: API
                csrf = context.cookies()
                csrf_token = next(
                    (c["value"] for c in csrf if c["name"] == "csrftoken"), ""
                )
                api_resp = context.request.post(
                    f"{URL}/djangoapp/reviews/add",
                    headers={"X-CSRFToken": csrf_token, "Referer": URL + "/"},
                    form={
                        "dealerId": 1,
                        "review": review_text,
                        "car_make": 1,
                        "car_year": 2024,
                        "purchase_date": "2024-01-15",
                        "purchase": "true",
                    },
                )
                print(f"  API review submit status: {api_resp.status}")
        except Exception as exc:
            print(f"  Review submission error: {exc}")

        # Reload the dealer page so the screenshot shows the new review
        page.goto(
            f"{URL}/djangoapp/dealer/1/", wait_until="domcontentloaded", timeout=30000
        )
        time.sleep(5)
        shoot(page, "deployed_add_review.png")

        browser.close()

    print()
    print("All screenshots written to:", OUT_DIR)
    for f in sorted(OUT_DIR.glob("deployed_*.png")):
        print(" -", f, f"({f.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
