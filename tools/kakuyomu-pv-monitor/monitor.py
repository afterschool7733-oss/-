#!/usr/bin/env python3
"""カクヨム公開画面の『詳細』から可視PVを読む試作。非公開APIや認証情報は使用しない。"""
import argparse
import asyncio
import csv
from datetime import datetime
from pathlib import Path
import re
from zoneinfo import ZoneInfo

URL = "https://kakuyomu.jp/works/11054822663706183433"
OUT = Path(__file__).resolve().parent / "data" / "pv_history.csv"
FIELDS = ["checked_at_jst", "work_url", "total_pv", "source", "note"]

def parse_pv(text):
    text = text.replace("ＰＶ", "PV").replace("，", ",")
    patterns = [
        r"(?:累計|総)?(?:アクセス数|閲覧数|PV)\s*[:：]?\s*([0-9][0-9,]*)\s*(?:PV)?\b",
        r"(?<!\w)([0-9][0-9,]*)\s*PV\b",
    ]
    found = {int(m.group(1).replace(",", "")) for p in patterns for m in re.finditer(p, text, re.I)}
    if len(found) != 1:
        raise RuntimeError("公開画面のPV表示を一意に読み取れません（候補: " + str(sorted(found)) + "）")
    return found.pop()

async def fetch_pv():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page(locale="ja-JP", timezone_id="Asia/Tokyo")
            response = await page.goto(URL, wait_until="domcontentloaded", timeout=45000)
            if not response or response.status >= 400:
                raise RuntimeError("カクヨムへのアクセスに失敗しました")
            try:
                await page.get_by_role("tab", name="詳細").click(timeout=5000)
            except Exception:
                await page.get_by_text("詳細", exact=True).first.click(timeout=6000)
            await page.wait_for_timeout(1200)
            return parse_pv(await page.locator("body").inner_text())
        finally:
            await browser.close()

def save(pv, source):
    today = datetime.now(ZoneInfo("Asia/Tokyo")).isoformat(timespec="seconds")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    exists = OUT.exists()
    if exists:
        with OUT.open(encoding="utf-8-sig", newline="") as f:
            rows = list(csv.DictReader(f))
        if any(row["checked_at_jst"].startswith(today[:10]) and row["source"] == source for row in rows):
            print(f"取得成功：{pv}PV。ただし同日の{source}データは既に存在するため追記しません")
            return
    with OUT.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, FIELDS)
        if not exists:
            writer.writeheader()
        writer.writerow(dict(checked_at_jst=today, work_url=URL, total_pv=pv, source=source, note=""))
    print(f"記録成功: {pv}PV / 残り {max(0, 10000-pv)}PV")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual-pv", type=int, help="取得せず確認済みの値を記録")
    args = parser.parse_args()
    pv = args.manual_pv if args.manual_pv is not None else asyncio.run(fetch_pv())
    if pv < 0:
        raise ValueError("PVは0以上")
    print(f"検出したPV：{pv}")
    save(pv, "user_reported" if args.manual_pv is not None else "public_detail_ui")
