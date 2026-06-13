from sqlalchemy import Column, Integer, String, Date, Boolean
from src.db.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer, unique=True)
    position = Column(String)

class Match(Base):
    __tablename__ = "match"

    id = Column(Integer, primary_key=True, index=True)
    opponent = Column(String)
    is_home = Column(Boolean)
    date_match = Column(Date)
    bayern_goals = Column(Integer, default=0)
    opponent_goals = Column(Integer, default=0)