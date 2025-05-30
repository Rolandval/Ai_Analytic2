from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from .models import Base

# Завантаження змінних середовища
load_dotenv(override=True)

# Отримуємо URL бази даних з змінних середовища
DATABASE_URL = os.environ.get("DATABASE_URL")

print(f"Using database connection: {DATABASE_URL}")

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

async def create_tables():
    """Создает все таблицы в базе данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def init_db():
    """Инициализирует базу данных с начальными данными"""
    
    # Создаем таблицы
    await create_tables()
    