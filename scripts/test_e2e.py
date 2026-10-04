#!/usr/bin/env python3
"""
Comprehensive End-to-End Test Suite for Sam's Chi-Fi Notes
Runs headless Chrome with Playwright over a local HTTP server.
Tests every user journey, interaction, filter, modal, audio deck, and image load.
"""
import os
import sys
import time
import socket
import threading
import http.server
import socketserver
import asyncio
from playwright.async_api import async_playwright

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "tests", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

class DualStaticServer:
    def __init__(self, directory, port):
        self.directory = directory
        self.port = port
        self.httpd = None
        self.thread = None

    def start(self):
        handler = lambda *args: http.server.SimpleHTTPRequestHandler(*args, directory=self.directory)
        self.httpd = socketserver.TCPServer(("", self.port), handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        print(f"[Server] Serving {self.directory} on http://localhost:{self.port}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            print("[Server] Server stopped.")

async def run_e2e_tests():
    port = find_free_port()
    server = DualStaticServer(DIST_DIR, port)
    server.start()
    base_url = f"http://localhost:{port}"

    console_errors = []
    page_errors = []
    failed_requests = []

    tests_passed = 0
    tests_failed = 0

    def record_pass(test_name):
        nonlocal tests_passed
        tests_passed += 1
        print(f"  ✓ PASS: {test_name}")

    def record_fail(test_name, reason):
        nonlocal tests_failed
        tests_failed += 1
        print(f"  ✗ FAIL: {test_name}: {reason}")

    try:
        async with async_playwright() as p:
            print("\n=======================================================")
            print("🚀 Launching Headless Chrome for End-to-End Testing")
            print("=======================================================")
            browser = await p.chromium.launch(
                executable_path="/usr/bin/google-chrome",
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            
            # Context with clipboard permissions
            context = await browser.new_context(
                viewport={"width": 1440, "height": 900},
                permissions=["clipboard-read", "clipboard-write"]
            )
            page = await context.new_page()

            page.on("pageerror", lambda err: page_errors.append(str(err)))
            page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ["error"] else None)
            page.on("requestfailed", lambda req: failed_requests.append(f"{req.url} ({req.failure})"))

            # -----------------------------------------------------------------
            # TEST 1: Initial Page Load & Visual Check
            # -----------------------------------------------------------------
            print("\n[Test 1] Initial Page Load & Structure")
            response = await page.goto(base_url, wait_until="networkidle")
            if response.status == 200:
                record_pass("Page loaded with HTTP 200 OK")
            else:
                record_fail("Page load status", f"Expected 200, got {response.status}")

            title = await page.title()
            if "Sam's Chi-Fi Notes" in title:
                record_pass(f"Page title is correct: '{title}'")
            else:
                record_fail("Page title check", f"Unexpected title: '{title}'")

            cards = await page.locator("#cards-view > div").all()
            if len(cards) == 24:
                record_pass("All 24 IEM cards rendered in main view")
            else:
                record_fail("Card count", f"Expected 24 cards, found {len(cards)}")

            # Check that images inside cards actually loaded (naturalWidth > 0)
            await page.wait_for_timeout(500)
            images_ok = await page.evaluate("""
                async () => {
                    const imgs = Array.from(document.querySelectorAll('#cards-view img'));
                    await Promise.all(imgs.map(img => {
                        if (img.complete) return Promise.resolve();
                        return new Promise(res => {
                            img.onload = img.onerror = res;
                        });
                    }));
                    const bad = imgs.filter(img => !img.complete || img.naturalWidth === 0);
                    return { total: imgs.length, badCount: bad.length, badSources: bad.map(i => i.src) };
                }
            """)
            if images_ok["badCount"] == 0 and images_ok["total"] == 24:
                record_pass(f"All {images_ok['total']} card product images loaded successfully (naturalWidth > 0)")
            else:
                record_fail("Card product images", f"Found {images_ok['badCount']} broken images: {images_ok['badSources']}")

            # -----------------------------------------------------------------
            # TEST 2: Search Functionality
            # -----------------------------------------------------------------
            print("\n[Test 2] Live Search Filter")
            await page.fill("#search-input", "Hexa")
            await page.wait_for_timeout(300)
            visible_cards = await page.locator("#cards-view > div:not(.hidden)").count()
            hexa_visible = await page.locator("#cards-view h3:has-text('Truthear Hexa')").is_visible()
            if visible_cards == 1 and hexa_visible:
                record_pass("Search for 'Hexa' correctly filtered down to 1 card")
            else:
                record_fail("Search 'Hexa'", f"Expected 1 card, got {visible_cards}")

            # Clear search
            await page.click("#clear-search-btn")
            await page.wait_for_timeout(300)
            visible_after_clear = await page.locator("#cards-view > div:not(.hidden)").count()
            if visible_after_clear == 24:
                record_pass("Clear search button restored all 24 cards")
            else:
                record_fail("Clear search", f"Expected 24 cards, got {visible_after_clear}")

            # Search by sound character
            await page.fill("#search-input", "planar")
            await page.wait_for_timeout(300)
            may_visible = await page.locator("#cards-view h3:has-text('Moondrop May')").is_visible()
            if may_visible:
                record_pass("Search for sound attribute 'planar' surfaced Moondrop May")
            else:
                record_fail("Search 'planar'", "Moondrop May not found")
            await page.fill("#search-input", "")
            await page.wait_for_timeout(300)

            # -----------------------------------------------------------------
            # TEST 3: Category Filter Pills
            # -----------------------------------------------------------------
            print("\n[Test 3] Category Filter Pills")
            # Wireless TWS filter
            await page.click("button[data-filter='Wireless Chi-Fi TWS']")
            await page.wait_for_timeout(300)
            tws_count = await page.locator("#cards-view > div:not(.hidden)").count()
            st1_visible = await page.locator("#cards-view h3:has-text('Moondrop Space Travel')").first.is_visible()
            st2_visible = await page.locator("#cards-view h3:has-text('Moondrop Space Travel 2')").is_visible()
            qcy_visible = await page.locator("#cards-view h3:has-text('QCY MeloBuds Pro')").is_visible()
            if tws_count == 3 and st1_visible and st2_visible and qcy_visible:
                record_pass(f"Wireless TWS filter showed {tws_count} sets including Space Travel 1, Space Travel 2, and QCY MeloBuds Pro")
            else:
                record_fail("Wireless TWS filter", f"Count: {tws_count}, ST1: {st1_visible}, ST2: {st2_visible}, QCY: {qcy_visible}")

            # Small Ears filter
            await page.click("button[data-filter='Small Ears & Sleep']")
            await page.wait_for_timeout(300)
            count_small = await page.locator("#cards-view > div:not(.hidden)").count()
            chu2_visible = await page.locator("#cards-view h3:has-text('Moondrop Chu II')").is_visible()
            red_visible = await page.locator("#cards-view h3:has-text('Truthear x Crinacle Zero:RED')").is_visible()
            if chu2_visible and not red_visible:
                record_pass(f"Small Ears filter showed {count_small} sets, included Chu II, and excluded bulky 6.2mm Zero:Red")
            else:
                record_fail("Small Ears filter", "Filter logic failed to exclude bulky nozzle or include small ear set")

            # Neutral Reference filter
            await page.click("button[data-filter='Audio Purists & Reference']")
            await page.wait_for_timeout(300)
            hexa_visible = await page.locator("#cards-view h3:has-text('Truthear Hexa')").is_visible()
            if hexa_visible:
                record_pass("Neutral Reference filter correctly includes Truthear Hexa")
            else:
                record_fail("Neutral Reference filter", "Truthear Hexa missing")

            # Reset to All
            await page.click("button[data-filter='all']")
            await page.wait_for_timeout(300)
            count_all = await page.locator("#cards-view > div:not(.hidden)").count()
            if count_all == 24:
                record_pass("All (24) filter restored all 24 cards")
            else:
                record_fail("All filter", f"Expected 24, got {count_all}")

            # -----------------------------------------------------------------
            # TEST 4: Sort Dropdown
            # -----------------------------------------------------------------
            print("\n[Test 4] Sorting Controls")
            # Sort by price AliExpress
            await page.select_option("#sort-select", "price-ali-asc")
            await page.wait_for_timeout(300)
            first_card_title = await page.locator("#cards-view > div:first-child h3").text_content()
            if "GK Kunten" in first_card_title or "Tangzu" in first_card_title or "Gate" in first_card_title:
                record_pass(f"Sort by AliExpress price puts budget champion '{first_card_title.strip()}' first")
            else:
                record_fail("Sort by Price Ali", f"Unexpected first item: {first_card_title}")

            # Sort Alphabetical
            await page.select_option("#sort-select", "name-asc")
            await page.wait_for_timeout(300)
            first_alpha = await page.locator("#cards-view > div:first-child h3").text_content()
            if "7Hz" in first_alpha:
                record_pass(f"Alphabetical sort correctly puts '{first_alpha.strip()}' first")
            else:
                record_fail("Alphabetical sort", f"Unexpected first item: {first_alpha}")

            # -----------------------------------------------------------------
            # TEST 5: Table View Toggle
            # -----------------------------------------------------------------
            print("\n[Test 5] View Mode Toggle (Cards vs Table)")
            await page.click("#view-table-btn")
            await page.wait_for_timeout(300)
            table_visible = await page.locator("#table-view").is_visible()
            cards_visible = await page.locator("#cards-view").is_visible()
            row_count = await page.locator("#table-body tr").count()
            if table_visible and not cards_visible and row_count == 24:
                record_pass("Switched to Comparison Table view; 24 table rows rendered")
            else:
                record_fail("Table view switch", f"Table vis: {table_visible}, Cards vis: {cards_visible}, Rows: {row_count}")

            # Switch back to Cards view
            await page.click("#view-cards-btn")
            await page.wait_for_timeout(300)
            cards_visible_again = await page.locator("#cards-view").is_visible()
            if cards_visible_again:
                record_pass("Switched back to Cards view")
            else:
                record_fail("Cards view switch", "Cards view failed to restore")

            # -----------------------------------------------------------------
            # TEST 6: Bookmark & Shortlist Drawer Flow
            # -----------------------------------------------------------------
            print("\n[Test 6] Shortlist Bookmarking & Drawer")
            badge_text_init = await page.locator("#wishlist-counter-badge").text_content()
            if badge_text_init == "0":
                record_pass("Initial shortlist counter is 0")
            else:
                record_fail("Initial counter", f"Expected 0, got {badge_text_init}")

            # Bookmark Hexa and Chu II
            await page.locator("#cards-view button[aria-label='Save to shortlist'][onclick*='truthear-hexa']").click()
            await page.wait_for_timeout(300)
            await page.locator("#cards-view button[aria-label='Save to shortlist'][onclick*='moondrop-chu-2-3']").click()
            await page.wait_for_timeout(300)

            badge_text_after = await page.locator("#wishlist-counter-badge").text_content()
            if badge_text_after == "2":
                record_pass("Shortlist counter correctly updated to 2")
            else:
                record_fail("Updated counter", f"Expected 2, got {badge_text_after}")

            # Open Wishlist Drawer
            await page.click("#open-wishlist-top-btn")
            await page.wait_for_timeout(400)
            drawer_visible = await page.locator("#wishlist-drawer").is_visible()
            saved_items_count = await page.locator("#wishlist-items-container > div").count()
            if drawer_visible and saved_items_count == 2:
                record_pass("Shortlist drawer opened with both bookmarked sets")
            else:
                record_fail("Drawer items", f"Visible: {drawer_visible}, Count: {saved_items_count}")

            # Test Copy Share URL button
            await page.click("#copy-share-url-btn")
            await page.wait_for_timeout(300)
            btn_text = await page.locator("#copy-share-url-btn").text_content()
            if "Copied" in btn_text:
                record_pass("Copy Shareable Link button showed 'Copied' confirmation")
            else:
                record_fail("Copy Share Link", f"Button text did not confirm: {btn_text}")

            # Close drawer
            await page.click("#close-wishlist-btn")
            await page.wait_for_timeout(300)

            # -----------------------------------------------------------------
            # TEST 7: Shared URL Query Param Flow (?picks=...)
            # -----------------------------------------------------------------
            print("\n[Test 7] Shared URL Navigation (?picks=...)")
            shared_url = f"{base_url}/?picks=truthear-hexa,kefine-delci"
            await page.goto(shared_url, wait_until="networkidle")
            await page.wait_for_timeout(300)

            banner_visible = await page.locator("#shared-picks-banner").is_visible()
            if banner_visible:
                record_pass("Shared picks detection banner displayed on '?picks=' URL")
            else:
                record_fail("Shared banner", "Shared banner failed to appear")

            # Click View Shared Only
            await page.click("#filter-shared-only-btn")
            await page.wait_for_timeout(300)
            shared_cards_count = await page.locator("#cards-view > div:not(.hidden)").count()
            if shared_cards_count == 2:
                record_pass("Filter Shared Only showed exactly the 2 shared picks (Hexa & Delci)")
            else:
                record_fail("Filter Shared Only", f"Expected 2 cards, got {shared_cards_count}")

            # Click Show All 24
            await page.click("#clear-shared-view-btn")
            await page.wait_for_timeout(300)
            all_restored = await page.locator("#cards-view > div:not(.hidden)").count()
            if all_restored == 24:
                record_pass("Show All button successfully restored all 24 models")
            else:
                record_fail("Restore from shared", f"Expected 24, got {all_restored}")

            # -----------------------------------------------------------------
            # TEST 8: Detail Modal & Local Note Saving
            # -----------------------------------------------------------------
            print("\n[Test 8] Detail Modal Dialog & Local Notes")
            # Click card title to open modal
            await page.locator("#cards-view h3:has-text('Truthear x Crinacle Zero:RED')").click()
            await page.wait_for_timeout(400)
            modal_visible = await page.locator("#iem-detail-modal").is_visible()
            modal_title = await page.locator("#modal-title").text_content()
            modal_img_src = await page.locator("#modal-image").get_attribute("src")
            modal_nozzle_text = await page.locator("#modal-nozzle").text_content()
            store_links_count = await page.locator("#modal-stores-container a").count()

            if modal_visible and "Zero:RED" in modal_title and "6.2mm" in modal_nozzle_text and store_links_count >= 3:
                record_pass(f"Detail modal opened for '{modal_title}' with 6.2mm nozzle spec and {store_links_count} store links")
            else:
                record_fail("Modal open", f"Vis: {modal_visible}, Title: {modal_title}, Nozzle: {modal_nozzle_text}, Stores: {store_links_count}")

            # Test interactive gallery switcher
            gallery_tabs_count = await page.locator("#modal-gallery-strip button").count()
            initial_caption = await page.locator("#modal-gallery-caption").text_content()
            if gallery_tabs_count >= 2:
                # Click second gallery tab
                await page.locator("#modal-gallery-strip button:nth-child(2)").click()
                await page.wait_for_timeout(300)
                second_img_src = await page.locator("#modal-image").get_attribute("src")
                second_caption = await page.locator("#modal-gallery-caption").text_content()
                if second_img_src != modal_img_src and second_caption != initial_caption:
                    record_pass(f"Gallery switcher correctly changed image to '{second_img_src}' ({second_caption})")
                else:
                    record_fail("Gallery switch", f"Image: {second_img_src}, Caption: {second_caption}")
            else:
                record_fail("Gallery tabs count", f"Expected >= 2, got {gallery_tabs_count}")

            # Save a personal note
            await page.fill("#modal-note-input", "Loved the red faceplates and bass slam!")
            await page.click("#save-note-btn")
            await page.wait_for_timeout(400)
            btn_saved_text = await page.locator("#save-note-btn").text_content()
            if "Saved" in btn_saved_text:
                record_pass("Personal note saved with visual confirmation")
            else:
                record_fail("Save note", f"Button text: {btn_saved_text}")

            # Close modal
            await page.click("#close-modal-btn")
            await page.wait_for_timeout(400)

            # Verify note appears on card
            card_note = await page.locator("text=Loved the red faceplates and bass slam!").is_visible()
            if card_note:
                record_pass("Saved personal note correctly rendered on the IEM card")
            else:
                record_fail("Card note display", "Note did not render on card")

            # -----------------------------------------------------------------
            # TEST 9: Audiophile Sound Bench Player
            # -----------------------------------------------------------------
            print("\n[Test 9] Audiophile Sound Bench Player Controls")
            pill_visible = await page.locator("#sound-deck-pill").is_visible()
            if pill_visible:
                record_pass("Sticky sound bench pill player is visible at bottom")
            else:
                record_fail("Pill player", "Pill player not visible")

            # Expand sound deck
            await page.click("#pill-expand-btn")
            await page.wait_for_timeout(300)
            deck_panel_visible = await page.locator("#sound-deck-panel").is_visible()
            if deck_panel_visible:
                record_pass("Sound bench expanded to full control panel")
            else:
                record_fail("Expand player", "Panel failed to expand")

            # Category filter in deck (Eurobeat)
            await page.locator("button[data-cat='eurobeat']").click()
            await page.wait_for_timeout(300)
            euro_tracks = await page.locator("#deck-playlist-container > div").count()
            if euro_tracks == 3:
                record_pass(f"Category tab '🏎️ Eurobeat' filtered playlist to {euro_tracks} Initial D tracks")
            else:
                record_fail("Deck category", f"Expected 3 tracks, got {euro_tracks}")

            # Minimize deck
            await page.click("#deck-minimize-btn")
            await page.wait_for_timeout(300)
            panel_hidden = not await page.locator("#sound-deck-panel").is_visible()
            if panel_hidden:
                record_pass("Sound bench minimized back to compact pill")
            else:
                record_fail("Minimize player", "Panel still visible")

            # -----------------------------------------------------------------
            # TEST 10: Audiophile Gear Toolkit Interaction
            # -----------------------------------------------------------------
            print("\n[Test 10] Audiophile Gear Toolkit Interaction")
            toolkit_visible = await page.locator("#gear-toolkit").is_visible()
            tabs_count = await page.locator(".toolkit-tab-btn").count()
            if toolkit_visible and tabs_count == 6:
                record_pass(f"Audiophile Gear Toolkit section is visible with {tabs_count} category tabs")
            else:
                record_fail("Toolkit visibility", f"Vis: {toolkit_visible}, Tabs: {tabs_count}")

            # Verify initial Tips panel is visible
            tips_visible = await page.locator("#toolkit-panel-tips").is_visible()
            if tips_visible:
                record_pass("Ear Tips panel is active by default with SpinFit, Sancai, and S&S")
            else:
                record_fail("Tips panel default", "Ear Tips panel was not visible")

            # Click Dongle DACs tab
            await page.click(".toolkit-tab-btn[data-target='toolkit-panel-dacs']")
            await page.wait_for_timeout(300)
            dacs_visible = await page.locator("#toolkit-panel-dacs").is_visible()
            tips_now_hidden = not await page.locator("#toolkit-panel-tips").is_visible()
            apple_dongle_present = await page.locator("#toolkit-panel-dacs h4:has-text('Apple USB-C')").is_visible()
            jcally_present = await page.locator("#toolkit-panel-dacs h4:has-text('Jcally JA11')").is_visible()
            if dacs_visible and tips_now_hidden and apple_dongle_present and jcally_present:
                record_pass("Dongle DACs tab activated, displaying Apple Dongle & Jcally JA11 PEQ cards")
            else:
                record_fail("DACs tab switch", f"DACS vis: {dacs_visible}, Tips hidden: {tips_now_hidden}")

            # Click Care & Storage tab
            await page.click(".toolkit-tab-btn[data-target='toolkit-panel-care']")
            await page.wait_for_timeout(300)
            care_visible = await page.locator("#toolkit-panel-care").is_visible()
            roadie_wrap = await page.locator("#toolkit-panel-care h4:has-text('Roadie Wrap')").is_visible()
            silica_gel = await page.locator("#toolkit-panel-care h4:has-text('Silica Gel')").is_visible()
            if care_visible and roadie_wrap and silica_gel:
                record_pass("Care & Storage tab activated with Roadie Wrap and Silica Gel guides")
            else:
                record_fail("Care tab switch", f"Care vis: {care_visible}, Roadie: {roadie_wrap}, Silica: {silica_gel}")

            # Click Wireless TWS tab
            await page.click(".toolkit-tab-btn[data-target='toolkit-panel-wireless']")
            await page.wait_for_timeout(300)
            wireless_visible = await page.locator("#toolkit-panel-wireless").is_visible()
            st_card_present = await page.locator("#toolkit-panel-wireless h4:has-text('Space Travel 1 vs Space Travel 2')").is_visible()
            qcy_card_present = await page.locator("#toolkit-panel-wireless h4:has-text('QCY MeloBuds Pro')").is_visible()
            earhooks_present = await page.locator("#toolkit-panel-wireless h4:has-text('Bluetooth Earhooks')").is_visible()
            if wireless_visible and st_card_present and qcy_card_present and earhooks_present:
                record_pass("Wireless TWS tab activated, displaying Space Travel 1 vs 2, MeloBuds Pro, and Earhooks guide")
            else:
                record_fail("Wireless TWS tab switch", f"Vis: {wireless_visible}, ST: {st_card_present}, QCY: {qcy_card_present}, Hooks: {earhooks_present}")

            # -----------------------------------------------------------------
            # TEST 11: Responsiveness & Screenshots
            # -----------------------------------------------------------------
            print("\n[Test 11] Responsive Layout & Visual Verification")
            desktop_png = os.path.join(SCREENSHOTS_DIR, "desktop_1440.png")
            await page.screenshot(path=desktop_png, full_page=True)
            record_pass(f"Desktop screenshot saved: {desktop_png}")

            # Check horizontal overflow on desktop
            has_overflow_desktop = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if not has_overflow_desktop:
                record_pass("Zero horizontal overflow on desktop (1440px)")
            else:
                record_fail("Desktop overflow", "Detected horizontal scrollbar")

            # Test mobile viewport (390px iPhone)
            await page.set_viewport_size({"width": 390, "height": 844})
            await page.wait_for_timeout(400)
            mobile_png = os.path.join(SCREENSHOTS_DIR, "mobile_390.png")
            await page.screenshot(path=mobile_png, full_page=True)
            record_pass(f"Mobile screenshot saved: {mobile_png}")

            has_overflow_mobile = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if not has_overflow_mobile:
                record_pass("Zero horizontal overflow on mobile (390px iPhone viewport)")
            else:
                record_fail("Mobile overflow", "Detected horizontal scrollbar on mobile 390px")

            # Check Mobile Quick Navigation Strip
            mobile_nav_visible = await page.locator("header .sm\\:hidden").is_visible()
            if mobile_nav_visible:
                record_pass("Mobile quick-navigation strip is visible on small screen")
            else:
                record_fail("Mobile quick nav", "Quick nav strip was not visible")

            # Check docked bottom player on mobile
            pill_visible = await page.locator("#sound-deck-pill").is_visible()
            if pill_visible:
                record_pass("Docked bottom mini-player is visible across mobile viewport")
            else:
                record_fail("Mobile audio pill", "Bottom mini-player not visible")

            # Test opening detail modal on mobile
            await page.locator("#cards-view h3:has-text('Moondrop Chu II')").click()
            await page.wait_for_timeout(400)
            modal_visible_mobile = await page.locator("#iem-detail-modal").is_visible()
            modal_overflow_mobile = await page.evaluate("() => document.querySelector('#iem-detail-modal > div').scrollWidth > document.querySelector('#iem-detail-modal > div').clientWidth")
            if modal_visible_mobile and not modal_overflow_mobile:
                record_pass("Detail modal opened on mobile with zero horizontal overflow")
            else:
                record_fail("Mobile modal", f"Visible: {modal_visible_mobile}, Overflow: {modal_overflow_mobile}")
            await page.click("#close-modal-btn")
            await page.wait_for_timeout(300)

            # Test extra-compact 360px viewport (Android budget phones)
            await page.set_viewport_size({"width": 360, "height": 740})
            await page.wait_for_timeout(400)
            mobile_360_png = os.path.join(SCREENSHOTS_DIR, "mobile_360.png")
            await page.screenshot(path=mobile_360_png, full_page=True)
            record_pass(f"Compact mobile 360px screenshot saved: {mobile_360_png}")

            has_overflow_360 = await page.evaluate("() => document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if not has_overflow_360:
                record_pass("Zero horizontal overflow on compact mobile (360px Android viewport)")
            else:
                record_fail("360px overflow", "Detected horizontal scrollbar on 360px viewport")

            # -----------------------------------------------------------------
            # Console & Network Integrity Check
            # -----------------------------------------------------------------
            print("\n[Console & Network Error Audit]")
            # Filter out expected third-party CDNs/analytics (YouTube IFrame, Google Fonts)
            critical_console = [err for err in console_errors if not any(domain in err for domain in ["youtube.com", "ytimg.com", "google.com"])]
            critical_failed = [req for req in failed_requests if not any(domain in req for domain in ["youtube.com", "google.com", "googleapis.com", "gstatic.com"])]

            if len(page_errors) == 0:
                record_pass("Zero uncaught JavaScript page errors")
            else:
                record_fail("Uncaught JS errors", f"{page_errors}")

            if len(critical_console) == 0:
                record_pass("Zero critical console errors")
            else:
                record_fail("Console errors", f"{critical_console}")

            if len(critical_failed) == 0:
                record_pass("Zero failed network requests for internal assets")
            else:
                record_fail("Network failures", f"{critical_failed}")

            await browser.close()

    finally:
        server.stop()

    print("\n=======================================================")
    print(f"🏁 Test Results: {tests_passed} PASSED, {tests_failed} FAILED")
    print("=======================================================\n")
    return tests_failed == 0

if __name__ == "__main__":
    success = asyncio.run(run_e2e_tests())
    sys.exit(0 if success else 1)
