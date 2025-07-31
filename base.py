from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List
from fastapi.responses import HTMLResponse

app = FastAPI()

class Player(BaseModel):
    Number: int
    Name: str
players: List[Player] = []

@app.get("/hello", response_class=HTMLResponse)
async def hello():
    return "<h1>Hello</h1>"
@app.get("/welcome")
async def welcome(name: str):
    if not name:
        raise HTTPException(status_code=400, detail="Name parameter is required")
    return {"message": f"Welcome {name}"}
@app.post("/players", status_code=201)
async def create_player(player: Player):
    players.append(player)
    return players
@app.get("/players")
async def get_players():
    return players
@app.put("/players")
async def update_or_create_player(player: Player):
    for i, existing_player in enumerate(players):
        if existing_player.Number == player.Number:
            players[i] = player
            return players
    players.append(player)
    return players
@app.get("/players-authorized")
async def get_players_authorized(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    if authorization != "bon courage":
        raise HTTPException(status_code=403, detail="Invalid authorization credentials")
    return players
