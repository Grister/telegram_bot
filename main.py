import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.db import init_db
from handlers import base, currency, notes, tasks

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(base.router)
    dp.include_router(notes.router)
    dp.include_router(currency.router)
    dp.include_router(tasks.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
