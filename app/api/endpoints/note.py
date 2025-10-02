from typing import Dict, List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.core.db import get_async_session
from app.core.user import current_user
from app.db.crud.note import note_crud
from app.db.models.user import User

router = APIRouter()


@router.post("/notes",
             response_model=NoteRead,
             status_code=status.HTTP_201_CREATED,
             response_model_exclude_none=True,
             response_model_exclude_unset=True
             )
async def create_note(
        data: NoteCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    data_dict = data.model_dump()
    data_dict["user_id"] = user.id
    return await note_crud.create(session, data_dict)


@router.get("/notes",
            response_model=List[NoteRead],
            status_code=status.HTTP_200_OK
            )
async def get_notes(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    notes = await note_crud.get_notes_of_user(session, user.id)
    return notes


@router.get("/notes/{note_id}",
            response_model=NoteRead,
            status_code=status.HTTP_200_OK,
            dependencies=[Depends(current_user)])
async def get_note(
        note_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    return await note_crud.get(session, note_id)


@router.patch("/notes/{note_id}",
              response_model=NoteRead,
              response_model_exclude_none=True,
              response_model_exclude_unset=True ,
              status_code=status.HTTP_200_OK
              )
async def update_note(
        data: NoteUpdate,
        note_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user),

):
    note_updated = await note_crud.update_own_note(
        session=session,
        data=data,
        user_id= user.id,
        note_id=note_id
    )
    return note_updated
@router.delete("/notes/{note_id}",response_model=NoteRead,status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
        note_id: int,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    return await note_crud.delete_own_note(session=session, note_id=note_id, user_id=user.id)

