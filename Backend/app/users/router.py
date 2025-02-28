from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from app.database import async_session_maker
from app.users.models import User
from app.users.dao import UserDAO
from app.users.schemas import UUser
from typing import List
from app.users.rb import RBUser


router = APIRouter(prefix='/users', tags=['Пользователи'])

@router.get('/', summary='Получить всех пользователей', response_model=List[UUser])
async def get_all_users(request_body: RBUser = Depends()) -> list[UUser]:
    return await UserDAO.get_all_users(**request_body.to_dict())

@router.get('/{user_id}', summary='Получить пользователя по id', response_model=List[UUser])
async def get_user_by_id(request_body: RBUser = Depends()) -> list[UUser]:
    return await UserDAO.get_all_users(**request_body.to_dict())

@router.post('/add', summary='Добавление пользователя')
async def register_user(user: UUser) -> UUser:
    try:
        new_user = await UserDAO.add_user(
            id=user.id, first_name=user.first_name, phone_number=user.phone_number, email=user.email
        )
        return UUser.model_validate(new_user)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f'Failed to create user: {str(e)}')
    