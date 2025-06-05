from bs4 import BeautifulSoup
import os
import sys
from typing import List, Tuple
import random
import requests
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from helpers.get_user_agent import get_headers



async def parse_batteries_aku_lviv():
    headers = get_headers()
    url = "https://aku.lviv.ua/"
    html = requests.get(url, headers=headers)
    if html.status_code != 200:
        raise Exception("Failed to fetch page")
    print(f"✅ Завантажено сторінку 1 {url}")
    soup = BeautifulSoup(html.text, 'html.parser')
    catalog = soup.find("div", class_="fm catalog")
    return [{"page_num": 1, "batteries": catalog}]


# if __name__ == "__main__":
#     print(asyncio.run(parse_batteries_aku_lviv()))
