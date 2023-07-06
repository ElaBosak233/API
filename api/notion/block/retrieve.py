import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from notion_client import Client


router: APIRouter = APIRouter()
notion: Client = Client(auth=os.environ["NOTION_API_TOKEN"])


@router.get("/retrieve/{b_id}")
async def retrieve(b_id: str, response_class=JSONResponse):
    return notion.blocks.retrieve(b_id)
