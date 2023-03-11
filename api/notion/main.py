import os

from fastapi import APIRouter
from notion_client import Client
from fastapi.responses import HTMLResponse

from .utils.HtmlParser import HtmlParser

router: APIRouter = APIRouter()
notion: Client = Client(auth=os.environ.get("NOTION_API_KEY"))


@router.get("/")
async def index():
    return "NOTION API"


# 以 html 的形式输出文章所有内容
@router.get("/{page_id}", response_class=HTMLResponse)
async def stats(page_id: str):
    children = notion.blocks.children.list(block_id=page_id)
    r = HtmlParser(children).export()
    return r
