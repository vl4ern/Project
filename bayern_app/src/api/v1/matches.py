from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.schemas import matches as schemas
from src.db import models
from src.db.database import SessionLocal

# Создаем "мини-приложение" (роутер) только для матчей
router = APIRouter(prefix="/matches", tags=["Matches"])

# Функция зависимости
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ВАЖНО: теперь мы используем @router, а не @app. 
# И путь просто "/", потому что префикс "/matches" мы уже указали выше!
@router.post("/", response_model=schemas.MatchResponse)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_match = models.Player(opponent=match.opponent, is_home=match.is_home, date_match=match.date_match, 
                             bayern_goals=match.bayern_goals, opponent_goals=match.opponent_goals)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match

#Получаем список всех игроков(get all matches)
@router.get("/", response_model=list[schemas.MatchResponse])
def read_matches(db: Session = Depends(get_db)):
    matches = db.query(models.Match).all()
    return matches

#Получаем одного игрока по id(get one match on his id)
@router.get("/{match_id}", response_model=schemas.MatchResponse)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()

    if match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    
    return match