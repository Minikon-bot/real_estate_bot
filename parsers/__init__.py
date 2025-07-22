from .otodom_parser import fetch_otodom
from .olx_parser import fetch_olx
from .gratka_parser import fetch_gratka
from .morizon_parser import fetch_morizon
from .nieruchomosci_parser import fetch_nieruchomosci

async def fetch_all():
    results = []
    for func in [fetch_otodom, fetch_olx, fetch_gratka, fetch_morizon, fetch_nieruchomosci]:
        try:
            results.extend(await func())
        except Exception as e:
            print(f"Ошибка парсера {func.__name__}: {e}")
    return results
