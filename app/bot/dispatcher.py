from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.middleware.db import DbMiddleware
from app.config import settings

dp = Dispatcher()

dp.update.middleware(DbMiddleware())

from app.handlers import start, main

dp.include_router(start.router)
dp.include_router(main.router)