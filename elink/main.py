from fastapi import APIRouter
import ujson
import requests

router: APIRouter = APIRouter()

headers: dict = {
    "content-type": "text/html; charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
}


@router.get("/")
async def index():
    return "eLink API"


@router.get("/{uid}")
@router.get("/{uid}/title")
async def title(uid: int) -> str:
    res: requests.Response = requests.post(
        "https://api.live.bilibili.com/room/v1/Room/get_info",
        params={"id": uid},
        headers=headers
    )
    result: dict = ujson.loads(res.text)
    return result["data"]["title"]
