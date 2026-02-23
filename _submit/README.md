# Auth_sprint1_team1

# Auth Service

Учебный Auth-сервис: аутентификация + авторизация (RBAC).

Что реализовано:
- регистрация и вход
- профиль текущего пользователя
- refresh-токены с ротацией и инвалидированием старого
- logout (инвалидация refresh)
- история входов
- роли (RBAC): CRUD + назначение/отзыв + проверка прав (управление ролями доступно суперпользователю)

---

## Адреса и порты (локально)
- API: http://127.0.0.1:8006
- Postgres (на хосте): 127.0.0.1:5433 (в контейнере 5432)
- Redis (на хосте): 127.0.0.1:6380 (в контейнере 6379)

---

## Быстрый старт (Windows, PowerShell)

### 1) Поднять инфраструктуру (Postgres + Redis)
```powershell
docker compose up -d
```

### 2) Виртуальное окружение и зависимости
Если `.venv` уже создано — пропусти создание и выполни только установку зависимостей.
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3) Применить миграции
```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m alembic upgrade head
```

### 4) Запустить API
```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8006
```

### 5) Проверка
```powershell
Invoke-WebRequest http://127.0.0.1:8006/health -UseBasicParsing
```

---

## Переменные окружения
Секреты в репозиторий не кладём.
Используй свой `.env` локально, а в проекте держим только пример: `.env.example`.

---

## CLI: создать/обновить суперпользователя
```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m cli.create_superuser --login admin --password Admin_123!
```

---

## Тесты
Интеграционные тесты ожидают запущенный API на `http://127.0.0.1:8006`.
```powershell
.\.venv\Scripts\python.exe -m pytest .\tests -q
```

---

## Если что-то пошло не так
- Порт 8006 занят: останови процесс, который слушает порт, и запусти сервис заново.
- Миграции падают: проверь, что поднят Postgres (`docker compose ps`) и заполнены переменные окружения.

