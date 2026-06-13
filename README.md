# Построение защищённого API для работы с большой языковой моделью
(LLM API - FastAPI приложение с интеграцией OpenRouter)

## Цель работы:
Разработка серверного приложения на FastAPI, предоставляющего защищённый API для взаимодействия с большой языковой моделью (LLM) через сервис OpenRouter.
## Задача:
- реализовать аутентификацию и авторизацию пользователей с использованием JWT, хранение данных в базе SQLite,
- корректно разделить ответственность между слоями приложения (API, бизнес-логика, доступ к данным).

## Структура проекта
```
llm_p/
├── pyproject.toml                 # Зависимости проекта (uv)
├── README.md                      # Описание проекта и запуск
├── .env.example                   # Пример переменных окружения
│
├── app/
│   ├── init.py
│   ├── main.py                    # Точка входа FastAPI
│   │
│   ├── core/                      # Общие компоненты и инфраструктура
│   │   ├── init.py
│   │   ├── config.py              # Конфигурация приложения (env → Settings)
│   │   ├── security.py            # JWT, хеширование паролей
│   │   └── errors.py              # Доменные исключения
│   │
│   ├── db/                        # Слой работы с БД
│   │   ├── init.py
│   │   ├── base.py                # DeclarativeBase
│   │   ├── session.py             # Async engine и sessionmaker
│   │   └── models.py              # ORM-модели (User, ChatMessage)
│   │
│   ├── schemas/                   # Pydantic-схемы (вход/выход API)
│   │   ├── init.py
│   │   ├── auth.py                # Регистрация, логин, токены
│   │   ├── user.py                # Публичная модель пользователя
│   │   └── chat.py                # Запросы и ответы LLM
│   │
│   ├── repositories/              # Репозитории (ТОЛЬКО SQL/ORM)
│   │   ├── init.py
│   │   ├── users.py               # Доступ к таблице users
│   │   └── chat_messages.py       # Доступ к истории чатов
│   │
│   ├── services/                  # Внешние сервисы
│   │   ├── init.py
│   │   └── openrouter_client.py   # Клиент OpenRouter / LLM
│   │
│   ├── usecases/                  # Бизнес-логика приложения
│   │   ├── init.py
│   │   ├── auth.py                # Регистрация, логин, профиль
│   │   └── chat.py                # Логика общения с LLM
│   │
│   └── api/                       # HTTP-слой (тонкие эндпоинты)
│       ├── init.py
│       ├── deps.py                # Dependency Injection
│       ├── routes_auth.py         # /auth/*
│       └── routes_chat.py         # /chat/*
│
└── app.db                         # SQLite база (создаётся при запуске)
```
## Технологии
- FastAPI
- SQLite + SQLAlchemy (async)
- JWT аутентификация
- OpenRouter API

## Установка и запуск

### Требования
- Python 3.12+
- uv package manager

### Установка
```
# Клонирование репозитория
git clone git@github.com:mishra-alla/llm-api.git
cd llm-api

# Создание виртуального окружения
uv venv --python 3.12
source .venv/bin/activate

# Установка зависимостей
uv pip install -r requirements.txt

# Настройка
# Создайте файл .env в корне проекта:

JWT_SECRET=your_secret_key_here
OPENROUTER_API_KEY=your_api_key_here

# Запуск
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Документация API
После запуска: http://localhost:8000/docs
```