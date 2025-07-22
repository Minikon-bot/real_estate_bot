import httpx
from bs4 import BeautifulSoup

OTODOM_URL = "https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow"

def parse_otodom():
    response = httpx.get(OTODOM_URL, timeout=10.0)
    soup = BeautifulSoup(response.text, "html.parser")

    listings = []
    for listing in soup.select("li[data-cy='search-result-item']")[:3]:
        title = listing.select_one("p[data-cy='listing-item-title']").text.strip()
        price = listing.select_one("span[data-testid='price']").text.strip()
        link = "https://www.otodom.pl" + listing.select_one("a")["href"]
        listings.append(f"{title}\n{price}\n{link}")
    
    return listings
