from typing import Callable, Union

from sqlalchemy.ext.asyncio import (
    AsyncConnection, AsyncEngine, AsyncSession, create_async_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(settings.database_url, pool_size=0, max_overflow=30, echo=True)


def create_sessionmaker(bind_engine: Union[AsyncEngine, AsyncConnection]) -> Callable[..., AsyncSession]:
    return sessionmaker(
        bind=bind_engine,
        autoflush=False,
        expire_on_commit=False,
        future=True,
        class_=AsyncSession,
    )


engine = create_engine()
Session = create_sessionmaker(engine)

Base = declarative_base(bind=engine)
