import aiohttp
from bs4 import BeautifulSoup
import hashlib
from fake_useragent import UserAgent

async def fetch_otodom():
    url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie?priceMax=200000&areaMin=30"
    listings = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": UserAgent().random}) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")
            for item in soup.select("article"):
                link_tag = item.find("a", href=True)
                if not link_tag:
                    continue
                link = link_tag["href"]
                title = item.get_text(strip=True)[:50]
                price = item.select_one("strong").get_text(strip=True) if item.select_one("strong") else "нет цены"
                hash_id = hashlib.md5(link.encode()).hexdigest()
                listings.append({
                    "title": title,
                    "price": price,
                    "location": "Polska",
                    "description": "Описание недоступно",
                    "url": link,
                    "image_url": None,
                    "hash": hash_id
                })
    return listings
