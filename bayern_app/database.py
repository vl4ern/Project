from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Указываем путь, где будет лежать файл БД. 
# В нашем случае это файл bayern.db в текущей папке.
SQLALCHEMY_DATABASE_URL = "sqlite:///./bayern.db"

# 2. Создаем "движок". Это главный узел, который общается с файлом базы.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Эта настройка нужна только для SQLite в FastAPI
)

# 3. Фабрика сессий. Когда пользователь заходит на сайт, 
# мы открываем для него сессию (канал связи), а потом закрываем.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Базовый класс. От него мы будем наследовать таблицы (Игроки, Матчи и т.д.)
Base = declarative_base()