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
    return f"https://dviklemy.com.ua/avtomobilni/filter/brand-bosch-or-exide-or-fiamm-or-inter-or-ista-or-platin-or-topla-or-varta-or-westa?utm_source=google&utm_medium=cpc&utm_campaign=search_akumulyatory_dlya_avto&utm_content=&utm_term=&gad_source=1&gbraid=0AAAAAp6FrgpN4ij8iJvErj1xPj5i3gqZS&gclid=Cj0KCQjww-HABhCGARIsALLO6Xx0m_YJ8ag2PWNGMCbToQcN8UtitmNk4UifhIl-0KD5LS32IEtELeMaAjECEALw_wcB&page={page}"

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
        url = "https://dviklemy.com.ua/avtomobilni/filter/brand-bosch-or-exide-or-fiamm-or-inter-or-ista-or-platin-or-topla-or-varta-or-westa?utm_source=google&utm_medium=cpc&utm_campaign=search_akumulyatory_dlya_avto&utm_content=&utm_term=&gad_source=1&gbraid=0AAAAAp6FrgpN4ij8iJvErj1xPj5i3gqZS&gclid=Cj0KCQjww-HABhCGARIsALLO6Xx0m_YJ8ag2PWNGMCbToQcN8UtitmNk4UifhIl-0KD5LS32IEtELeMaAjECEALw_wcB&page=1"
        html, _ = await fetch_html(session, url, 0)
        soup = BeautifulSoup(html, 'html.parser')
        pagination_ul = soup.find("ul", class_="pagination")

        if not pagination_ul:
            return 1

        pagination_lis = pagination_ul.find_all("li")
        pagination_li = pagination_lis[-2]
        last_page = pagination_li.find("a").text.strip()
        return int(last_page)


def extract_batteries_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", class_="catalog-list-more catalog-list load-more-target")
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    batteries = container.find_all("div", class_="product-card-wrapper")
    batteries_links = []
    for battery in batteries:
        link_div = battery.find("a")
        batteries_links.append(link_div["href"])
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
                "id": "characteristic-acc",
                "class": "collapse show"
            })

            price_div = soup.find("span", {
                "class": "price-value"
            })
            name_div = soup.find("h1", {
                "class": "page-title"
            })
            
            return [name_div, price_div, battery_details]
    except Exception as e:
        print(f"❌ Помилка при отриманні деталей {url}: {e}")
        return None

async def extract_batteries_html(session: aiohttp.ClientSession, links: List[str], page_num: int):
    """
    Асинхронно отримує детальну інформацію про акумулятори за посиланнями
    """
    batteries = []
    
    # Створюємо завдання для кожного посилання
    tasks = []
    for link in links:
        tasks.append(fetch_battery_details(session, link))
    
    # Виконуємо всі завдання асинхронно
    results = await asyncio.gather(*tasks)
    
    # Фільтруємо результати, видаляючи None
    batteries = [battery for battery in results if battery]
    
    return {"page_num": page_num, "batteries": batteries}

async def parse_batteries_dvi_klemy() -> List[str]:
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



if __name__ == "__main__":
    last_page = asyncio.run(parse_batteries_dvi_klemy())
    print(last_page)