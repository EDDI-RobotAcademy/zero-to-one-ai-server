import re
import time
import json

import selenium.common
from fastapi import HTTPException
from typing import List

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


# TODO: Need to Refactor
def analyze_naver_shopping_product_url_and_get_html_list(product_url: str) -> List[str]:

    def get_number_of_reviews_registered(html: str) -> int:
        soup = BeautifulSoup(html, "html.parser")
        return int(soup
                   .find('div', {'class': 'J2bxvqM5w5'})
                   .find('span', {'class': 'sFI4W1erDx'}).get_text()
                   .replace(',', ''))

    html_list = []

    # selenium 옵션 설정
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')   # headless 로 실행시 동작 불가
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options,
                              service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(3)

    try:
        driver.get(product_url)
        time.sleep(2)

        # 전체 보기 클릭
        review_all_selector = '#content > div > div.Q1bBXdV7RJ > div.K38C2T0Ypx > div.wKQQf4o3UG > div > a'
        # TODO: 클릭 일부 안 되는 것은 어떻게 할 것인가?
        # brand 대부분) #content > div > div.Q1bBXdV7RJ > div.K38C2T0Ypx > div.wKQQf4o3UG > div > a
        # applestore) #content > div > div.ZgCvvTbvsN > div.K38C2T0Ypx > div.wKQQf4o3UG > div > a

        driver.find_element(By.CSS_SELECTOR, review_all_selector).click()
        time.sleep(1)

        initial_html = driver.page_source
        if initial_html:
            print(f'상품 URL 기반 HTML 로드 완료\n{initial_html}')

        # 전체 리뷰수 & 페이지 확인
        total_review_count = min(get_number_of_reviews_registered(initial_html), 100)  # 100개 제한
        total_review_pages = min(total_review_count // 20 + 1, 5)  # 100개 제한
        print(f'상품 리뷰 전체 개수 : {total_review_count}, 상품 리뷰 페이지 수 : {total_review_pages}')

        html_list.append(initial_html)

        for i in range(3, total_review_pages + 2):
            driver.find_element(
                By.CSS_SELECTOR,
                f'#REVIEW > div > div.JHZoCyHfg7 > div.HTT4L8U0CU > div > div > a:nth-child({i})'
            ).click()
            time.sleep(1)
            html_list.append(driver.page_source)

        return html_list

    except selenium.common.NoSuchElementException as not_found_error:
        raise HTTPException(status_code=500, detail=f"Element not found : {not_found_error}")

    except selenium.common.exceptions.ElementNotInteractableException as interaction_error:
        raise HTTPException(status_code=500, detail=f"Interaction failed: {interaction_error}")

    finally:
        driver.quit()

def parse_reviews_from_html_list(review_html_list: List[str]) -> dict:

    if not review_html_list:
        raise HTTPException(status_code=404, detail="Fail to load HTML from given URL")

    reviews_dict = {}
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

            reviews_dict[review_count] = review_content
            review_count += 1

    print(f'reviews: {reviews_dict}')
    return reviews_dict

def get_naver_shopping_product_reviews(product_url: str) -> dict:
    naver_shopping_product_review_html_list = analyze_naver_shopping_product_url_and_get_html_list(product_url)
    reviews_dictionary = parse_reviews_from_html_list(naver_shopping_product_review_html_list)
    return reviews_dictionary
