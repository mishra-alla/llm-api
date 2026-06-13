# app/usecases/auth.py
from app.repositories.users import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.core.errors import ConflictError, UnauthorizedError


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def register(self, email: str, password: str):
        """Регистрация нового пользователя"""
        # Проверяем, не занят ли email
        existing_user = await self._user_repo.get_by_email(email)
        if existing_user:
            raise ConflictError("Email already registered")

        # Создаем пользователя
        password_hash = hash_password(password)
        user = await self._user_repo.create(email, password_hash)
        return user

    async def login(self, email: str, password: str) -> str:
        """Логин пользователя и выдача токена"""
        # Находим пользователя
        user = await self._user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Invalid email or password")

        # Проверяем пароль
        if not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        # Создаем токен
        token = create_access_token(user.id, user.role)
        return token

    async def get_profile(self, user_id: int):
        """Получение профиля пользователя"""
        user = await self._user_repo.get_by_id(user_id)
        return user