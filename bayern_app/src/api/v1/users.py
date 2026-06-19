from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.database import SessionLocal
from src.db import models
from src.schemas import users as schemas
from src.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["Users (Security)"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового болельщика (создание пользователя).
    """
    # 1. Проверяем, существует ли уже пользователь с таким email
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        # Если есть - кидаем ошибку 400 (Bad Request)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists in the system."
        )

    # 2. Шифруем пароль! 
    hashed_pw = get_password_hash(user_in.password)

    # 3. Создаем объект базы данных (ORM)
    # ВНИМАНИЕ: мы передаем hashed_password, а НЕ user_in.password!
    new_user = models.User(
        email=user_in.email,
        hashed_password=hashed_pw
    )

    # 4. Сохраняем в базу (Транзакция)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 5. Возвращаем юзера (FastAPI пропустит его через UserResponse и удалит пароль из ответа)
    return new_user