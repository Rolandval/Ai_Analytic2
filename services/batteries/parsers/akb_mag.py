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
    return f"https://akbmag.com.ua/ua/akkumulyatory/avtomobilnye/exide/fiamm/bosch/ista/rocket/topla/varta/page-{page}"


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
        url = "https://akbmag.com.ua/ua/akkumulyatory/avtomobilnye/exide/fiamm/bosch/ista/rocket/topla/varta/"
        html, _ = await fetch_html(session, url, 0)
        soup = BeautifulSoup(html, 'html.parser')
        pagination_div = soup.find("div", {
                "class": "row",
                "id": "pag5",
            })

        if not pagination_div:
            return 1

        results_divs = pagination_div.find_all("div", class_="col-sm-12 text-center")
        results_div = results_divs[-1].text.strip()
        # Шукаємо текст "всього X сторінок" і витягуємо число
        match = re.search(r'всього (\d+) сторінок', results_div)
        if match:
            return int(match.group(1))
        else:
            return 1


def extract_batteries_links_from_html(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    container = soup.find("div", {
                "class": "row",
                "id": "b_pag",
            })
    if not container:
        print("⚠️ Контейнер не знайдено")
        return []
    batteries = container.find_all("div", class_="fon_tov")
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
            
            battery_details = soup.find("table", {
                "class": "table table-striped",
            })
            price_div = soup.find("span", {
                "class": "autocalc-product-price",
            })
            name_lis = soup.find("ul", {
                "class": "breadcrumb",
            })

            if battery_details:
                # Видалення зайвих пробілів з тексту в таблиці
                for tag in battery_details.find_all(text=True):
                    if tag.strip():
                        tag.replace_with(tag.strip())
            return [name_lis, price_div, battery_details]
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
    filtered_results = [battery for battery in results if battery]
    
    # Визначаємо середину списку
    middle_index = len(filtered_results) // 2
    
    # Ділимо на дві рівні частини
    batteries_first = filtered_results[:middle_index]
    batteries_second = filtered_results[middle_index:]
    
    return [{"page_num": page_num, "batteries": batteries_first}, {"page_num": page_num + 100, "batteries": batteries_second}]



async def parse_batteries_akb_mag() -> List[str]:
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
                bateries_list = await extract_batteries_html(session, batteries_links, page_num)
                for batteries in bateries_list:
                    all_batteries.append(batteries)

    return all_batteries
        

# if __name__ == "__main__":
#     result = asyncio.run(parse_batteries_akb_mag())
#     print(result)
