from fastapi import APIRouter
from .retrieve import router as retrieve_router
from .retrieve_all import router as retrieve_all_router

router = APIRouter()
router.include_router(retrieve_router)
router.include_router(retrieve_all_router)
