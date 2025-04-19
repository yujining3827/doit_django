import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json


def get_thumbnail_from_article(url):
    try:
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, 'html.parser')
        og_image = soup.select_one("meta[property='og:image']")
        if og_image:
            return og_image.get("content")
    except Exception as e:
        print(f"썸네일 가져오기 실패: {e}")
    return None

def crawl_hani_latest_with_selenium():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.get("https://www.hani.co.kr/arti")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = soup.select("a.BaseArticleCard_link__Q3YFK")

    #print("=== 한겨레 최신 뉴스 (제목 + 링크 + 이미지) ===")
    results = []
    seen = set()
    for article in articles:
        href = article.get("href", "")
        if href in seen or not href:
            continue
        seen.add(href)

        title_div = article.select_one("div.BaseArticleCard_title__TVFqt")
        if not title_div:
            continue

        title = title_div.text.strip()
        full_url = "https://www.hani.co.kr" + href

        image_url = get_thumbnail_from_article(full_url)

        results.append({
            "title": title,
            "url": full_url,
            "image": image_url
        })

        #print(f"{len(results)}. {title}\n   → {full_url}\n   🖼 {image_url}")

        if len(results) >= 10:
            break

    driver.quit()
    return results

if __name__ == "__main__":
    results = crawl_hani_latest_with_selenium()
    print(json.dumps(results, ensure_ascii=False))

crawl_hani_latest_with_selenium()
