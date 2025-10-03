from app.db.crud.base import BaseCRUD
from app.core.base import User


class UserCRUD(BaseCRUD):
    pass

user_crud = UserCRUD(User)