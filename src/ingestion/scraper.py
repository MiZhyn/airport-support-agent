import json
import time
from pathlib import Path
from playwright.sync_api import sync_playwright
from pages_config import PAGES, BASE_URL
import random

# 保存路径
RAW_DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def scrape_detail_page(page, url, name, category):
    """爬取单个详细页的内容"""
    print(f"Scraping: {url}")
    page.goto(url, wait_until="networkidle")
    time.sleep(2)  # 等待动态内容加载

    # 提取页面标题
    title = page.title()

    # 提取正文内容
    content = page.inner_text("body")

    result = {
        "name": name,
        "category": category,
        "url": url,
        "title": title,
        "content": content
    }

    return result


def scrape_directory_page(page, url, name, category, seen_urls):
    print(f"Scraping directory: {url}")
    page.goto(url, wait_until="networkidle")
    page.wait_for_selector("div.facility-card", timeout=15000)
    time.sleep(random.uniform(2, 4))  # 随机等待2-4秒

    links = page.eval_on_selector_all(
        "a[href*='/facilities-and-services-directory/']",
        "elements => elements.map(el => ({href: el.href, text: el.innerText}))"
    )

    print(f"Found {len(links)} links in {name}")

    results = []
    for link in links:
        href = link["href"]
        link_name = link["text"].strip()
        if href and link_name and href not in seen_urls:
            seen_urls.add(href)
            time.sleep(random.uniform(1, 3))  # 每个请求之间随机等待
            detail = scrape_detail_page(page, href, link_name, category)
            results.append(detail)

    return results

def save_results(results, filename):
    """保存结果到JSON文件"""
    filepath = RAW_DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Saved to {filepath}")


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        seen_urls = set()  # ← 移到这里，所有category共享

        for page_config in PAGES:
            name = page_config["name"]
            url = page_config["url"]
            category = page_config["category"]
            scrape_type = page_config["scrape_type"]

            if scrape_type == "directory":
                results = scrape_directory_page(page, url, name, category, seen_urls)
                save_results(results, f"{name}.json")

            elif scrape_type == "detail":
                if url not in seen_urls:
                    seen_urls.add(url)
                    result = scrape_detail_page(page, url, name, category)
                    save_results([result], f"{name}.json")

        browser.close()
        print("Done!")


if __name__ == "__main__":
    main()