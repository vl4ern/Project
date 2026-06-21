from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from src.core.config import settings
from src.db.database import SessionLocal
from src.db import models

# Эта штука автоматически ищет токен в заголовках запроса (Authorization: Bearer <token>)
# tokenUrl указывает Swagger'у, куда идти за токеном (для красивой кнопки Authorize)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Dependency (Охранник).
    Принимает токен, расшифровывает его, достает email, ищет юзера в БД и возвращает его.
    Если что-то не так - выкидывает 401 Unauthorized.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Расшифровываем токен нашим СЕКРЕТНЫМ КЛЮЧОМ
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        # 2. Достаем email (мы прятали его под ключом "sub")
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
            
    except JWTError:
        # Если токен поддельный, просроченный или поврежденный
        raise credentials_exception
        
    # 3. Идем в базу и ищем пользователя
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if user is None:
        raise credentials_exception
        
    return user