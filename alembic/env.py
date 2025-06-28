import asyncio
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

from app.db.base import Base  # твои модели

load_dotenv(".env")

# Alembic Config object
config = context.config

# Logging
fileConfig(config.config_file_name)

# Получаем URL из env вручную
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Мета-данные моделей
target_metadata = Base.metadata



def run_migrations_offline():
    """Offline mode (без подключения к БД)"""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Online mode (асинхронный движок)"""
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
