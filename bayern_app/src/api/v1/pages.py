from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

# Импортируем нашу базу и модели
from src.db.database import SessionLocal
from src.db import models

router = APIRouter(tags=["Web Pages"])
templates = Jinja2Templates(directory="src/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Добавляем db: Session = Depends(get_db)
@router.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    # Просим базу дать нам всех игроков
    players = db.query(models.Player).all()
    
    # Передаем игроков в шаблон (добавляем context)
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={"players": players} # <- ВАЖНО! Передаем данные
    )