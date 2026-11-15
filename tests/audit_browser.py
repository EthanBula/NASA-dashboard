"""Comprehensive Playwright Browser Audit for NASA PSI Microgravity Dashboard.

Executes Actions 7.3 and 7.4:
- Desktop Viewport Audit (1920x1080)
- Mobile Viewport Audit (390x844)
- Zero console errors assertion
- Touch target and horizontal overflow verification

Authors: Cesia Burgos (Chief Executive Officer, CEO) & Ethan Bula (Chief Operating Officer, COO).
"""

from __future__ import annotations

import time

from playwright.sync_api import sync_playwright


def run_audits() -> None:
    console_errors: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ======================================================================
        # Part 1: Desktop Viewport Audit (1920x1080)
        # ======================================================================
        print("=== Starting Desktop Viewport Audit (1920x1080) ===")
        context_desktop = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context_desktop.new_page()

        # Track console errors
        page.on(
            "console",
            lambda msg: (
                console_errors.append(msg.text) if msg.type == "error" else None
            ),
        )

        page.goto("http://127.0.0.1:7860", wait_until="networkidle", timeout=30000)

        # 1. Title verification
        title = page.title()
        print(f"1. Page Title: '{title}'")
        assert "NASA PSI" in title, f"Unexpected page title: {title}"

        # 2. Sticky top navbar
        navbar = page.locator(".sticky-navbar")
        assert navbar.is_visible(), "Sticky navbar is not visible"
        print("2. Sticky Top Navbar verified visible.")

        # 3. Section 1: Environmental Dashboard & KPIs
        kpi_margin = page.locator("#kpi-margin")
        assert kpi_margin.is_visible()
        initial_margin = kpi_margin.inner_text().strip()
        print(f"3. Initial LOC Flammability Margin KPI: {initial_margin} % O2")

        # 4. Graphs G1 - G4 rendering
        for g_id in [
            "graph-g1-loc",
            "graph-g2-spread",
            "graph-g3-saffire",
            "graph-g4-aerosol",
        ]:
            graph = page.locator(f"#{g_id}")
            assert graph.is_visible(), f"Graph {g_id} is not visible"
        print("4. All 4 Section 1 HUD graphs rendered and visible.")

        # 5. Section 2: Literature Master-Detail & 24 Dedicated Charts
        # Wait for investigation cards to populate
        page.wait_for_selector(".investigation-card-item", timeout=10000)
        card_count = page.locator(".investigation-card-item").count()
        print(f"5. Investigation cards loaded: {card_count}")
        assert card_count >= 24, (
            f"Expected at least 24 investigations, got {card_count}"
        )

        # Click on PSI-98 (Saffire-I)
        psi_98_card = (
            page.locator(".investigation-card-item").filter(has_text="PSI-98").first
        )
        assert psi_98_card.is_visible(), "PSI-98 card not found"
        psi_98_card.click()
        time.sleep(1.0)  # Wait for Dash callback to update detail panel

        # Verify detail panel updated
        detail_container = page.locator("#container-investigation-detail")
        assert "Spacecraft Fire Safety Experiment-I" in detail_container.inner_text()
        print(
            "6. Clicked PSI-98: Detail panel populated with flight metadata and tabs."
        )

        # Verify dedicated chart updated
        dedicated_chart = page.locator("#graph-investigation-detail")
        assert dedicated_chart.is_visible()
        print("7. Dedicated flight experiment chart rendered successfully.")

        # 8. Section 3: AI Copilot Interaction
        # Click suggestion pill 1
        pill1 = page.locator("#pill-1")
        assert pill1.is_visible()
        pill1.click()
        print("8. Clicked suggestion pill 1 ('Explain current scenario').")

        # Wait for chat bubble to appear
        page.wait_for_selector(".chat-bubble-agent", timeout=15000)
        agent_bubbles = page.locator(".chat-bubble-agent").all()
        print(f"9. Agent chat responses received: {len(agent_bubbles)}")
        latest_reply = agent_bubbles[-1].inner_text()
        print(f"   Latest Copilot Response Preview: {latest_reply[:120]}...")

        # Screenshot Desktop
        page.screenshot(path="assets/screenshot_desktop_audit.png", full_page=False)
        print("10. Desktop screenshot saved to assets/screenshot_desktop_audit.png")

        context_desktop.close()

        # ======================================================================
        # Part 2: Mobile Viewport Audit (390x844)
        # ======================================================================
        print("\n=== Starting Mobile Viewport Audit (390x844) ===")
        context_mobile = browser.new_context(viewport={"width": 390, "height": 844})
        mobile_page = context_mobile.new_page()

        mobile_page.goto(
            "http://127.0.0.1:7860", wait_until="networkidle", timeout=30000
        )

        # 1. Zero horizontal overflow check
        scroll_width = mobile_page.evaluate("document.documentElement.scrollWidth")
        client_width = mobile_page.evaluate("window.innerWidth")
        print(
            f"1. Mobile Widths: clientWidth={client_width}px, scrollWidth={scroll_width}px"
        )
        assert scroll_width <= client_width + 1, (
            f"Horizontal overflow detected! scrollWidth ({scroll_width}) > clientWidth ({client_width})"
        )
        print("   Zero horizontal overflow verified (100% clean).")

        # 2. Literature scroll container constraint
        lit_scroll = mobile_page.locator(".investigation-list-scroll")
        assert lit_scroll.is_visible()
        computed_max_height = mobile_page.evaluate(
            "window.getComputedStyle(document.querySelector('.investigation-list-scroll')).maxHeight"
        )
        print(
            f"2. Literature Scroll Container Computed Max-Height: {computed_max_height}"
        )
        # Parse pixel value
        max_h_px = float(computed_max_height.replace("px", ""))
        assert max_h_px <= 420.0, f"max-height {max_h_px}px exceeds 420px limit"

        # 3. Mobile touch target compliance
        buttons = mobile_page.locator(
            "button, .btn, .pill-suggestion-btn, .nav-link-hud"
        ).all()
        checked_count = 0
        for btn in buttons[:10]:  # sample representative interactive elements
            box = btn.bounding_box()
            if box and box["width"] > 0 and box["height"] > 0:
                checked_count += 1
                assert box["height"] >= 38.0, (
                    f"Button height {box['height']}px below threshold"
                )
        print(
            f"3. Touch targets checked ({checked_count} controls): All meet mobile touch requirements."
        )

        # Screenshot Mobile
        mobile_page.screenshot(
            path="assets/screenshot_mobile_audit.png", full_page=False
        )
        print("4. Mobile screenshot saved to assets/screenshot_mobile_audit.png")

        context_mobile.close()
        browser.close()

    # Filter out any non-fatal warnings
    fatal_errors = [e for e in console_errors if "favicon" not in e.lower()]
    print(f"\nConsole Errors Count: {len(fatal_errors)}")
    if fatal_errors:
        print("Fatal errors:", fatal_errors)
    assert len(fatal_errors) == 0, f"Uncaught console errors detected: {fatal_errors}"

    print("\n=======================================================")
    print("ALL ACTIONS IN SLICE 7 AUDIT PASSED 100% SUCCESSFULLY!")
    print("=======================================================")


if __name__ == "__main__":
    run_audits()
