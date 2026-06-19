from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool: # проверка на совпадения пароля с хэшем из БД
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str: # принимает обычный пароль и возвращает его захэшированную версию
    return pwd_context.hash(password)