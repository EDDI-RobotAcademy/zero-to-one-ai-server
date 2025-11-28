import re
import time
from datetime import datetime
from typing import Dict, List, Mapping, Any

import selenium.common
from fastapi import HTTPException
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

from product_review_collector.application.port.review_crawler_port import ReviewCrawlerPort


class NaverCrawlerAdapter(ReviewCrawlerPort):
    """네이버 쇼핑 리뷰를 Selenium으로 수집하는 collector 전용 어댑터."""

    async def fetch_reviews(self, product_url: str) -> Dict[Any, Any]:
        html_list = self._analyze_naver_shopping_product_url_and_get_html_list(product_url)
        return self._parse_reviews_from_html_list(html_list)

    def _build_driver(self, headless: bool) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--lang=ko-KR")
        options.add_argument("--remote-allow-origins=*")
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        options.add_experimental_option(
            "prefs",
            {
                "profile.managed_default_content_settings.images": 2,
            },
        )

        driver = webdriver.Chrome(
            options=options,
            service=Service(ChromeDriverManager().install()),
        )
        driver.implicitly_wait(3)
        return driver

    def _analyze_naver_shopping_product_url_and_get_html_list(self, product_url: str) -> List[str]:
        html_list: List[str] = []

        def get_number_of_reviews_registered(html: str) -> int:
            soup = BeautifulSoup(html, "html.parser")
            return int(
                soup
                .find('div', {'class': 'J2bxvqM5w5'})
                .find('span', {'class': 'sFI4W1erDx'}).get_text()
                .replace(',', '')
            )

        headless_preferred = True
        try:
            driver = self._build_driver(headless=headless_preferred)
        except WebDriverException:
            driver = self._build_driver(headless=False)

        wait = WebDriverWait(driver, 10)

        try:
            driver.get(product_url)
            time.sleep(2)

            review_all_selector = '#content > div > div.Q1bBXdV7RJ > div.K38C2T0Ypx > div.wKQQf4o3UG > div > a'

            review_all_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, review_all_selector))
            )
            driver.execute_script("arguments[0].click();", review_all_button)
            time.sleep(1)

            initial_html = driver.page_source
            if initial_html:
                print(f'상품 URL 기반 HTML 로드 완료\n{initial_html}')

            total_review_count = min(get_number_of_reviews_registered(initial_html), 100)
            total_review_pages = min(total_review_count // 20 + 1, 5)
            print(f'상품 리뷰 전체 개수 : {total_review_count}, 상품 리뷰 페이지 수 : {total_review_pages}')

            html_list.append(initial_html)

            for i in range(3, total_review_pages + 2):
                page_button = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.CSS_SELECTOR,
                            f'#REVIEW > div > div.JHZoCyHfg7 > div.HTT4L8U0CU > div > div > a:nth-child({i})',
                        )
                    )
                )
                driver.execute_script("arguments[0].click();", page_button)
                time.sleep(1)
                html_list.append(driver.page_source)

            return html_list

        except selenium.common.NoSuchElementException as not_found_error:
            raise HTTPException(status_code=500, detail=f"Element not found : {not_found_error}")

        except selenium.common.exceptions.ElementNotInteractableException as interaction_error:
            raise HTTPException(status_code=500, detail=f"Interaction failed: {interaction_error}")

        finally:
            driver.quit()

    @staticmethod
    def _extract_rating(review_item) -> float:
        rating_tag = review_item.select_one("div.uyBAhJxDVs em.n6zq2yy0KA")
        if not rating_tag:
            return 0.0
        try:
            return float(rating_tag.get_text().strip())
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _extract_created_at(review_item) -> datetime | None:
        date_tag = review_item.select_one("div.uyBAhJxDVs span.MX91DFZo2F")
        if not date_tag:
            return None
        raw = date_tag.get_text().strip().rstrip(".")
        try:
            parsed = datetime.strptime(raw, "%y.%m.%d")
            print(f"[collector-debug] parsed date: {parsed}")
            return parsed
        except ValueError:
            print(f"[collector-debug] date parse failed for: {raw}")
            return None

    @staticmethod
    def _extract_writer(review_item) -> str | None:
        writer_tag = review_item.select_one("div.Db9Dtnf7gY strong.MX91DFZo2F")
        if not writer_tag:
            return None
        writer = writer_tag.get_text().strip()
        print(f"[collector-debug] writer raw: {writer}")
        return writer or None

    def _parse_reviews_from_html_list(self, review_html_list: List[str]) -> Dict[int, Mapping[str, Any]]:
        if not review_html_list:
            raise HTTPException(status_code=404, detail="Fail to load HTML from given URL")

        reviews_dict: Dict[int, Mapping[str, Any]] = {}
        review_count = 1

        for review_html in review_html_list:
            soup = BeautifulSoup(review_html, "html.parser")
            review_items = soup.findAll('li', {'class': "PxsZltB5tV _nlog_click _nlog_impression_element"})

            for review in range(len(review_items)):
                review_content_raw = (
                    review_items[review]
                    .findAll('div', {'class': 'KqJ8Qqw082'})[0]
                    .find('span', {'class': 'MX91DFZo2F'}).get_text())
                review_content = re.sub(' +', ' ', re.sub('\n', ' ', review_content_raw))
                rating = self._extract_rating(review_items[review])
                created_at = self._extract_created_at(review_items[review])
                writer = self._extract_writer(review_items[review])

                reviews_dict[review_count] = {
                    "content": review_content,
                    "rating": rating,
                    "created_at": created_at,
                    "review_writer": writer,
                }
                review_count += 1

        print(f'reviews: {reviews_dict}')
        return reviews_dict
