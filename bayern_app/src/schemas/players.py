from pydantic import BaseModel

class PlayerCreate(BaseModel):
    name: str
    number: int
    position: str

class PlayerResponse(BaseModel):
    id: int
    name: str
    number: int
    position: str

    class Config:
        from_attributes = True