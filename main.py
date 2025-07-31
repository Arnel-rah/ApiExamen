import json
from typing import List
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
app = FastAPI()
class art_model(BaseModel):
    author: str
    title: str
    cotent: str
    creation_datetime: str

art_model_list: List[art_model] = []

def serialized_art_model():
    arts_converted = []
    for art in art_model_list:
        arts_converted.append(art.model_dump())
    return arts_converted

@app.get('/ping')
def ping_pong():
    return "Pong"

@app.get('/home')
def welcome_home():
    with open("home.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")


@app.get("/{full_path:path}")
def catch_all(full_path: str):
    with open("not_found.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=404, media_type="text/html")

@app.post('/posts')
def add_art(arts: List[art_model]):
    art_model_list.extend(arts)
    return {"events": serialized_art_model()}

@app.get('/posts')
def list_art():
    return {"arts": serialized_art_model()}

@app.put('/posts')
def update_art(arts: List[art_model]):
    existing_arts = {arts.title: arts for arts in art_model_list}
    for art in arts:
        existing_arts[art.title] = art
    art_model_list.clear()
    art_model_list.extend(existing_arts.values())
    return {"events": serialized_art_model()}


# BONUS
@app.get('/ping/auth')
def root_auth(request: Request):
    password = request.headers.get("password")
    username = request.headers.get("username")
    if password != "12345678" and username != "admin":
        return Response(
            content=json.dumps({"message": f"Invalid authentification: {password} " + {username}}),
            status_code=403,
            media_type="application/json"
        )
    return {f'pong'}
    