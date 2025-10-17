from app.core.base import User
from app.db.crud.base import BaseCRUD


class UserCRUD(BaseCRUD):
    pass


user_crud = UserCRUD(User)
