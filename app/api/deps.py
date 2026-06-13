# app/api/deps.py
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_token
from app.core.errors import UnauthorizedError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_session() -> AsyncSession:
    """Dependency для получения сессии БД"""
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_repo(session: Annotated[AsyncSession, Depends(get_session)]) -> UserRepository:
    return UserRepository(session)


async def get_message_repo(session: Annotated[AsyncSession, Depends(get_session)]) -> ChatMessageRepository:
    return ChatMessageRepository(session)


async def get_llm_client() -> OpenRouterClient:
    return OpenRouterClient()


async def get_auth_usecase(
    user_repo: Annotated[UserRepository, Depends(get_user_repo)]
) -> AuthUseCase:
    return AuthUseCase(user_repo)


async def get_chat_usecase(
    message_repo: Annotated[ChatMessageRepository, Depends(get_message_repo)],
    llm_client: Annotated[OpenRouterClient, Depends(get_llm_client)],
) -> ChatUseCase:
    return ChatUseCase(message_repo, llm_client)


async def get_current_user_id(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> int:
    """Получает ID текущего пользователя из JWT токена"""
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        if not user_id:
            raise UnauthorizedError("Invalid token")
        return user_id
    except (ValueError, UnauthorizedError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )