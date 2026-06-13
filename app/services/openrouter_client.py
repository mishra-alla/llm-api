# app/services/openrouter_client.py
import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.site_url = settings.openrouter_site_url
        self.app_name = settings.openrouter_app_name

    async def chat_completion(self, messages: list[dict]) -> str:
        """Отправляет запрос к OpenRouter и возвращает ответ"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(f"OpenRouter API error: {e.response.status_code}")
            except httpx.RequestError as e:
                raise ExternalServiceError(f"OpenRouter request error: {str(e)}")