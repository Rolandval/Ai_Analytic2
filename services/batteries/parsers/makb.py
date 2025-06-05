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
    if page == 1:
        return "https://makb.com.ua/akkumuliatory-legkovye/brand-bosch-or-exide-or-fiamm-or-platin-or-plazma-or-rocket-or-varta-or-westa"
    page_num = (page - 1) * 24
    return f"https://makb.com.ua/akkumuliatory-legkovye/brand-bosch-or-exide-or-fiamm-or-platin-or-plazma-or-rocket-or-varta-or-westa?per_page={page_num}"


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
        url = "https://makb.com.ua/akkumuliatory-legkovye/brand-bosch-or-exide-or-fiamm-or-platin-or-plazma-or-rocket-or-varta-or-westa"
        html, _ = await fetch_html(session, url, 0)
        soup = BeautifulSoup(html, 'html.parser')
        pagination_div = soup.find("div", class_="content__pagination")

        if not pagination_div:
            return 1

        last_element = pagination_div.find("li", class_="paginator__item paginator__item--last")
        last_page = last_element.find("a").text.strip()
        last_page_text = ''.join(c for c in last_page if c.isdigit())
        return int(last_page_text)

def extract_batteries_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", class_="col-sm-8 col-md-9")
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    batteries = container.find_all("div", class_="col-xs-6 col-sm-6 col-md-4 col-lg-3")
    batteries_links = []
    for battery in batteries:
        link_div = battery.find("a", class_="product-cut__title-link")
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
            
            battery_details = ""
            battery_details_div = soup.find("div", class_="product-fullinfo")
            divs = battery_details_div.find_all("div", class_="product-fullinfo__item")
            for div in divs:
                o = div.find("div", class_="product-fullinfo__title")
                if o:
                    properties = div.find("div", class_="properties")
                    battery_details = properties


            price_div = soup.find("div", {
                "class": "product-intro__price"
            })
            name_div = soup.find("div", {
                "class": "content__header content__header--xs"
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

async def parse_batteries_makb() -> List[str]:
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
#     last_page = asyncio.run(parse_batteries_makb())
#     print(last_page)
