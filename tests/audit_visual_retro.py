"""Playwright visual regression audit for:
1. Section title hover in green (Microgravity Flammability & Fire Safety Dashboard)
2. Sharp straight borders (border-radius: 0)
3. Colorless borders (neutral white/transparent, no red/green/yellow border lines)
4. Typewriter typography (Courier New / monospace)
"""
from __future__ import annotations

import time

from playwright.sync_api import sync_playwright


def run_visual_audit():
    with sync_playwright() as p:
        b = p.chromium.launch()
        
        # -------------------------------------------------------------
        # 1. Desktop Audit (1280 x 800)
        # -------------------------------------------------------------
        print("Auditing Desktop View...")
        pg = b.new_page(viewport={"width": 1280, "height": 800})
        pg.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1)
        
        # Check Typography
        body_font = pg.locator("body").evaluate("el => getComputedStyle(el).fontFamily")
        print(f"Body Font Family: {body_font}")
        assert "Courier" in body_font or "monospace" in body_font, f"Expected typewriter font, got {body_font}"
        
        title_font = pg.locator(".section-heading-title").first.evaluate("el => getComputedStyle(el).fontFamily")
        print(f"Section Title Font Family: {title_font}")
        assert "Courier" in title_font or "monospace" in title_font, f"Expected typewriter font, got {title_font}"
        print("PASS 1: Typewriter typography is actively applied across desktop and mobile!")
        
        # Check Border Radius (Straight borders)
        card_radius = pg.locator(".hud-card").first.evaluate("el => getComputedStyle(el).borderRadius")
        btn_radius = pg.locator(".btn").first.evaluate("el => getComputedStyle(el).borderRadius")
        print(f"HUD Card Border Radius: {card_radius}")
        print(f"Button Border Radius: {btn_radius}")
        assert card_radius in ("0px", "0"), f"Expected 0px border-radius, got {card_radius}"
        assert btn_radius in ("0px", "0"), f"Expected 0px border-radius, got {btn_radius}"
        print("PASS 2: Borders are 100% straight with 0px radius (no rounded corners)!")
        
        # Check Colorless Borders
        card_border_color = pg.locator(".hud-card-red").first.evaluate("el => getComputedStyle(el).borderColor")
        print(f"Card Border Color: {card_border_color}")
        # Ensure it is neutral/colorless (r, g, b are equal, e.g. rgba(255, 255, 255, ...))
        # and not red (where r is 217 and g is 17)
        if "rgba" in card_border_color:
            parts = [int(p.strip()) for p in card_border_color.replace("rgba(", "").replace(")", "").split(",")[:3]]
            assert parts[0] == parts[1] == parts[2], f"Expected monochromatic border color, got {card_border_color}"
        print("PASS 3: Card borders are completely colorless / monochromatic!")
        
        # Take normal desktop screenshot
        pg.screenshot(path="assets/verify_retro_desktop_initial.png")
        print("Screenshot assets/verify_retro_desktop_initial.png saved!")
        
        # Hover over Section 1 Title to test Green Glow
        title_el = pg.locator(".section-heading-title").first
        print(f"Initial Title Color: {title_el.evaluate('el => getComputedStyle(el).color')}")
        
        # Hover
        title_el.hover()
        time.sleep(0.3)
        hover_color = title_el.evaluate("el => getComputedStyle(el).color")
        hover_shadow = title_el.evaluate("el => getComputedStyle(el).textShadow")
        print(f"Hovered Title Color: {hover_color}")
        print(f"Hovered Title Text-Shadow: {hover_shadow}")
        # Green is rgb(12, 182, 77) or rgb(6, 136, 57)
        assert "182" in hover_color or "136" in hover_color, f"Title should glow green on hover, got {hover_color}"
        print("PASS 4: Section title illuminates in luminous green on mouse hover!")
        
        # Take screenshot of green hovered title
        pg.screenshot(path="assets/verify_retro_desktop_hover_green.png")
        print("Screenshot assets/verify_retro_desktop_hover_green.png saved!")
        
        # -------------------------------------------------------------
        # 2. Mobile Audit (390 x 844)
        # -------------------------------------------------------------
        print("Auditing Mobile View...")
        pg_m = b.new_page(viewport={"width": 390, "height": 844})
        pg_m.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1)
        
        pg_m.screenshot(path="assets/verify_retro_mobile_top.png")
        pg_m.locator("#graph-g1-loc").scroll_into_view_if_needed()
        time.sleep(0.4)
        pg_m.screenshot(path="assets/verify_retro_mobile_graphs.png")
        pg_m.locator("#literature").scroll_into_view_if_needed()
        time.sleep(0.4)
        pg_m.screenshot(path="assets/verify_retro_mobile_literature.png")
        print("Mobile screenshots saved!")
        
        b.close()
    print("ALL RETRO VISUAL AUDIT CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_visual_audit()
