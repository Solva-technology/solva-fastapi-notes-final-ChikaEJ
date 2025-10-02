from fastapi import APIRouter

from .endpoints import note_roter


main_router = APIRouter()

main_router.include_router(note_roter, prefix="/notes", tags=["Note"])
