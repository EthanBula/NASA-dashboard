"""Playwright verification script for sticky navbar, horizontal graph aspect ratio, and list density.
"""
from __future__ import annotations

import time

from playwright.sync_api import sync_playwright


def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # -------------------------------------------------------------
        # 1. Mobile Audit (390 x 844)
        # -------------------------------------------------------------
        print("Auditing mobile fixes (390x844)...")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1.5)
        
        # Test 1: Fixed Navbar on scroll
        print("Checking navbar at initial position...")
        nav_box = page.locator(".sticky-navbar").bounding_box()
        assert nav_box["y"] == 0, f"Initial navbar Y should be 0, got {nav_box['y']}"
        
        print("Scrolling down 1200px...")
        page.evaluate("window.scrollBy(0, 1200)")
        time.sleep(0.5)
        nav_box_scrolled = page.locator(".sticky-navbar").bounding_box()
        print(f"Navbar Y after 1200px scroll: {nav_box_scrolled['y']}")
        assert nav_box_scrolled["y"] == 0, f"Navbar must stay at Y=0 (fixed), got {nav_box_scrolled['y']}"
        print("PASS 1: Navbar is permanently fixed to top of viewport during scroll!")
        
        # Test 2: Horizontal Graph Height
        g1_card = page.locator("#graph-g1-loc").locator("xpath=..")
        g1_box = g1_card.bounding_box()
        print(f"G1 Card bounding box on mobile: width={g1_box['width']:.1f}px, height={g1_box['height']:.1f}px")
        # Aspect ratio: width / height
        aspect_ratio = g1_box['width'] / g1_box['height']
        print(f"G1 Card aspect ratio: {aspect_ratio:.2f} (Landscape > 1.3)")
        assert g1_box['height'] <= 235, f"Card height should be <= 235px, got {g1_box['height']}px"
        assert aspect_ratio >= 1.3, f"Card must be widescreen horizontal, got aspect ratio {aspect_ratio}"
        print("PASS 2: Graphs have genuine horizontal widescreen ratio (~16:9) on mobile!")
        
        # Test 3: Investigation List Density
        page.locator("#literature").scroll_into_view_if_needed()
        time.sleep(0.5)
        list_container = page.locator(".investigation-list-scroll")
        list_box = list_container.bounding_box()
        print(f"List container height: {list_box['height']}px")
        
        cards = page.locator(".investigation-card-item")
        total_cards = cards.count()
        print(f"Total investigation cards rendered: {total_cards}")
        
        # Count cards whose bounding boxes fall within the list container's visible vertical window
        visible_count = 0
        container_top = list_box['y']
        container_bottom = list_box['y'] + list_box['height']
        for i in range(total_cards):
            card_box = cards.nth(i).bounding_box()
            if card_box and card_box['y'] >= container_top - 10 and (card_box['y'] + card_box['height']) <= container_bottom + 10:
                visible_count += 1
                
        print(f"Simultaneously visible cards in mobile list view: {visible_count}")
        assert visible_count >= 5, f"Must show at least 5 cards at once, got {visible_count}"
        print(f"PASS 3: List displays {visible_count} investigations simultaneously (dense & legible)!")
        
        # Capture verification screenshots
        page.screenshot(path="assets/verify_mobile_fixed_navbar_scroll.png")
        page.locator("#graph-g1-loc").scroll_into_view_if_needed()
        time.sleep(0.3)
        page.screenshot(path="assets/verify_mobile_horizontal_graphs.png")
        page.locator(".investigation-list-scroll").scroll_into_view_if_needed()
        time.sleep(0.3)
        page.screenshot(path="assets/verify_mobile_dense_list.png")
        
        browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
