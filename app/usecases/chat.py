# app/usecases/chat.py
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self, message_repo: ChatMessageRepository, llm_client: OpenRouterClient):
        self._message_repo = message_repo
        self._llm_client = llm_client

    async def ask(self, user_id: int, prompt: str, system: str | None, max_history: int, temperature: float) -> str:
        """Отправляет запрос к LLM и сохраняет историю"""
        
        # Формируем список сообщений для LLM
        messages = []
        
        # Добавляем system инструкцию если есть
        if system:
            messages.append({"role": "system", "content": system})
        
        # Получаем историю пользователя
        history = await self._message_repo.get_history(user_id, limit=max_history * 2)  # *2 потому что user+assistant
        
        # Добавляем историю в messages
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Добавляем текущий prompt
        messages.append({"role": "user", "content": prompt})
        
        # Сохраняем prompt пользователя в БД
        await self._message_repo.add_message(user_id, "user", prompt)
        
        # Отправляем запрос к LLM
        response = await self._llm_client.chat_completion(messages)
        
        # Сохраняем ответ ассистента в БД
        await self._message_repo.add_message(user_id, "assistant", response)
        
        return response

    async def get_history(self, user_id: int, limit: int = 50) -> list:
        """Получает историю сообщений пользователя"""
        return await self._message_repo.get_history(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        """Очищает историю сообщений пользователя"""
        await self._message_repo.clear_history(user_id)