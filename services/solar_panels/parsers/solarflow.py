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
    return f"https://solarflow.shop/soniachni-paneli-ta-batarei/"


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


def extract_sollar_panels_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", {
                "class": "catalog__content",
            })
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    solar_panels = container.find_all("li", {
                "class": "catalog-grid__item",
            })
    solar_panels_links = []
    for solar_panel in solar_panels:
        link_div = solar_panel.find("a")
        solar_panels_links.append(link_div["href"])
    return solar_panels_links


async def fetch_sollar_panel_details(session: aiohttp.ClientSession, url: str):
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
            
            solar_panel_details = soup.find("div", {
                "class": "product__section",
            })
            price_div = soup.find("div", {
                "class": "product-price__box",
            })
            name_lis = soup.find("div", {
                "class": "product-header",
            })

            if solar_panel_details:
                # Видалення зайвих пробілів з тексту в таблиці
                for tag in solar_panel_details.find_all(text=True):
                    if tag.strip():
                        tag.replace_with(tag.strip())
            return [name_lis, price_div, solar_panel_details]
    except Exception as e:
        print(f"❌ Помилка при отриманні деталей {url}: {e}")
        return None


async def extract_sollar_panels_html(session: aiohttp.ClientSession, links: List[str], page_num: int):
    """
    Асинхронно отримує детальну інформацію про сонячні панелі за посиланнями
    """
    sollar_panels = []
    base_link = "https://solarflow.shop"
    
    # Створюємо завдання для кожного посилання
    tasks = []
    for link in links:
        full_link = f"{base_link}{link}"
        tasks.append(fetch_sollar_panel_details(session, full_link))
    
    # Виконуємо всі завдання асинхронно
    results = await asyncio.gather(*tasks)
    
    # Фільтруємо результати, видаляючи None
    solar_panels = [sollar_panel for sollar_panel in results if sollar_panel]
    
    return {"page_num": page_num, "solar_panels": solar_panels}


async def parse_solar_panels_solarflow() -> List[str]:
    headers = get_headers()
    last_page = await get_last_page()
    all_sollar_panels = []

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for i in range(1, last_page + 1):
            url = get_page_url(i)
            tasks.append(fetch_html(session, url, i))
            await asyncio.sleep(random.uniform(2, 3))  # антиспам-пауза

        results = await asyncio.gather(*tasks)

        for html, page_num in results:
            if html:
                solar_panels_links = extract_sollar_panels_links_from_html(html)
                all_sollar_panels.append(await extract_sollar_panels_html(session, solar_panels_links, page_num))

    return all_sollar_panels



# if __name__ == "__main__":
#     result = asyncio.run(parse_sollar_panels_solarflow())
#     print(result)