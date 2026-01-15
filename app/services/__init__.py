import os
from pathlib import Path
from typing import List

from aiogram import Bot
from aiogram.types import FSInputFile


class ImageService:
    def __init__(self):
        self.images_dir = Path(".data/images")

    def get_ticket_images(self, ticket_number: int) -> List[FSInputFile]:
        """Получить все изображения для билета"""
        ticket_dir = self.images_dir / str(ticket_number)

        if not ticket_dir.exists():
            return []

        images = []
        for image_path in sorted(ticket_dir.glob("*")):
            if image_path.is_file() and not image_path.name.startswith("."):
                images.append(FSInputFile(image_path))

        return images

    async def send_ticket_images(self, bot: Bot, chat_id: int, ticket_number: int):
        """Отправить все изображения билета пользователю"""
        images = self.get_ticket_images(ticket_number)

        if not images:
            await bot.send_message(
                chat_id=chat_id,
                text=f"Извините, билет №{ticket_number} не найден."
            )
            return

        for image in images:
            await bot.send_photo(
                chat_id=chat_id,
                photo=image,
                caption=f"Билет №{ticket_number}"
            )