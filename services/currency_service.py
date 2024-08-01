import os

import aiohttp
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import List, Dict

load_dotenv()


async def get_rates_monobank():
    url = 'https://api.monobank.ua/bank/currency'
    iso = {
        840: 'USD',
        978: 'EUR',
        980: 'UAH',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                currency_rates = []
                for item in data:
                    if item["currencyCodeA"] in iso.keys() and item["currencyCodeB"] == 980:
                        currency_rates.append(
                            {
                                'rate': f'{iso[item["currencyCodeA"]]}/{iso[item["currencyCodeB"]]}',
                                'buy': round(item['rateSell'], 2),
                                'sell': round(item['rateBuy'], 2),
                            }
                        )
                return currency_rates

            else:
                print(f"Error: Unable to fetch data (status code: {response.status})")
                return None


async def bestchange_session(rate: str, api_key: str, convert_rate=False):
    url = f'https://www.bestchange.app/v2/{api_key}/rates/{rate}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()

                rates = [float(r['rate']) for r in data['rates'][rate]]

                if convert_rate:
                    return round(1 / min(rates), 4)

                return round(min(rates), 4)

            else:
                print(f"Error: Unable to fetch data (status code: {response.status})")
                return None


async def get_rates_bestchange():
    api_key = os.getenv('BESTCHANCE_API_KEY')
    rates = [
        {
            'rate': 'USDT/UAH',
            'buy': await bestchange_session(
                rate='60-10',
                api_key=api_key,
            ),
            'sell': await bestchange_session(
                rate='10-60',
                api_key=api_key,
                convert_rate=True
            ),
        },
        {
            'rate': 'USDT/RUB',
            'buy': await bestchange_session(
                rate='59-10',
                api_key=api_key,
            ),
            'sell': await bestchange_session(
                rate='10-59',
                api_key=api_key,
                convert_rate=True
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


currency_cache = {}
cache_duration = timedelta(minutes=10)


async def collect_rates() -> Dict:
    now = datetime.utcnow()

    if 'data' in currency_cache and 'timestamp' in currency_cache:
        if now - currency_cache['timestamp'] < cache_duration:
            return currency_cache['data']

    data = {
        'monobank': await get_rates_monobank(),
        'bestchange': await get_rates_bestchange(),
        'binance': await get_rates_binance(),
    }

    currency_cache['data'] = data
    currency_cache['timestamp'] = now

    return data
