from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import settings

Base = declarative_base()

dsn = (
    f'postgresql+asyncpg://{settings.user}:{settings.password}'
    f'@{settings.host}:{settings.port}/{settings.db}'
)

engine = create_async_engine(dsn, echo=False, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

from models import user, role, user_role, login_history, refresh_token  # noqa: F401,E402

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session