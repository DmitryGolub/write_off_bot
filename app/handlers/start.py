from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repo import UserRepository

router = Router()


@router.message(CommandStart())
async def start_command(message: types.Message, session: AsyncSession):
    user_repo = UserRepository(session)
    user = await user_repo.get_or_create_user(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await message.reply(
        "Привет! 👋\n\n"
        "Это бот для списывания выш мата.\n"
        "Пришли мне число от 1 до 30 и я пришлю тебе решенный билет!\n"
        "Список билетов (номер билета и первое задание): /list"
    )
