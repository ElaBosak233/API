import os
from typing import Optional

from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from notion_lab.converter import HtmlCvt, MDCvt

router: APIRouter = APIRouter()


@router.get("/")
async def index():
    return "NOTION API"


# 以 html 的形式输出文章所有内容
@router.get("/{page_id}", response_class=HTMLResponse)
async def stats(page_id: str, fmt: Optional[str] = "html"):
    r = ""
    if fmt == "html":
        cvt = HtmlCvt(api_token=os.environ["NOTION_API_TOKEN"], block_id=page_id, is_page=True)
        r = cvt.convert()
    elif fmt == "md":
        cvt = MDCvt(api_token=os.environ["NOTION_API_TOKEN"], block_id=page_id, is_page=True)
        r = cvt.convert()
    return r
