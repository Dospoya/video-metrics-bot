# Video Metrics Bot (Telegram + LLM + PostgreSQL)

Telegram-бот, который принимает аналитические вопросы на русском языке по видео-метрикам, преобразует их в структурированный запрос (intent + params) через LLM и возвращает **одно число** как ответ.

## Стек
- Python 3.13
- PostgreSQL 17 (Docker Compose)
- asyncpg
- aiogram
- OpenAI Responses API (structured output через Pydantic)

---

## 1) Требования
- Docker + Docker Compose
- Python 3.13+
- uv (желательно) или любой способ установить зависимости

---

## 2) Переменные окружения

### 2.1. PostgreSQL (Docker)
Файл: `infra/.env`

Пример:
```env
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=videometricsbot
DATABASE_URL=postgres://user:pass@localhost:5432/videometricsbot
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```


## 3) Запуск базы данных
###3.1. Поднять PostgreSQL
docker compose -f infra/docker-compose.yml up -d

### 3.2. (Опционально) Пересоздать БД полностью

Удаляет volume с данными:
docker compose -f infra/docker-compose.yml down -v
docker compose -f infra/docker-compose.yml up -d


## 4) Создание / пересоздание таблиц (SQL)

DDL лежит в папке sql/:
sql/schema.sql — создание таблиц и индексов
sql/drop.sql — удаление таблиц (для пересоздания)

### 4.1. Удалить таблицы
docker compose -f infra/docker-compose.yml exec -T db \
  psql -U user -d videometricsbot -f /docker-entrypoint-initdb.d/drop.sql

### 4.2. Создать таблицы
docker compose -f infra/docker-compose.yml exec -T db \
  psql -U user -d videometricsbot -f /docker-entrypoint-initdb.d/schema.sql
  
  
## 5) Загрузка данных из JSON в базу

В корне проекта лежит файл:
videos.json — массив объектов videos с вложенными snapshots

### 5.1. Запуск загрузчика
python -m src.db.init_db

## 6) Запуск Telegram-бота
python -m main


## 7) Как работает интерпретация запросов (архитектура)
### 7.1. Поток обработки
- Пользователь пишет вопрос на русском в Telegram.
- Модуль converter отправляет вопрос в LLM и получает структурированный объект Query:
  - intent — тип операции
  - params — параметры (даты/порог/creator_id)
- execute_query выбирает SQL-функцию и выполняет запрос к PostgreSQL.
- Бот возвращает пользователю одно число.

## 8) Поддерживаемые intents (пример)
- total_videos — сколько всего видео
- creator_videos_in_period — сколько видео у креатора за период (по video_created_at)
- videos_over_views — сколько видео с просмотрами > N (по videos.views_count)
- views_growth_on_date — суммарный прирост просмотров за день (по SUM(video_snapshots.delta_views_count))
- videos_with_growth_on_date — сколько разных видео имели прирост просмотров за день (по COUNT(DISTINCT video_id) и delta_views_count > 0)
