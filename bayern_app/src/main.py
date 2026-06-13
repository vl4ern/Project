from fastapi import FastAPI
from src.db.database import Base, engine
# Подключаем наш новый роутер
from src.api.v1 import players

# Создаем таблицы (позже мы заменим это на миграции)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FC Bayern Munich API",
    description="Production-ready API for Bayern Stats Portal",
    version="1.0.0"
)

# Подключаем роутер к главному приложению
app.include_router(players.router)