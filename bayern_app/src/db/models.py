from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime, ForeignKey, Float
from src.db.database import Base
from datetime import datetime

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer, unique=True)
    position = Column(String)

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    opponent = Column(String)
    is_home = Column(Boolean)
    date_match = Column(Date)
    bayern_goals = Column(Integer, default=0)
    opponent_goals = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    # Почта будет логином. unique=True значит, что двух юзеров с одной почтой быть не может
    email = Column(String, unique=True, index=True) 
    # Храним только зашифрованный след пароля!
    hashed_password = Column(String)
    # В банках не удаляют людей, их деактивируют (soft delete)
    is_active = Column(Boolean, default=True)
    # Время создания аккаунта (для аудита)
    created_at = Column(DateTime, default=datetime.utcnow)

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    balance = Column(Float, default=0.0)

class Seat(Base):
    """Модель конкретного места на стадионе для конкретного матча"""
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True) # Привязка к матчу
    
    # Чтобы фанат понимал, где он сидит
    sector = Column(String) # Например: "A1"
    row = Column(Integer)   # Ряд
    number = Column(Integer) # Место
    
    price = Column(Float, nullable=False) # Цена именно этого места
    is_available = Column(Boolean, default=True) # Свободно ли оно?

class Ticket(Base):
    """Модель купленного билета (Связывает Юзера, Матч и Место)"""
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    match_id = Column(Integer, ForeignKey("matches.id"), index=True)
    seat_id = Column(Integer, ForeignKey("seats.id"), unique=True) # Одно место = Строго один билет!
    
    purchase_time = Column(DateTime, default=datetime.utcnow)