from fastapi import APIRouter

from .endpoints import note_router, user_router

main_router = APIRouter()

main_router.include_router(note_router, prefix="/notes", tags=["Note"])
main_router.include_router(user_router, prefix="/users", tags=["Users"])
