from fastapi_users import schemas
from pydantic import ConfigDict


class UserRead(schemas.BaseUser[int]):
    model_config = ConfigDict(
        from_attributes=True,
        title="Просмотр пользователя")


class UserCreate(schemas.BaseUserCreate):
    model_config = ConfigDict(
        from_attributes=True,
        title="Создание пользователя")
