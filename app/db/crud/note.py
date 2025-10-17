from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.note import NoteUpdate
from app.core.base import Note
from app.db.crud.base import BaseCRUD


class NoteCRUD(BaseCRUD):

    async def check_ownership(self, session: AsyncSession, note_id: int,
                              user_id: int):
        note = await self.get(session, note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        if note.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized")
        return note

    async def get_notes_of_user(self, session: AsyncSession, user_id: int):
        sqlr = (
            select(self.model)
            .where(self.model.user_id == user_id)
        )
        notes_db = await session.execute(sqlr)
        return notes_db.scalars().all()

    async def update_own_note(self, session: AsyncSession,
                              note_id: int,
                              user_id: int,
                              data: NoteUpdate):
        check = await self.check_ownership(session, note_id, user_id)
        if check is not None:
            return await self.update(session, note_id, data)

    async def delete_own_note(self, session: AsyncSession, note_id: int,
                              user_id: int):
        check = await self.check_ownership(session, note_id, user_id)
        if check is not None:
            return await self.delete(session, note_id)

    async def get_global_notes(self, session: AsyncSession):
        sqlr = (select(self.model).where(self.model.is_public == True))
        notes_db = await session.execute(sqlr)
        return notes_db.scalars().all()


note_crud = NoteCRUD(Note)
