from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt
from src.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool: # проверка на совпадения пароля с хэшем из БД
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str: # принимает обычный пароль и возвращает его захэшированную версию
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Генерирует JWT токен (ключ-карту) для пользователя.
    """
    # Делаем копию данных (обычно там будет {"sub": "example@gmail.com"})
    to_encode = data.copy()
    
    # Считаем, когда токен "протухнет"
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Добавляем время смерти токена в данные (стандартное поле "exp")
    to_encode.update({"exp": expire})
    
    # Главная магия: криптографически подписываем данные нашим SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt