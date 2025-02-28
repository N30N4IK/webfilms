from typing import AsyncGenerator
from fastapi import Depends
from app.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_async_session():
        yield session