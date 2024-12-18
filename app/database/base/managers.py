import logging

from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.async_base import Base

logger = logging.getLogger(__name__)


class BaseManager:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


class BaseModelManager(BaseManager):
    model = None

    async def do_commit(self) -> None:
        try:
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            raise e

    async def get(self, **filters) -> model:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_one_or_none(self, **filters) -> model:
        try:
            stmt = select(self.model)
            if filters:
                stmt = stmt.filter_by(**filters)
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None
        except MultipleResultsFound:
            return None

    async def all(self, **filters) -> list[model]:
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, **kwargs) -> model:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.do_commit()
        return obj

    async def update(self, obj: Base, **kwargs) -> model | Base:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        await self.do_commit()
        return obj

    async def delete(self, obj: Base) -> model | Base:
        await self.session.delete(obj)
        await self.session.commit()
        return obj
