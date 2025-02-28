from httpx import delete
from sqlalchemy import insert, update, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from app.database import async_session_maker
from app.users.models import User


class BaseDAO:
    model = None

    @classmethod
    async def find_all_users(cls, **filtre_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filtre_by)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            new_intanse = cls.model(**values)
            session.add(new_intanse)
            try:
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e
            return new_intanse