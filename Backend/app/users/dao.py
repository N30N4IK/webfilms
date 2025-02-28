from sqlalchemy import select
from app.users.models import User
from app.database import async_session_maker
from app.dao.base import BaseDAO

        
class UserDAO(BaseDAO):
    model = User
    @staticmethod
    async def get_all_users() -> list[dict]:
        async with async_session_maker() as session:
            query = select(User)
            users = await session.execute(query)
            return users.scalars().all()
    @staticmethod
    async def add_user(id: int, first_name: str, phone_number: str, email: str) -> User:
        async with async_session_maker() as session:
            new_user = User (
                id=id,
                first_name=first_name,
                phone_number=phone_number,
                email=email,
            )

            try:
                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)
                return new_user
            except Exception as e:
                await session.rollback()
                raise ValueError(f"Failed to add user: {e}")