import asyncio
import logging
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from database.db import init_db
from handlers.notes import router

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()


async def main():
    await init_db()

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
