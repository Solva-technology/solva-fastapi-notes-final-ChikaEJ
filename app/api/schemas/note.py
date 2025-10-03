from datetime import datetime

from pydantic import BaseModel, Field

from app.core.constants import MAX_LENGTH_CONTENT, MAX_LENGTH_TITLE


class Note(BaseModel):
    title: str = Field(..., max_length=MAX_LENGTH_TITLE)
    content: str = Field(max_length=MAX_LENGTH_CONTENT)


class NoteCreate(Note):
    class Config:
        title = "Создание заметки"


class NoteUpdate(Note):
    title: str = Field(max_length=MAX_LENGTH_TITLE)
    is_public: bool = True
    is_completed: bool = True
    updated_at: datetime = Field(default_factory=datetime.now)

    class Config:
        title = "Обновление заметки"


class NoteRead(Note):
    id: int = Field(..., ge=1)
    is_public: bool = True
    is_completed: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        title = "Обзор заметки"


class NoteDelete(Note):
    id: int
    created_at: datetime
    updated_at: datetime
