from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import matches as schemas
from src.db import models
from src.db.database import SessionLocal
from src.api.v1.dependencies import get_current_user
from src.schemas import matches as match_schemas
from src.schemas import tickets as ticket_schemas

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
@router.post("/", response_model=match_schemas.MatchResponse)
def create_match(match: match_schemas.MatchCreate, db: Session = Depends(get_db)):
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

# Вернем просто список доступных мест для матча
@router.get("/{match_id}/seats")
def get_available_seats(match_id: int, db: Session = Depends(get_db)):
    seats = db.query(models.Seat).filter(
        models.Seat.match_id == match_id,
        models.Seat.is_available == True
    ).all()
    return seats

@router.post("/buy-ticket")
def buy_ticket(
    purchase: ticket_schemas.TicketPurchase, # ТУТ ИСПРАВИЛИ!
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    # НАЧАЛО ТРАНЗАКЦИИ (Сейф открыт)
    try:
        # 1. Ищем место И БЛОКИРУЕМ ЕГО (with_for_update()) !!!
        # Это защитит нас от двойных продаж.
        seat = db.query(models.Seat).filter(models.Seat.id == purchase.seat_id).with_for_update().first()
        
        if not seat:
            raise HTTPException(status_code=404, detail="Seat not found")
            
        if not seat.is_available:
            raise HTTPException(status_code=400, detail="Sorry, this seat is already taken")

        # 2. Ищем кошелек юзера И БЛОКИРУЕМ ЕГО (чтобы баланс не ушел в минус от двух быстрых кликов)
        wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).with_for_update().first()
        
        # 3. Финансовая проверка
        if wallet.balance < seat.price:
            raise HTTPException(status_code=400, detail="Insufficient funds in wallet")

        # 4. Списываем деньги
        wallet.balance -= seat.price

        # 5. Помечаем место как занятое
        seat.is_available = False

        # 6. Выписываем билет
        new_ticket = models.Ticket(
            user_id=current_user.id,
            match_id=seat.match_id,
            seat_id=seat.id
        )
        db.add(new_ticket)

        # 7. СОХРАНЯЕМ ВСЁ РАЗОМ (Сейф закрыт, блокировки сняты)
        db.commit()
        db.refresh(new_ticket)

        return {"message": "Ticket purchased successfully!", "ticket_id": new_ticket.id}

    except Exception as e:
        # Если где-то произошла ошибка (даже внутри HTTPException)
        # мы ОБЯЗАНЫ откатить транзакцию, чтобы снять блокировки с БД!
        db.rollback()
        raise e