from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.core.db import get_async_session
from app.core.user import current_user
from app.db.crud.note import note_crud
from app.db.models.user import User

router = APIRouter()


@router.post(
    "/notes",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
async def create_note(
    data: NoteCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Создание новой заметки.

    - Доступно и пользователю, и суперпользователю.
    - Если вызывает обычный пользователь → создается его заметка.
    - Суперпользователь также может создавать заметки от своего имени.
    """
    data_dict = data.model_dump()
    data_dict["user_id"] = user.id
    return await note_crud.create(session, data_dict)


@router.get(
    "/notes",
    response_model=List[NoteRead],
    status_code=status.HTTP_200_OK,
)
async def get_notes(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Получить список заметок.

    - Обычный пользователь видит **только свои** заметки.
    - Суперпользователь видит **все заметки**.
    """
    if user.is_superuser:
        return await note_crud.get(session)  # все заметки
    return await note_crud.get_notes_of_user(session, user.id)


@router.get(
    "/notes/{note_id}",
    response_model=NoteRead,
    status_code=status.HTTP_200_OK,
)
async def get_note(
    note_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Получить заметку по ID.

    - Обычный пользователь может видеть только свои заметки.
    - Суперпользователь может видеть любую заметку.
    """
    note = await note_crud.get(session, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    if not user.is_superuser and note.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    return note


@router.patch(
    "/notes/{note_id}",
    response_model=NoteRead,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    status_code=status.HTTP_200_OK,
)
async def update_note(
    data: NoteUpdate,
    note_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Обновление заметки.

    - Обычный пользователь может обновлять только свои заметки.
    - Суперпользователь может обновлять любые заметки.
    """
    if user.is_superuser:
        return await note_crud.update(session=session, obj_id=note_id, obj_in=data)

    return await note_crud.update_own_note(
        session=session,
        data=data,
        user_id=user.id,
        note_id=note_id,
    )


@router.delete(
    "/notes/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_note(
    note_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Удаление заметки по ID.

    - Обычный пользователь может удалить только свои заметки.
    - Суперпользователь может удалить любые заметки.
    """
    if user.is_superuser:
        return await note_crud.delete(session=session, obj_id=note_id)

    return await note_crud.delete_own_note(session=session, note_id=note_id, user_id=user.id)


@router.get(
    "/notes/global",
    response_model=List[NoteRead],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(current_user)]
)
async def get_global_notes(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Получить публичные заметки.

    - Доступно и пользователям, и суперпользователям.
    - Возвращает все заметки, помеченные как публичные.
    """
    notes = await note_crud.get_global_notes(session=session)
    return notes
