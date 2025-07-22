import requests
from bs4 import BeautifulSoup

def parse_otodom():
    url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    offers = []

    # Пример: парсим названия и ссылки первых 5 объявлений
    for offer_div in soup.select("div.offer-item-details")[:5]:
        title_tag = offer_div.select_one("a.offer-item-title")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = "https://www.otodom.pl" + title_tag['href']
            offers.append(f"{title}\n{link}")

    return offers
