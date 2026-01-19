import time
from typing import Dict

from aiogram import Router, types, Bot
from aiogram.filters import Command, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repo import ExaminationTicketRepository
from app.services import ImageService

router = Router()
image_service = ImageService()
user_last_request: Dict[int, float] = {}
COOLDOWN_SECONDS = 3


@router.message(Command("list"))
async def search_by_first_task(message: types.Message, session: AsyncSession):
    repo = ExaminationTicketRepository(session)
    tickets = await repo.list_tickets()

    if not tickets:
        await message.reply("Список билетов пуст.")
        return

    lines = [
        f"{ticket.number}. {ticket.description_first_task}"
        for ticket in sorted(tickets, key=lambda t: t.number)
    ]
    text = "\n".join(lines)

    await message.reply(text)


@router.message(StateFilter(None))
async def handle_ticket_number(message: types.Message, bot: Bot):
    """Обработчик чисел от 1 до 30"""
    text = message.text.strip()

    if not text.isdigit():
        return

    ticket_number = int(text)

    if not (1 <= ticket_number <= 30):
        await message.reply(
            "Пожалуйста, введите число от 1 до 30 включительно."
        )
        return

    user_id = message.from_user.id
    current_time = time.time()

    if user_id in user_last_request:
        time_since_last = current_time - user_last_request[user_id]

        if time_since_last < COOLDOWN_SECONDS:
            remaining_time = int(COOLDOWN_SECONDS - time_since_last)
            await message.answer(
                f"⏳ Пожалуйста, подождите {remaining_time} секунд перед следующим запросом билета."
            )
            return

    user_last_request[user_id] = current_time

    await image_service.send_ticket_images(
        bot=bot,
        chat_id=message.chat.id,
        ticket_number=ticket_number
    )
