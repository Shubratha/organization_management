from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

# Create async engine for the master database
engine = create_async_engine(DATABASE_URL, echo=True, isolation_level="AUTOCOMMIT")

# Create async session factory
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_database(db_name: str, user: str, password: str) -> str:
    """Create a new database for an organization."""
    try:
        async with engine.connect() as conn:
            # Create new database (needs AUTOCOMMIT mode)
            await conn.execute(text(f'CREATE DATABASE "{db_name}"'))

            # Create user with password
            await conn.execute(text(f"CREATE USER \"{user}\" WITH PASSWORD '{password}'"))

            # Grant privileges
            await conn.execute(text(f'GRANT ALL PRIVILEGES ON DATABASE "{db_name}" TO "{user}"'))

            # Return the connection string for the new database
            return f"postgresql+asyncpg://{user}:{password}@db:5432/{db_name}"

    except Exception as e:
        # If database/user already exists, just return the connection string
        if "already exists" in str(e):
            return f"postgresql+asyncpg://{user}:{password}@db:5432/{db_name}"
        raise e
