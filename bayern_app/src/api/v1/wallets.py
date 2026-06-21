from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas import wallets as schemas
from src.db.database import SessionLocal
from src.db import models
from src.api.v1.dependencies import get_current_user # Наш Охранник!

router = APIRouter(prefix="/wallet", tags=["Finance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Защищенный маршрут: только авторизованные пользователи!
@router.get("/balance")
def get_my_balance(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Возвращает баланс текущего пользователя.
    """
    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()
    
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
        
    return {"email": current_user.email, "balance": wallet.balance}

@router.post("/deposit")
def post_deposit(deposit_data: schemas.WalletDeposit, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):

    wallet = db.query(models.Wallet).filter(models.Wallet.user_id == current_user.id).first()

    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    else:
        wallet.balance += deposit_data.amount

    db.commit()
    db.refresh(wallet)
    return{"message": "Success", "new_balance": wallet.balance}