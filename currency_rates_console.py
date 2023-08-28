import argparse
import aiohttp
import asyncio
from datetime import datetime, timedelta


class CurrencyAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_exchange_rates(self, date):
        url = f"{self.base_url}?date={date}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_data = await response.json()
                return response_data.get('exchangeRate', [])

    async def get_currency_rates(self, date, currencies):
        exchange_rates = await self.fetch_exchange_rates(date)
        rates = {}

        for rate in exchange_rates:
            currency = rate.get('currency')
            if currency in currencies:
                rates[currency] = {
                    'sale': rate.get('saleRate'),
                    'purchase': rate.get('purchaseRate')
                }

        return rates


async def main():
    parser = argparse.ArgumentParser(
        description="Fetch currency exchange rates")
    parser.add_argument("date", type=str, help="Date in the format DD.MM.YYYY")
    args = parser.parse_args()

    date = datetime.strptime(args.date, '%d.%m.%Y')
    api = CurrencyAPI()
    currencies = ['EUR', 'USD']  # Add more currencies if needed
    rates = await api.get_currency_rates(date.strftime('%d.%m.%Y'), currencies)

    for currency, rate_info in rates.items():
        print(
            f"{currency}: Sale - {rate_info['sale']}, Purchase - {rate_info['purchase']}")

if __name__ == "__main__":
    asyncio.run(main())
