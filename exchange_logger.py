import aiofiles
from datetime import datetime


class CommandLogger:
    async def log_exchange_command(self, command):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"{timestamp}: Executed command '{command}'"
        async with aiofiles.open('exchange_log.txt', mode='a') as file:
            await file.write(log_line + '\n')
