from fastapi import APIRouter

router: APIRouter = APIRouter()


@router.get("/")
async def index() -> str:
    return "NOTION PAGE API"


