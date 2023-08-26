import argparse
import asyncio
import aiohttp


class CurrencyAPI:
    def __init__(self):
        self.base_url = "https://api.privatbank.ua/p24api/exchange_rates"

    async def fetch_url(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()  # Raise an error if the response is not successful
                    return await response.json()
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")
            return None

    async def get_exchange_rates(self, days):
        url = f"{self.base_url}"
        response_data = await self.fetch_url(url)

        if response_data is not None:
            self.parse_responses(response_data, days)

    def parse_responses(self, response_data, days):
        # Here, you should parse the response data and extract the relevant information
        # You can access the JSON data using response_data['key'] notation
        exchange_rates = response_data.get('exchangeRates', [])

        # Placeholder: Example of filtering exchange rates for the last 'days' days
        filtered_rates = [
            rate for rate in exchange_rates if rate['date'] > days]

        self.format_exchange_rates(filtered_rates)

    def format_exchange_rates(self, exchange_rates):
        # Here, you should format the extracted exchange rates into the desired output
        # You can create a formatted string or print the information

        for rate in exchange_rates:
            print(
                f"Date: {rate['date']}, Currency: {rate['currency']}, Rate: {rate['rate']}")


def main():
    parser = argparse.ArgumentParser(
        description="Fetch currency exchange rates")
    parser.add_argument("days", type=int, help="Number of days")
    args = parser.parse_args()

    api = CurrencyAPI()
    asyncio.run(api.get_exchange_rates(args.days))


if __name__ == "__main__":
    main()
