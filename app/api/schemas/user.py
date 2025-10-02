from fastapi_users import schemas
from fastapi_users.schemas import BaseUserCreate
from pydantic import ConfigDict


class UserRead(schemas.BaseUser[int]):
    full_name: str | None = None
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseUserCreate[int]):
    full_name: str | None = None
    age: int | None = None

    model_config = ConfigDict(from_attributes=True)