#!/usr/bin/env python3
"""
Auto-capture screenshots for Capstone submission (Tasks 25-28).

Run on the IBM SkillsBuild lab terminal AFTER bash start_cloudflared.sh
has produced a working public URL.

Usage:
    python3 take_screenshots.py
    # or
    python3 take_screenshots.py https://your-deployment-url
"""
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

# Default to the URL produced by start_cloudflared.sh
DEFAULT_URL = "https://promotion-cartoons-wellness-outstanding.trycloudflare.com"
URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else DEFAULT_URL

# Save into the lab user's home so the user can pull/scp them out
OUT_DIR = Path.home() / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Test user created by seed_data
USERNAME = "testuser"
PASSWORD = "TestPass123"

VIEWPORT = {"width": 1366, "height": 850}


def shoot(page, name: str):
    """Take a full-page screenshot and print the saved path."""
    path = OUT_DIR / name
    page.screenshot(path=str(path), full_page=True)
    size = path.stat().st_size
    print(f"  [OK] {path}  ({size:,} bytes)")
    return str(path)


def main():
    print(f"Deployment URL: {URL}")
    print(f"Output dir:     {OUT_DIR}")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(viewport=VIEWPORT, ignore_https_errors=True)
        page = context.new_page()

        # ---------------- Task 25: landing page ----------------
        print("[Task 25] Landing page ...")
        page.goto(f"{URL}/", wait_until="networkidle", timeout=30000)
        page.wait_for_selector(".dealers-grid", timeout=10000)
        time.sleep(1)
        shoot(page, "deployed_landingpage.png")

        # ---------------- Login ----------------
        print("[Login] Signing in as testuser ...")
        page.goto(f"{URL}/login-page/", wait_until="networkidle", timeout=30000)
        # Login form has fields: username, password (default Django template).
        # Fall back to the API endpoint if the page form is missing.
        try:
            page.fill("input[name=username]", USERNAME)
            page.fill("input[name=password]", PASSWORD)
            page.click("button[type=submit], input[type=submit]")
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as exc:
            print(f"  Form login path failed ({exc}); trying API login ...")
            csrf = context.cookies()
            csrf_token = next((c["value"] for c in csrf if c["name"] == "csrftoken"), "")
            api_resp = context.request.post(
                f"{URL}/djangoapp/login",
                headers={"X-CSRFToken": csrf_token, "Referer": URL + "/"},
                form={
                    "userName": USERNAME,
                    "password": PASSWORD,
                },
            )
            print(f"  API login status: {api_resp.status}")
            page.goto(f"{URL}/", wait_until="networkidle", timeout=30000)

        # ---------------- Task 26: logged-in page ----------------
        print("[Task 26] Logged-in home ...")
        page.goto(f"{URL}/", wait_until="networkidle", timeout=30000)
        # Make sure the user-badge is visible so the screenshot proves login
        try:
            page.wait_for_selector(".user-badge", timeout=10000)
        except Exception:
            # maybe the navbar uses a different selector; continue anyway
            pass
        time.sleep(1)
        shoot(page, "deployed_loggedin.png")

        # ---------------- Task 27: dealer detail page ----------------
        print("[Task 27] Dealer detail (id=1) ...")
        page.goto(f"{URL}/djangoapp/dealer/1/", wait_until="networkidle", timeout=30000)
        page.wait_for_selector(".dealer-detail-header", timeout=10000)
        time.sleep(1)
        shoot(page, "deployed_dealer_detail.png")

        # ---------------- Task 28: review displayed ----------------
        # The review form is in the same page (after the reviews list).
        # Submit a fresh review so the screenshot shows the new entry.
        print("[Task 28] Add a review and capture it ...")
        try:
            page.fill(
                "form#review-form textarea[name=review]",
                "Absolutely fantastic experience with this dealer. Highly recommended!",
            )
            page.select_option("form#review-form select[name=car_make]", index=1)
            page.click("form#review-form button[type=submit]")
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception as exc:
            print(f"  Could not submit form via UI ({exc}); falling back to API ...")
            csrf = context.cookies()
            csrf_token = next((c["value"] for c in csrf if c["name"] == "csrftoken"), "")
            context.request.post(
                f"{URL}/djangoapp/reviews/add",
                headers={"X-CSRFToken": csrf_token, "Referer": URL + "/"},
                form={
                    "dealerId": 1,
                    "review": "Absolutely fantastic experience with this dealer. Highly recommended!",
                    "car_make": 1,
                    "car_year": 2024,
                    "purchase_date": "2024-01-15",
                    "purchase": "true",
                },
            )
            page.goto(f"{URL}/djangoapp/dealer/1/", wait_until="networkidle", timeout=30000)

        time.sleep(1)
        shoot(page, "deployed_add_review.png")

        browser.close()

    print()
    print("All screenshots written to:", OUT_DIR)
    for f in sorted(OUT_DIR.glob("deployed_*.png")):
        print(" -", f)


if __name__ == "__main__":
    main()
