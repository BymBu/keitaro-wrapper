# Keitaro Wrapper

Обёртка над API рекламного трекера Keitaro: создание кампаний с двумя потоками и редактор офферов.

## Стек

- Backend: FastAPI, SQLAlchemy, SQLite, httpx
- Frontend: HTML + JS (без сборки)
- Миграции: Alembic

## Установка

1. Склонируй репозиторий:

~~~bash
git clone <твой_репо>
cd test2
~~~

2. Создай виртуальное окружение (Python 3.10+):

~~~bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
~~~

3. Установи зависимости:

~~~bash
pip install -r requirements.txt
~~~

4. Создай `.env` в корне (пример в `.env.example`):

~~~env
KEITARO_API_URL=https://tlgk.host/admin_api/v1
KEITARO_API_KEY=твой_ключ
~~~

## Миграции

Примени миграции для создания БД:

~~~bash
alembic upgrade head
~~~

(Если БД ещё нет — создастся `keitaro.db` с таблицей `campaigns`).

## Запуск

Запусти сервер:

~~~bash
uvicorn main:app --reload
~~~

Открой интерфейс: [http://127.0.0.1:8000/ui](http://127.0.0.1:8000/ui)  
Swagger-документация: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API

- `POST /api/campaigns` — создать кампанию (принимает `name`, `geo`, `offer_id`, создаёт 2 потока в Keitaro).
- `GET /api/campaigns` — список кампаний из БД.
- `GET /api/campaigns/{id}/offers` — список офферов кампании.
- `POST /api/campaigns/{id}/offers` — добавить оффер.
- `DELETE /api/campaigns/{id}/offers/{offer_id}` — удалить оффер.

## Структура проекта

- `main.py` — роуты FastAPI.
- `app/models.py` — SQLAlchemy модель.
- `app/schemas.py` — Pydantic-схемы.
- `app/database.py` — подключение к SQLite.
- `app/keitaro_client.py` — клиент к Keitaro API.
- `frontend/` — HTML + JS интерфейс.