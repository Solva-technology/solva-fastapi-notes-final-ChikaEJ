from typing import Type, Generic, Optional, List
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.base import CreateSchemaType, ModelType, UpdateSchemaType


def db_transaction(func):
    async def wrapper(self, session: AsyncSession, *args, **kwargs):
        try:
            return await func(self, session, *args, **kwargs)
        except Exception:
            await session.rollback()
            raise
    return wrapper


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, model_id: int) -> Optional[
        ModelType]:
        return await session.get(self.model, model_id)

    async def get_all(self, session: AsyncSession) -> List[ModelType]:
        result = await session.execute(select(self.model))
        return result.scalars().all()

    @db_transaction
    async def create(self, session: AsyncSession, data: CreateSchemaType) -> ModelType:
        obj_db = self.model(**data.model_dump())
        session.add(obj_db)
        await session.commit()
        await session.refresh(obj_db)
        return obj_db

    @db_transaction
    async def update(self, session: AsyncSession, model_id: int, data: UpdateSchemaType) -> Optional[
        ModelType]:
        stmt = (
            update(self.model)
            .where(self.model.id == model_id)
            .values(**data.model_dump(exclude_unset=True))  # обновляем только переданные поля
            .returning(self.model)
        )
        result = await session.execute(stmt)
        await session.commit()
        return result.scalars().one_or_none()

    @db_transaction
    async def delete(self, session: AsyncSession, model_id: int) -> Optional[
        ModelType]:
        obj_db = await session.get(self.model, model_id)
        if not obj_db:
            return None
        await session.delete(obj_db)
        await session.commit()
        return obj_db
