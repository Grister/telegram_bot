import aiohttp

from typing import List, Dict
from bs4 import BeautifulSoup


async def get_rates_monobank() -> List:
    url = 'https://api.monobank.ua/bank/currency'
    iso = {
        840: 'USD',
        978: 'EUR',
        980: 'UAH',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            currency_rates = []
            for item in data:
                if item["currencyCodeA"] in iso.keys() and item["currencyCodeB"] == 980:
                    currency_rates.append(
                        {
                            'rate': f'{iso[item["currencyCodeA"]]}/{iso[item["currencyCodeB"]]}',
                            'buy': round(item['rateBuy'], 2),
                            'sell': round(item['rateSell'], 2),
                        }
                    )
            return currency_rates


async def bestchange_session(url, index):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                table = soup.find('table', {'id': 'content_table'})
                rows = table.find_all('td', {'class': 'bi'})

                rates = []
                for i in range(index, len(rows), 2):
                    rate = rows[i].text.split()[0]
                    rates.append(float(rate))

                return round(sum(rates[:5]) / 5, 2)

            else:
                print(f"Error: Unable to fetch data (status code: {response.status})")
                return None


async def get_rates_bestchange():
    rates = [
        {
            'rate': 'USDT/UAH',
            'buy': await bestchange_session(
                url='https://www.bestchange.ru/visa-mastercard-uah-to-tether-trc20.html',
                index=0
            ),
            'sell': await bestchange_session(
                url='https://www.bestchange.ru/tether-trc20-to-visa-mastercard-uah.html',
                index=1
            ),
        },
        {
            'rate': 'USDT/RUB',
            'buy': await bestchange_session(
                url='https://www.bestchange.ru/sberbank-to-tether-trc20.html',
                index=0
            ),
            'sell': await bestchange_session(
                url='https://www.bestchange.ru/tether-trc20-to-sberbank.html',
                index=1
            ),
        }]

    return rates


async def binance_session(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return round(float(data['price']), 4)


async def get_rates_binance():
    rates = [
        {
            'rate': 'BTC/USDT',
            'buy': await binance_session(
                url='https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
            ),
            'sell': '-'
        },
        {
            'rate': 'ETH/USDT',
            'buy': await binance_session(
                url='https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
            ),
            'sell': '-'
        }]
    return rates


async def collect_rates() -> Dict:
    result = {
        'monobank': await get_rates_monobank(),
        'bestchange': await get_rates_bestchange(),
        'binance': await get_rates_binance(),
    }

    return result
