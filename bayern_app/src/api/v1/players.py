from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Импортируем наши схемы, модели и зависимость базы
from src.schemas import players as schemas
from src.db import models
from src.db.database import SessionLocal

# Создаем "мини-приложение" (роутер) только для игроков
router = APIRouter(prefix="/players", tags=["Players"])

# Функция зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ВАЖНО: теперь мы используем @router, а не @app. 
# И путь просто "/", потому что префикс "/players" мы уже указали выше!
@router.post("/", response_model=schemas.PlayerResponse)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = models.Player(name=player.name, number=player.number, position=player.position)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

#Получаем список всех игроков(get all players)
@router.get("/", response_model=list[schemas.PlayerResponse])
def read_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()
    return players

#Получаем одного игрока по id(get one player by his id)
@router.get("/{player_id}", response_model=schemas.PlayerResponse)
def read_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    
    return player