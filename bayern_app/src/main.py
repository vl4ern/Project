from fastapi import FastAPI
# Подключаем наш новый роутер
from src.api.v1 import players

app = FastAPI(
    title="FC Bayern Munich API",
    description="Production-ready API for Bayern Stats Portal",
    version="1.0.0"
)

# Подключаем роутер к главному приложению
app.include_router(players.router)