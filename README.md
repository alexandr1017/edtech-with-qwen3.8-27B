# EdTech REST API

REST-сервис курса edTech (спецификация edTechREST) + веб-дашборд: студенты, курсы и
преподаватели; подписки студентов на курсы и назначение преподавателей.

Стек: **FastAPI**, **SQLAlchemy 2 async**, **SQLite** (`aiosqlite`), **Jinja2**.

## Требования

- Python ≥3.11 <3.13 (проверено на 3.12)
- [`uv`](https://docs.astral.sh/uv/) для установки зависимостей
  (в репозитории — `pyproject.toml` + `uv.lock`)

## Быстрый старт

```bat
:: 1. Зависимости: создаёт .venv и ставит пакеты из pyproject.toml (+ dev-группа)
uv sync

:: 2. (Опционально) Конфигурация — дефолты работают без .env
copy .env.example .env

:: 3. Запуск сервера
uv run uvicorn src.main:app --reload
```

Без `uv` в PATH — через виртуальное окружение напрямую
(Windows cmd / PowerShell):

```bat
:: Windows
.venv\Scripts\activate.bat
uvicorn src.main:app --reload

:: Linux / macOS
source .venv/bin/activate
uvicorn src.main:app --reload
```

- База данных создаётся **автоматически при старте** — файл `edtech.db` в корне проекта
  (`*.db` уже в `.gitignore`).
- Веб-дашборд: <http://127.0.0.1:8000/>
- Swagger/OpenAPI: `/docs` — доступен при `APP_ENVIRONMENT=local|staging`,
  скрыт в production.

## Конфигурация

Все настройки читаются из переменных окружения или файла `.env` (префикс `APP_`).

| Переменная          | Дефолт                          | Описание                                          |
|---------------------|---------------------------------|---------------------------------------------------|
| `APP_ENVIRONMENT`   | `local`                         | `local`/`staging` — с `/docs`; иначе — без        |
| `APP_DATABASE_URL`  | `sqlite+aiosqlite:///<корень>/edtech.db` | URL БД (SQLAlchemy async)                   |

Пример `.env` — см. [.env.example](./.env.example).

## Структура проекта

```
src/
├── main.py            # FastAPI-приложение, lifespan (create_all), обработчик ошибок домена
├── config.py          # Глобальные BaseSettings (APP_*)
├── database.py         # Async engine + session factory
└── edtech/             # Домен edTechREST
    ├── router.py        # REST-эндпоинты
    ├── web.py           # Веб-страницы (Jinja2)
    ├── schemas.py       # Pydantic-модели
    ├── models.py        # ORM-модели SQLAlchemy
    ├── service.py       # Бизнес-логика
    ├── dependencies.py  # Зависимости роутов
    ├── constants.py     # Коды ошибок
    ├── exceptions.py    # Доменные исключения
    ├── templates/       # Шаблоны Jinja2
    └── static/          # Статика (CSS)
tests/                  # pytest + httpx.AsyncClient (ASGITransport)
```

## Тесты и линтер

```bash
uv run pytest tests/            # 20 тестов; каждый тест получает чистую БД в tmp_path
ruff check --fix src tests      # lint
ruff format src tests           # формат
```

## API

| Метод | Путь                | Описание                                          |
|-------|---------------------|---------------------------------------------------|
| GET   | `/students/{id}`    | Студент по id                                     |
| POST  | `/students/`        | Создать студента                                  |
| PUT   | `/students/`        | Обновить студента (id из body)                    |
| DELETE| `/students/{id}`    | Удалить студента и его подписки                   |
| GET   | `/courses/{id}`     | Курс по id                                        |
| POST  | `/courses/`         | Создать курс                                      |
| PUT   | `/courses/`         | Обновить курс (id из body)                        |
| DELETE| `/courses/{id}`     | Удалить курс                                      |
| GET   | `/teachers/{id}`    | Преподаватель по id                               |
| POST  | `/teachers/`        | Создать преподавателя                             |
| PUT   | `/teachers/`        | Обновить преподавателя (id из body)               |
| DELETE| `/teachers/{id}`    | Удалить преподавателя (курсы остаются без него)   |
| GET   | `/students/`        | Все студенты со списками курсов                   |
| GET   | `/courses/`          | Все курсы со списками студентов                   |
| GET   | `/teachers/`         | Все преподаватели со списками курсов              |
| POST  | `/management/?studentId=&courseId=`    | Подписать студента на курс                        |
| DELETE| `/management/?studentId=&courseId=`    | Снять студента с курса                            |
| PUT   | `/management/?teacherId=&courseId=&action=add\|replace` | Назначить/заменить преподавателя курса |

Ошибки домена возвращаются как `{"error": "<CODE>", "detail": ...}`:
404 — `NOT_FOUND`, 409 — `CONFLICT`, 400 — `BAD_ACTION`.

Веб-страницы: `/` (дашборд), `/students`, `/courses`, `/teachers`.
