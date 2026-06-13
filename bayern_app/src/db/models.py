from sqlalchemy import Column, Integer, String
from src.db.database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    number = Column(Integer, unique=True)
    position = Column(String)