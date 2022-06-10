from fastapi import APIRouter
from .user import router as user_router

router: APIRouter = APIRouter()


@router.get("/")
async def index():
    return "MCBBS API"


router.include_router(user_router, prefix="/user")
