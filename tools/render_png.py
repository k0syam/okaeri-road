#!/usr/bin/env python3
"""assets/*.svg を PNG に書き出す（Playwright + Chromium）。

    pip install playwright && playwright install chromium   # 初回のみ
    python3 tools/render_png.py

日本語は Noto Sans CJK JP がインストールされている環境を想定（イラストはSVGなので絵文字フォントは不要）。
"""
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

# 出力サイズ（SVG の width に対する倍率）
SCALE = {
    "board_route_gauge.svg": 1,   # 1920×1080
    "quick_reference.svg": 1,     # 1080×2410
    "trump_cards_sheet.svg": 1,
}
CARD_SCALE = 2                    # 切り札カード：400×600 → 800×1200px
DEFAULT_SCALE = 3                 # コマ：200 → 600px


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for svg in sorted(ASSETS.glob("*.svg")) + sorted(ASSETS.glob("cards/*.svg")):
            src = svg.read_text(encoding="utf-8")
            w, h = (int(float(v)) for v in re.search(r'width="([\d.]+)" height="([\d.]+)"', src).groups())
            scale = CARD_SCALE if svg.parent.name == "cards" else SCALE.get(svg.name, DEFAULT_SCALE)
            page = browser.new_page(viewport={"width": w, "height": h}, device_scale_factor=scale)
            page.set_content(f'<html><body style="margin:0;background:transparent">{src}</body></html>')
            page.wait_for_timeout(200)
            page.locator("body > svg").screenshot(path=str(svg.with_suffix(".png")), omit_background=True)
            page.close()
            print(svg.with_suffix(".png").name, w * scale, h * scale)
        browser.close()


if __name__ == "__main__":
    main()
