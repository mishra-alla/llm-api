# app/repositories/chat_messages.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.db.models import ChatMessage


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Добавляет сообщение в историю"""
        message = ChatMessage(user_id=user_id, role=role, content=content)
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        """Получает историю сообщений пользователя"""
        result = await self._session.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at)
            .limit(limit)
        )
        return result.scalars().all()

    async def clear_history(self, user_id: int) -> None:
        """Очищает историю сообщений пользователя"""
        await self._session.execute(
            delete(ChatMessage).where(ChatMessage.user_id == user_id)
        )
        await self._session.commit()