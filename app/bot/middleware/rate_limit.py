import time
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject


class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = 10):
        self.cooldown_seconds = cooldown_seconds
        self.user_last_request: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        current_time = time.time()

        if user_id in self.user_last_request:
            time_since_last = current_time - self.user_last_request[user_id]
            
            if time_since_last < self.cooldown_seconds:
                remaining_time = int(self.cooldown_seconds - time_since_last)
                await event.answer(
                    f"⏳ Пожалуйста, подождите {remaining_time} секунд перед следующим запросом."
                )
                return

        self.user_last_request[user_id] = current_time
        return await handler(event, data)