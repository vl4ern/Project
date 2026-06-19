from fastapi import FastAPI
# Подключаем наш новый роутер
from src.api.v1 import players
from src.api.v1 import matches
from src.api.v1 import players, matches, pages, users


app = FastAPI(
    title="FC Bayern Munich API",
    description="Production-ready API for Bayern Stats Portal",
    version="1.0.0"
)

# Подключаем роутер к главному приложению
app.include_router(players.router)
app.include_router(matches.router)
app.include_router(pages.router)
app.include_router(users.router)