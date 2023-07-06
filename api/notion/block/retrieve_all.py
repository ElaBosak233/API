import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from notion_client import Client


router: APIRouter = APIRouter()
notion: Client = Client(auth=os.environ["NOTION_API_TOKEN"])


@router.get("/retrieve_all/{b_id}")
async def retrieve_all(b_id: str):
    return notion.blocks.children.list(b_id)["results"]
