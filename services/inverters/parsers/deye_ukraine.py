import asyncio
import aiohttp
from bs4 import BeautifulSoup
import os
import sys
from typing import List, Tuple
import random
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from helpers.get_user_agent import get_headers



def get_page_url(page: int) -> str:
    return f"https://www.deye-ukraine.com.ua/category/hybridinverter"


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
    return 1


def extract_inverters_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("section", {
                "data-hook": "product-list",
            })
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    inverters = container.find_all("li")
    inverters_links = []
    for inverter in inverters:
        link_div = inverter.find("a")
        inverters_links.append(link_div["href"])
    return inverters_links

async def fetch_inverter_details(session: aiohttp.ClientSession, url: str):
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
            
            inverter_details = soup.find("div", {
                "data-hook": "info-section-description",
            })
            price_div = soup.find("div", {
                "data-hook": "product-price",
            })
            name_lis = soup.find("h1", {
                "data-hook": "product-title",
            })

            if inverter_details:
                # Видалення зайвих пробілів з тексту в таблиці
                for tag in inverter_details.find_all(text=True):
                    if tag.strip():
                        tag.replace_with(tag.strip())
            return [name_lis, price_div, inverter_details]
    except Exception as e:
        print(f"❌ Помилка при отриманні деталей {url}: {e}")
        return None


async def extract_inverters_html(session: aiohttp.ClientSession, links: List[str], page_num: int):
    """
    Асинхронно отримує детальну інформацію про сонячні панелі за посиланнями
    """
    inverters = []
    
    # Створюємо завдання для кожного посилання
    tasks = []
    for link in links:
        tasks.append(fetch_inverter_details(session, link))
    
    # Виконуємо всі завдання асинхронно
    results = await asyncio.gather(*tasks)
    
    # Фільтруємо результати, видаляючи None
    inverters = [inverter for inverter in results if inverter]
    
    return {"page_num": page_num, "inverters": inverters}


async def parse_inverters_deye_ukraine() -> List[str]:
    headers = get_headers()
    last_page = await get_last_page()
    all_inverters = []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in range(1, last_page + 1):
            url = get_page_url(i)
            tasks.append(fetch_html(session, url, i))
            await asyncio.sleep(random.uniform(5, 10))  # антиспам-пауза

        results = await asyncio.gather(*tasks)

        for html, page_num in results:
            if html:
                inverters_links = extract_inverters_links_from_html(html)
                all_inverters.append(await extract_inverters_html(session, inverters_links, page_num))

    return all_inverters


# if __name__ == "__main__":
#     result = asyncio.run(parse_inverters_deye_ukraine())
#     print(result)