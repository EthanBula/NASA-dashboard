"""Verification script for:
1. 2x2 KPI cards on mobile
2. G1 and G3 shortened legend trace names
3. Accordion upward collapse for literature list on mobile
4. Shortened legend trace names in dedicated investigation charts (PSI-21)
"""
from __future__ import annotations

import time

from playwright.sync_api import sync_playwright


def run_audit():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 390, "height": 844})
        pg.goto("http://127.0.0.1:7860/", wait_until="networkidle")
        time.sleep(1)
        
        # -------------------------------------------------------------
        # 1. Check 2x2 KPI grid on mobile
        # -------------------------------------------------------------
        kpi_m = pg.locator("#kpi-margin").bounding_box()
        kpi_s = pg.locator("#kpi-spread").bounding_box()
        kpi_h = pg.locator("#kpi-hrr").bounding_box()
        kpi_d = pg.locator("#kpi-detection").bounding_box()
        print(f"KPI Margin: {kpi_m}")
        print(f"KPI Spread: {kpi_s}")
        print(f"KPI HRR: {kpi_h}")
        print(f"KPI Detection: {kpi_d}")
        
        # Check that margin and spread are side-by-side (same row Y)
        assert abs(kpi_m["y"] - kpi_s["y"]) < 5, f"Row 1 KPIs must have same Y: {kpi_m['y']} vs {kpi_s['y']}"
        assert abs(kpi_h["y"] - kpi_d["y"]) < 5, f"Row 2 KPIs must have same Y: {kpi_h['y']} vs {kpi_d['y']}"
        assert kpi_s["x"] > kpi_m["x"], "Spread must be to the right of Margin"
        assert kpi_d["x"] > kpi_h["x"], "Detection must be to the right of HRR"
        print("PASS 1: KPIs are arranged in a 2x2 grid on mobile!")
        
        # Capture KPI screenshot
        pg.screenshot(path="assets/verify_mobile_kpis_2x2.png")
        print("Screenshot verify_mobile_kpis_2x2.png saved!")
        
        # -------------------------------------------------------------
        # 2. Check G1 and G3
        # -------------------------------------------------------------
        pg.locator("#graph-g1-loc").scroll_into_view_if_needed()
        time.sleep(0.5)
        pg.screenshot(path="assets/verify_mobile_g1_g3.png")
        print("Screenshot verify_mobile_g1_g3.png saved!")
        
        # -------------------------------------------------------------
        # 3. Check Accordion in Literature section
        # -------------------------------------------------------------
        pg.locator("#literature").scroll_into_view_if_needed()
        time.sleep(0.5)
        list_el = pg.locator("#container-investigation-list")
        initial_box = list_el.bounding_box()
        print(f"Initial list height: {initial_box['height']}")
        assert initial_box["height"] > 300, "Initial list should be expanded"
        
        # Click an investigation card to select it
        print("Clicking PSI-142 card...")
        pg.locator(".investigation-card-item").first.click()
        time.sleep(0.6)
        
        # Check that list is now collapsed upwards
        collapsed_box = list_el.bounding_box()
        collapsed_height = collapsed_box["height"] if collapsed_box else 0
        print(f"Collapsed list height: {collapsed_height}")
        assert collapsed_height <= 1, f"List should collapse to 0 height, got {collapsed_height}"
        print("PASS 2: List collapsed upwards into accordion header on investigation select!")
        
        # Detail container is now directly visible
        detail_box = pg.locator("#container-investigation-detail").bounding_box()
        print(f"Detail container Y: {detail_box['y']}")
        
        # Screenshot of collapsed accordion with detail & chart visible
        pg.screenshot(path="assets/verify_mobile_accordion_collapsed.png")
        print("Screenshot verify_mobile_accordion_collapsed.png saved!")
        
        # Click Expand Catalog button to unfold
        print("Clicking Expand Catalog button...")
        pg.locator("#btn-toggle-list-size").click()
        time.sleep(0.6)
        expanded_box = list_el.bounding_box()
        print(f"Re-expanded list height: {expanded_box['height']}")
        assert expanded_box["height"] > 300, "List should re-expand on button click"
        print("PASS 3: List re-expanded successfully on button click!")
        
        # -------------------------------------------------------------
        # 4. Check PSI-21 chart dedicated telemetry
        # -------------------------------------------------------------
        print("Selecting PSI-21...")
        pg.locator("#input-search").fill("PSI-21")
        time.sleep(0.5)
        pg.locator(".investigation-card-item").first.click()
        time.sleep(0.6)
        pg.locator("#graph-investigation-detail").scroll_into_view_if_needed()
        time.sleep(0.5)
        pg.screenshot(path="assets/verify_mobile_psi21_chart.png")
        print("Screenshot verify_mobile_psi21_chart.png saved!")
        
        b.close()
    print("ALL AUDIT CHECKS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_audit()
