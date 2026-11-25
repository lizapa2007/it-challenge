# IT Challenge

Веб-сервис для обработки CSV-файлов. Пользователь загружает CSV и выбирает
числовой столбец, а сервис считает по нему статистику (count, min, max, mean)
и сохраняет задание в базу данных.

## Технологии

- Python 3, FastAPI
- PostgreSQL, SQLAlchemy
- pytest

## Структура проекта

```
app/
├── main.py         — эндпоинты API
├── database.py     — подключение к базе данных
├── models.py       — модель таблицы tasks
├── processing.py   — обработка задания и смена статусов
└── stats.py        — чтение CSV и расчёт статистики
tests/              — автотесты
examples/           — примеры CSV-файлов
```

## Установка и запуск

1. Установить PostgreSQL и создать базу данных:

```sql
   CREATE DATABASE it_challenge;
```

2. Создать виртуальное окружение и установить зависимости:

```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
```

3. Скопировать `.env.example` в `.env` и указать в нём свой пароль от PostgreSQL.

4. Запустить сервер:

```powershell
   fastapi dev app/main.py
```

Документация API: http://127.0.0.1:8000/docs

## API

| Метод | Адрес | Описание |
|---|---|---|
| GET | `/health` | проверка работы сервиса и базы данных |
| POST | `/tasks` | загрузить CSV (`file`) и указать столбец (`column`) |
| GET | `/tasks` | список всех заданий |
| GET | `/tasks/{id}` | статус и результат задания |

Статусы задания: `pending` → `processing` → `completed` или `failed`.

Пример ответа:

```json
{
  "id": 1,
  "status": "completed",
  "filename": "weather.csv",
  "column": "temperature",
  "result": {"count": 4, "min": 19.8, "max": 23.0, "mean": 21.6},
  "error": null
}
```

## Тесты

```powershell
python -m pytest -v
```

Тесты используют временную базу SQLite и не затрагивают основную базу PostgreSQL.