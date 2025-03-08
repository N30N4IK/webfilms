from contextlib import asynccontextmanager
from token import OP
from fastapi import FastAPI, Query, Depends, status, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from h11 import Request
from httpx import request
from utils import json_to_dict_list
import os
import asyncio
from typing import Optional
from app.pages.router import router as pages_router
from app.users.router import router as router_users
from pydantic import BaseModel, field_validator
from .users import models
from .users.models import get_db, User, create_db_and_tables


 
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

path_to_json = os.path.join(parent_dir, 'users.json')
path_to_json_films = os.path.join(parent_dir, 'films.json')

app = FastAPI()
app.include_router(pages_router)
app.include_router(router_users)

app.mount("/static", StaticFiles(directory='static'), name="static")

class AuthForm(BaseModel):
    auth_value: str
    auth_type: str

    @field_validator('auth_type')
    def auth_type_must_be_valid(cls, value):
        if value not in ('phone', 'email'):
            raise ValueError('auth_type must be "phone" or "email"')
        return value
    
    @field_validator('auth_value')
    def auth_value_must_be_valid(cls, value, values):
        auth_type = values.get('auth_type')
        if auth_type == 'phone' and not value.isdigit():
            raise ValueError('auth_value must be a valid phone number')
        elif auth_type == 'email':
            if not '@' in value or not '.' in value:
                raise ValueError("Некорректный email")
        return value
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    await models.create_db_and_tables()
    yield


@app.get("/")
async def get_all_film(film: Optional[str] = None):
    return json_to_dict_list(path_to_json_films)


@app.get("/profile")    
async def get_profile():
    return json_to_dict_list(path_to_json)

@app.post('/login')
async def post_login(
    auth_form: AuthForm,
    db: AsyncSession = Depends(get_db),
):
    auth_value = auth_form.auth_value
    auth_type = auth_form.auth_type
    
    existing_user = None

    if auth_type == 'phone':
        existing_user = await db.execute(
            select(User).filter(User.phone == auth_value)
        )
        existing_user = existing_user.scalar_one_or_none()
    elif auth_type == 'email':
        existing_user = await db.execute(
            select(User).filter(User.email == auth_value)
        )
        existing_user = existing_user.scalar_one_or_none

    if existing_user:
        return JSONResponse(content={'message': 'Вход успешен'})
    else:
        new_user = User()

        if auth_type == 'phone':
            new_user.phone = auth_value
        elif auth_type == 'email':
            new_user.email = auth_value

        try:
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        return JSONResponse(content={'message': "Регистрация успешна"}, status_code=status.HTTP_201_CREATED)




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


# CORS configuration (Adjust as needed for production)
origins = [
    "http://localhost:3000",
    "https://your-production-domain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

KINOPOISK_API_KEY = "RAXFWSF-BEW4PEJ-HMXH6WZ-EZAY68E"  # Replace with your actual API key
KINOPOISK_API_BASE_URL = "https://api.kinopoisk.dev/v1.4"  # Base URL for API Kinopoisk

@app.get("/api/search-movies")
async def search_movies(
    query: Optional[str] = Query(None, title="Search Query"),
    year: Optional[int] = Query(None, title="Year of movie"),
    genres_name: Optional[str] = Query(None, title="Genre of movie"),
    rating_imdb: Optional[str] = Query(None, title="IMDb rating range (e.g., 8-10)"),
    limit: int = Query(10, title="Limit results per page"),
    page: int = Query(1, title="Page number"),
):
    """
    Searches for movies on Kinopoisk API v1.4.  You can combine search parameters.
    """

    if not any([query, year, genres_name, rating_imdb]):
        raise HTTPException(status_code=400, detail="At least one search parameter is required (query, year, genre, rating)")


    url = f"{KINOPOISK_API_BASE_URL}/movie?"  # Start building the URL

    # Add query parameters based on provided values
    if query:
        url += f"name={query}&"
    if year:
        url += f"year={year}&"
    if genres_name:
        url += f"genres.name={genres_name}&"
    if rating_imdb:
        url += f"rating.imdb={rating_imdb}&"

    url += f"limit={limit}&page={page}"  # Add limit and page
    url = url.rstrip("&") # Remove trailing ampersand if any


    headers = {"X-API-KEY": KINOPOISK_API_KEY, "Content-Type": "application/json"} # Add API key to headers


    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers) # Include headers in the request
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Kinopoisk API Error: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to Kinopoisk API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")