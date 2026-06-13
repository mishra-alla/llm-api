# Построение защищённого API для работы с большой языковой моделью
(LLM API - FastAPI приложение с интеграцией OpenRouter)

## Цель работы:
Разработка серверного приложения на FastAPI, предоставляющего защищённый API для взаимодействия с большой языковой моделью (LLM) через сервис OpenRouter.
## Задача:
- реализовать аутентификацию и авторизацию пользователей с использованием JWT, хранение данных в базе SQLite,
- корректно разделить ответственность между слоями приложения (API, бизнес-логика, доступ к данным).

## Структура проекта
```
llm-p/
├── app/
│   ├── api/           # HTTP-слой (роутеры)
│   ├── core/          # Конфигурация, безопасность, ошибки
│   ├── db/            # База данных (модели, сессии)
│   ├── repositories/  # Слой доступа к данным
│   ├── schemas/       # Pydantic схемы
│   ├── services/      # Внешние сервисы (OpenRouter)
│   ├── usecases/      # Бизнес-логика
│   └── main.py        # Точка входа
├── screenshots/       # Скриншоты для документации
├── .env               # Конфигурация окружения
├── pyproject.toml     # Зависимости проекта
└── README.md          # Документация
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
# Демонстрация работы
1. Регистрация пользователя
Email должен быть в формате: student_surname@email.com

![Регистрация] (screenshots/01_registration.png)

2. Авторизация в Swagger
![Авторизация] (screenshots/02_auth_swagger.png)

3. Получение JWT токена
![Получение_JWT_токена] (screenshots/03_token.png)

4. Отправка запроса к LLM (POST /chat)
![Работа_чата] (screenshots/04_post_chat.png)

5. Получение истории диалога (GET /chat/history)
![История_диалога] (screenshots/05_get_history.png)

6. Очистка истории (DELETE /chat/history)
Удаление всей истории сообщений
![Очистка_истории] (screenshots/06_delete_history.png)

### Health check
```
curl http://localhost:8000/health
```
### Регистрация
```
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"mishra@email.com","password":"test123456"}'
```
### Логин
```
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=mishra@email.com&password=test123456"
  ```
### Отправка сообщения
```
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Расскажи о Python","max_history":10,"temperature":0.7}'
```

## Автор
Мишра Алла:  mishra-alla