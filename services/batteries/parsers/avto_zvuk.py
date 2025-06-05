import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import sys
from typing import List, Tuple
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from helpers.get_user_agent import get_headers


def get_page_url(page: int) -> str:
    return f"https://avtozvuk.ua/ua/avtomobilnye-akkumulyatory/c300/5000=50109;5000=50507;5000=50623;5000=50643;5000=50766;5000=50833;5000=51044;5000=51056;5000=52020;5000=82099;5000=83457/page{page}/"


async def fetch_html(session: aiohttp.ClientSession, url: str, page_num: int) -> Tuple[str, int]:
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                print(f"✅ Завантажено сторінку {page_num} {url}")
                return html, page_num
            else:
                print(f"⚠️ Помилка {response.status} на сторінці {page_num} {url}")
                return "", page_num
    except Exception as e:
        print(f"❌ Помилка на сторінці {page_num}: {e}")
        return "", page_num


async def get_last_page() -> int:
    headers = get_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        url = "https://avtozvuk.ua/ua/avtomobilnye-akkumulyatory/c300/5000=50109;5000=50507;5000=50623;5000=50643;5000=50766;5000=50833;5000=51044;5000=51056;5000=52020;5000=82099;5000=83457"
        html, _ = await fetch_html(session, url, 0)
        soup = BeautifulSoup(html, 'html.parser')
        pagination_div = soup.find("div", class_="pagination load-more-pagination__pagination")

        if not pagination_div:
            return 1

        page_elements = pagination_div.find_all("div", class_="pagination__el")
        last_page = 1
        for element in page_elements:
            if 'data-page-num' in element.attrs:
                try:
                    page_num = int(element['data-page-num'])
                    last_page = max(last_page, page_num)
                except ValueError:
                    continue
        return last_page


def extract_batteries_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", class_="products-layout__products-list products-container")
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    batteries = container.find_all("div", class_="products-layout__product-item")
    batteries_links = []
    for battery in batteries:
        link_div = battery.find("div", class_="product-view-header__wrap-img")
        batteries_links.append(link_div.find("a")["href"])
    return batteries_links

async def fetch_battery_details(session: aiohttp.ClientSession, url: str):
    """
    Асинхронно отримує детальну інформацію про акумулятор за посиланням
    """
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"⚠️ Помилка {response.status} при отриманні деталей: {url}")
                return None
                
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            battery_details = soup.find("div", {
                "class": "aside-main-box",
                "id": "characteristics"
            })
            price_div = soup.find("div", {
                "class": "features-aside__price benefits-price",
            })
            return [price_div, battery_details]
    except Exception as e:
        print(f"❌ Помилка при отриманні деталей {url}: {e}")
        return None
            
            

async def extract_batteries_html(session: aiohttp.ClientSession, links: List[str], page_num: int):
    """
    Асинхронно отримує детальну інформацію про акумулятори за посиланнями
    """
    batteries = []
    base_url = "https://avtozvuk.ua"
    
    # Створюємо завдання для кожного посилання
    tasks = []
    for link in links:
        full_url = f"{base_url}{link}"
        tasks.append(fetch_battery_details(session, full_url))
    
    # Виконуємо всі завдання асинхронно
    results = await asyncio.gather(*tasks)
    
    # Фільтруємо результати, видаляючи None
    batteries = [battery for battery in results if battery]
    
    return {"page_num": page_num, "batteries": batteries}
        
    
    


async def parse_batteries_avto_zvuk() -> List[str]:
    headers = get_headers()
    last_page = await get_last_page()
    all_batteries = []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in range(1, last_page + 1):
            url = get_page_url(i)
            tasks.append(fetch_html(session, url, i))
            await asyncio.sleep(random.uniform(0.1, 0.3))  # антиспам-пауза

        results = await asyncio.gather(*tasks)

        for html, page_num in results:
            if html:
                batteries_links = extract_batteries_links_from_html(html)
                all_batteries.append(await extract_batteries_html(session, batteries_links, page_num))

    return all_batteries
        
# if __name__ == "__main__":
#     result = asyncio.run(parse_batteries())
#     print(result)
