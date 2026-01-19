import re
import time
from typing import Dict

from aiogram import F, Router, types, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.repo import ExaminationTicketRepository
from app.services import ImageService

router = Router()
image_service = ImageService()
user_last_request: Dict[int, float] = {}
COOLDOWN_SECONDS = 3


class SearchByFirstTask(StatesGroup):
    waiting_for_text = State()


def normalize_search_tokens(value: str) -> list[str]:
    text = value.casefold().replace("ё", "е").replace("π", "pi")
    text = re.sub(r"[^a-zа-я0-9]+", " ", text)
    return [token for token in text.split() if len(token) > 1]


def tokens_match(query_tokens: list[str], target_tokens: list[str]) -> bool:
    if not query_tokens:
        return False
    for token in query_tokens:
        if not any(token in target for target in target_tokens):
            return False
    return True


@router.message(Command("search_by_first_task"))
async def search_by_first_task(message: types.Message, state: FSMContext):
    await state.set_state(SearchByFirstTask.waiting_for_text)
    await message.reply(
        "Введите описание первого задания для поиска билета"
    )


@router.message(SearchByFirstTask.waiting_for_text, F.text & ~F.text.startswith("/"))
async def handle_first_task_search(
    message: types.Message,
    bot: Bot,
    session: AsyncSession,
    state: FSMContext,
):
    text = (message.text or "").strip()
    if not text:
        await state.clear()
        return

    await state.clear()
    query_tokens = normalize_search_tokens(text)
    if not query_tokens:
        await message.reply(
            "Пожалуйста, введите описание первого задания текстом."
        )
        return

    repo = ExaminationTicketRepository(session)
    tickets = await repo.list_tickets()
    matches = [
        ticket.number
        for ticket in tickets
        if tokens_match(
            query_tokens,
            normalize_search_tokens(ticket.description_first_task),
        )
    ]

    if not matches:
        await message.reply(
            f"билет с описанием первого задания ({text.lower()}) не найден"
        )
        return

    if len(matches) > 1:
        numbers = ", ".join(str(number) for number in sorted(matches))
        await message.reply(
            "По вашему запросу нашлось несколько билетов: "
            f"{numbers}. Вы можете ввести запрос повторно "
            "/search_by_first_task"
        )
        return

    await image_service.send_ticket_images(
        bot=bot,
        chat_id=message.chat.id,
        ticket_number=matches[0],
    )


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
