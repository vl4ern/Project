# FC Bayern Munich - Stats Portal & API

Production-ready веб-приложение для управления статистикой, матчами и игроками футбольного клуба "Бавария" Мюнхен.

## 🛠 Технологический стек
* **Backend:** Python 3.10+, FastAPI
* **Database:** PostgreSQL, SQLAlchemy (ORM)
* **Infrastructure:** Docker, Docker Compose
* **Architecture:** Layered Architecture (DDD-lite)

## 🚀 Что уже реализовано (Progress Tracker)
- [x] Инициализация проекта и виртуального окружения.
- [x] Настройка базового сервера FastAPI.
- [x] Pydantic схемы (валидация данных).
- [x] Поднятие PostgreSQL в Docker-контейнере.
- [x] Подключение SQLAlchemy и настройка переменных окружения (.env).
- [x] Рефакторинг архитектуры (выделение роутеров, core, db слоев).
- [x] CRUD операции для сущности Player (создание и чтение).
- [ ] Настройка миграций базы данных (Alembic). *<- Мы здесь*
- [ ] Frontend интерфейс (Jinja2 + HTMX).

## 💻 Как запустить проект локально
- docker compose up -d - сборка контейнера
- docker ps - проверка состояния
- uvicorn main:app --reload - запуск локального сервера