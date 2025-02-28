from token import OP
from fastapi import FastAPI, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from httpx import request
from utils import json_to_dict_list
import os
from typing import Optional
from app.pages.router import router as pages_router
from app.users.router import router as router_users

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

path_to_json = os.path.join(parent_dir, 'users.json')
path_to_json_films = os.path.join(parent_dir, 'films.json')

app = FastAPI()
app.include_router(pages_router)
app.include_router(router_users)

app.mount("/static", StaticFiles(directory='static'), name="static")


@app.get("/")
async def get_all_film(film: Optional[str] = None):
    return json_to_dict_list(path_to_json_films)

# @app.get("/film/{title}") # Вывод описания фильма на ГЛАВНОМ МЕНЮ
# def get_film(title):
#     films = json_to_dict_list(path_to_json_films)
#     filtred_films = []
#     for film in films:
#         if film["title"].lower() == title.lower():
#             filtred_films.append(film)
#             return filtred_films
#     return {"error": "Фильм не найден"}



@app.get("/film/{id_film}") # Вывод СТРАНИЦЫ фильма
async def get_definite_film(id_film):
    films = json_to_dict_list(path_to_json_films)
    for film in films:
        if film["id_film"] == id_film:
            return film
    return {"error": "Фильм не найден"}


@app.get("/search?query={id_film}")
async def get_searched_film(id_film):
    films = json_to_dict_list(path_to_json_films)
    for search_films in films:
        if search_films['id_film'] == id_film:
            return search_films
    return {"error": "Фильм не найден"}



@app.get("/profile")    
async def get_profile():
    return json_to_dict_list(path_to_json)

@app.get('/login')
async def get_login():
    return {"data":  "login"}





# Проверка
@app.get("/users")
def get_users(id_user: Optional[int] = None):
    users = json_to_dict_list(path_to_json)
    # if id_user is None:
    #     return users
    # else:
    #     return_list = []
    #     for user in users:
    #         if user["id_user"] == id_user:
    #             return_list.append(user)
    return users

@app.get("/users/{id_user}")
def get_users_id(id_user: int):
    users = json_to_dict_list(path_to_json)
    filtred_users = []
    for user in users:
        if user["id_user"] == id_user:
            filtred_users.append(user)

    return filtred_users