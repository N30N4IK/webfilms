from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import jinja2


router = APIRouter(prefix="", tags=['s'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get('/login')
async def get_page_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get('/search?query')
async def get_page_search_films(request: Request):
    return templates.TemplateResponse("search_films.html", {"request": request})

@router.get('/film/{id}')
async def get_page_film(request: Request):
    return templates.TemplateResponse("film.html", {"request": request})