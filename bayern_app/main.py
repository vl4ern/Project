from fastapi import FastAPI
from pydantic import BaseModel

class Player(BaseModel):
    name: str
    number: int
    position: str

app = FastAPI(title="Bayern Munich Stats API")

@app.get("/")
def read_root():
    return {"message": "Mia San Mia!"}

#временная база данных (ключ - номер игрока)
fake_players_db = {
    1: {"name": "Manuel Neuer", "number": 1, "position": "Goalkeeper"},
    9: {"name": "Harry Kane", "number": 9, "position": "Forward"},
    25: {"name": "Thomas Müller", "number": 25, "position": "Midfielder"}
}

@app.get("/players/{player_id}")
def get_player(player_id: int):
    player = fake_players_db.get(player_id)
    if player:
        return player
    else:
        return{"error": "player not found"}

@app.post("/players/")
def create_player(player: Player):
    if player.number in fake_players_db:
        return{"eroor": "Player with this number already exist"}
    
    fake_players_db[player.number] = player.model_dump()

    return {"message": "Player added successfully!", "player": player}