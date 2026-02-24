# РЕПОЗИТОРИЙ - https://github.com/tramori21/Auth_sprint1_team1

# Auth Service (Sprint 6)

Сервис авторизации и управления ролями на FastAPI.

## Реализованный функционал

- Регистрация пользователя (signup)
- Авторизация (login, JWT access + refresh)
- Обновление access-токена (refresh с ротацией)
- Выход из аккаунта (logout)
- История входов пользователя
- Смена пароля (PUT /api/v1/users/me/password)
- Смена логина (PUT /api/v1/users/me/login)
- RBAC:
  - CRUD ролей
  - назначение роли пользователю
  - отзыв роли
  - проверка прав
- CLI-команда создания суперпользователя

## Архитектура

Стек:
- FastAPI
- PostgreSQL
- Redis
- SQLAlchemy (async)
- Alembic
- JWT

Структура:
- src/api — роутеры
- src/services — бизнес-логика
- src/models — ORM и схемы
- src/core — конфигурация и безопасность
- src/db — подключение к БД
- src/cli — консольные команды

## Запуск проекта

git clone https://github.com/tramori21/Auth_sprint1_team1
cd Auth_sprint1_team1
docker compose up -d
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
set PYTHONPATH=src
python -m alembic upgrade head
python -m cli.create_superuser --login admin --password Admin_123!
python -m uvicorn main:app --host 127.0.0.1 --port 8006

## Проверка

http://127.0.0.1:8006/health

## Changelog

### authy 1.1 password
- Добавлена смена пароля
- Добавлена смена логина
- Добавлены тесты
- Приведение к линтеру
