import argparse
import asyncio
import aiohttp
from datetime import datetime, timedelta


class CurrencyAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_url(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")
            return None

    async def get_exchange_rates(self, days):
        today = datetime.now()
        for day in range(days):
            date = (today - timedelta(days=day)).strftime('%d.%m.%Y')
            url = f"{self.base_url}?date={date}"
            response_data = await self.fetch_url(url)

            if response_data is not None:
                self.parse_responses(response_data, date)

    def parse_responses(self, response_data, date):
        exchange_rates = response_data.get('exchangeRate', [])
        rates = {'date': date}

        for rate in exchange_rates:
            currency = rate.get('currency', '')
            sale_rate = rate.get('saleRate', rate.get('saleRateNB', 'N/A'))
            purchase_rate = rate.get(
                'purchaseRate', rate.get('purchaseRateNB', 'N/A'))
            rates[currency] = {'sale': sale_rate, 'purchase': purchase_rate}

        print(rates)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch currency exchange rates")
    parser.add_argument("days", type=int, help="Number of days")
    args = parser.parse_args()

    print("Days:", args.days)

    api = CurrencyAPI()
    asyncio.run(api.get_exchange_rates(args.days))


if __name__ == "__main__":
    main()
