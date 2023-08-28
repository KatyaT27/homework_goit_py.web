import asyncio
import aiohttp
import websockets

from currency_rates_console import CurrencyAPI


class CurrencyChat:
    async def handle_chat(self, websocket, path):
        async for message in websocket:
            await self.handle_chat_command(message, websocket)

    async def handle_chat_command(self, command, websocket):
        if command == "exchange":
            await self.show_current_exchange_rate(websocket)
        elif command.startswith("exchange "):
            _, days = command.split()
            days = int(days)
            await self.show_exchange_rates_for_days(websocket, days)

    async def show_current_exchange_rate(self, websocket):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{CurrencyAPI.BASE_URL}?exchange&coursid=5") as response:
                data = await response.json()
                current_rates = data[0]['exchangeRate']
                formatted_rates = self.format_current_rates(current_rates)
                await websocket.send(formatted_rates)

    def format_current_rates(self, rates):
        formatted = "Current exchange rates:\n"
        for rate in rates:
            formatted += f"{rate['currency']}: Sale {rate['saleRate']}, Purchase {rate['purchaseRate']}\n"
        return formatted

    async def show_exchange_rates_for_days(self, websocket, days):
        exchange_rates = await self.api.get_exchange_rates(days)
        formatted_rates = self.format_rates(exchange_rates)
        await websocket.send(formatted_rates)


async def main():
    async with websockets.serve(CurrencyChat().handle_chat, "localhost", 8765):
        await asyncio.Future()  # Keep the server running

if __name__ == "__main__":
    asyncio.run(main())
