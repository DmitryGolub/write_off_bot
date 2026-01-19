from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models import ExaminationTicket, User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, user_id: int, username: str | None = None) -> User:
        """Получить пользователя или создать нового если не существует"""
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            user = User(id=user_id, username=username)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user


class ExaminationTicketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_tickets(self) -> list[ExaminationTicket]:
        stmt = select(ExaminationTicket).order_by(ExaminationTicket.number)
        result = await self.session.execute(stmt)
        return list(result.scalars())
