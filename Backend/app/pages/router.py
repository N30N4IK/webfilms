from fastapi import APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
import jinja2
from app.pages.database_films import movies

router = APIRouter(prefix="", tags=['s'])
templates = Jinja2Templates(directory='app/templates')


@router.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get('/login')
async def get_page_login(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@router.get('/search')
async def get_search_page(request: Request, q: str = None):
    search_term = q if q else ""
    return templates.TemplateResponse('searchPage.html', {'request': request, "search_term": search_term})

@router.get('/movies/{movie_id}')
async def get_page_description_film(request: Request, movie_id: int):
    movie = next((m for m in movies if m['id'] == movie_id))
    if movie is None:
        raise HTTPException(status_code=404, detail='Фильм не найден')
    
    return templates.TemplateResponse("description.html", {"request": request, "movie": movie})
