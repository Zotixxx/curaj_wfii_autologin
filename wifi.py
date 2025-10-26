import asyncio
from playwright.async_api import async_playwright

# ---------------- CONFIG ----------------
REDIRECT_URL = "http://www.msftconnecttest.com/redirect"
FALLBACK_USERNAME = "8368786617"
FALLBACK_PASSWORD = "7fday7qh"
AUTOFILL_WAIT = 3  # seconds to let browser autofill if passwords are saved
# ----------------------------------------

async def main():
    async with async_playwright() as p:
        print("[START] CURAJ Wi-Fi login automation with redirect flow.")

        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Step 1: Trigger Wi-Fi redirect
        print("[STEP] Opening redirect URL to trigger captive portal...")
        await page.goto(REDIRECT_URL, timeout=20000)

        # Wait for possible redirection
        await asyncio.sleep(5)

        # Step 2: Wait for Campus Login Page to appear
        print("[STEP] Waiting for portal page to load...")
        await page.wait_for_load_state("networkidle", timeout=15000)

        # Click "Campus User Login"
        try:
            await page.click("text=Campus User Login")
            print("[INFO] Clicked on 'Campus User Login'.")
        except:
            print("[WARN] Could not find 'Campus User Login'. It might already be open.")

        # Click "Existing User Login"
        try:
            await page.click("text=Existing User Login")
            print("[INFO] Clicked on 'Existing User Login'.")
        except:
            print("[WARN] Could not find 'Existing User Login'. Continuing anyway...")

        # Step 3: Wait for the username & password fields
        await page.wait_for_selector('input[name="username"]', timeout=15000)
        await page.wait_for_selector('input[name="password"]', timeout=15000)

        # Let browser autofill (if saved)
        await asyncio.sleep(AUTOFILL_WAIT)

        # Fill fallback credentials if fields are empty
        username_val = await page.eval_on_selector('input[name="username"]', "el => el.value")
        if not username_val:
            await page.fill('input[name="username"]', FALLBACK_USERNAME)
            print("[INFO] Entered fallback username.")

        password_val = await page.eval_on_selector('input[name="password"]', "el => el.value")
        if not password_val:
            await page.fill('input[name="password"]', FALLBACK_PASSWORD)
            print("[INFO] Entered fallback password.")

        # Step 4: Click submit or continue
        await page.click('//input[@type="submit" or @value="Continue"]')
        print("[INFO] Submitted login form.")

        # Step 5: Wait for success or redirect
        try:
            await page.wait_for_selector("text=You are connected", timeout=10000)
            print("[SUCCESS] Login successful! You are now connected.")
        except:
            print("[WARN] No success message detected — but the login form was submitted. Check connection manually.")

        # Wait a bit before closing
        await asyncio.sleep(8)
        await browser.close()
        print("[DONE] Browser closed. Script complete.")

# Run it
asyncio.run(main())
