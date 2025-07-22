import requests
from bs4 import BeautifulSoup

def check_new_ads():
    url = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa"  # Замените на ваш URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Замените на вашу логику парсинга
        ads = []  # Пример: список объявлений
        # Пример: ads = [ad.text for ad in soup.find_all('div', class_='offer-item')]
        return ads
    except requests.RequestException as e:
        print(f"Ошибка при запросе к Otodom: {e}")
        return []