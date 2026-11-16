"""Playwright audit script to verify mobile and desktop layouts for HUD improvements.
"""
from __future__ import annotations

import time
from playwright.sync_api import sync_playwright

def run_audit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # 1. Mobile Audit (390 x 844)
        print("Auditing mobile viewport (390x844)...")
        mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
        mobile_page.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1.5)
        
        # Capture mobile navbar
        mobile_page.screenshot(path="assets/verify_mobile_navbar.png")
        print("Captured assets/verify_mobile_navbar.png")
        
        # Scroll to Section 1 Graphs
        g1 = mobile_page.locator("#graph-g1-loc")
        g1.scroll_into_view_if_needed()
        time.sleep(0.5)
        mobile_page.screenshot(path="assets/verify_mobile_section1_graphs.png")
        print("Captured assets/verify_mobile_section1_graphs.png")
        
        # Scroll to Section 2 Literature
        lit = mobile_page.locator("#literature")
        lit.scroll_into_view_if_needed()
        time.sleep(0.5)
        mobile_page.screenshot(path="assets/verify_mobile_section2_order.png")
        print("Captured assets/verify_mobile_section2_order.png")
        
        # Check order of Section 2 elements
        filters_box = mobile_page.locator(".hud-lit-filters").bounding_box()
        list_box = mobile_page.locator(".hud-lit-list").bounding_box()
        detail_box = mobile_page.locator(".hud-lit-detail").bounding_box()
        chart_box = mobile_page.locator(".hud-lit-chart").bounding_box()
        
        print(f"Mobile Y positions: Filters={filters_box['y']}, List={list_box['y']}, Detail={detail_box['y']}, Chart={chart_box['y']}")
        assert filters_box['y'] < list_box['y'], "Filters must appear above List on mobile!"
        assert list_box['y'] < detail_box['y'], "List must appear above Detail on mobile!"
        assert detail_box['y'] < chart_box['y'], "Detail must appear above Chart on mobile!"
        print("PASS: Mobile Section 2 stacking order is strictly: Filters -> List -> Detail -> Chart!")
        
        # Scroll to Section 3 Chatbot
        agent = mobile_page.locator("#agent")
        agent.scroll_into_view_if_needed()
        time.sleep(0.5)
        mobile_page.screenshot(path="assets/verify_mobile_section3_chatbot.png")
        print("Captured assets/verify_mobile_section3_chatbot.png")
        
        # Verify pill-3 does not exist
        pill3 = mobile_page.locator("#pill-3")
        assert pill3.count() == 0, "pill-3 must be completely removed!"
        print("PASS: pill-3 is completely removed.")
        
        # 2. Desktop Audit (1400 x 900)
        print("Auditing desktop viewport (1400x900)...")
        desktop_page = browser.new_page(viewport={"width": 1400, "height": 900})
        desktop_page.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1.5)
        desktop_page.screenshot(path="assets/verify_desktop_full.png")
        print("Captured assets/verify_desktop_full.png")
        
        browser.close()
        print("All mobile and desktop audits passed successfully!")

if __name__ == "__main__":
    run_audit()

