import asyncio
import logging

from aiogram import Bot

from app.bot.dispatcher import dp
from app.config import settings
from app.infrastructure.db.engine import create_tables


async def main():
    logging.basicConfig(level=logging.INFO)

    await create_tables()

    bot = Bot(token=settings.BOT_TOKEN)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())