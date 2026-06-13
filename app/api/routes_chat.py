# app/api/routes_chat.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from app.schemas.chat import ChatRequest, ChatResponse, MessagePublic
from app.usecases.chat import ChatUseCase
from app.core.errors import ExternalServiceError
from app.api.deps import get_chat_usecase, get_current_user_id

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """Отправка сообщения LLM и получение ответа"""
    try:
        answer = await chat_usecase.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            max_history=request.max_history,
            temperature=request.temperature,
        )
        return ChatResponse(answer=answer)
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e)
        )


@router.get("/history", response_model=list[MessagePublic])
async def get_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
    limit: int = 50,
):
    """Получение истории сообщений пользователя"""
    history = await chat_usecase.get_history(user_id, limit)
    return history

@router.delete("/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: Annotated[int, Depends(get_current_user_id)],
    chat_usecase: Annotated[ChatUseCase, Depends(get_chat_usecase)],
):
    """Очистка истории сообщений пользователя"""
    await chat_usecase.clear_history(user_id)