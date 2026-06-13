from datetime import date
from pydantic import BaseModel

class MatchCreate(BaseModel):
    opponent: str
    is_home: bool
    date_match: date
    bayern_goals: int
    opponent_goals: int

class MatchResponse(BaseModel):
    id: int
    opponent: str
    is_home: bool
    date_match: date
    bayern_goals: int
    opponent_goals: int

    class Config:
        from_attributes = True