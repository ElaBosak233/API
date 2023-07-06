import os

from fastapi import APIRouter
from .block import router as block_router
from fastapi.responses import JSONResponse
from notion_lab.database import DB

router: APIRouter = APIRouter()
router.include_router(block_router, prefix="/block")


@router.get("/")
async def index():
    return "NOTION API"


# # 以 html 的形式输出块所有内容
# @router.get("/block/{block_id}", response_class=Response)
# async def page(block_id: str, is_page: Optional[bool] = False, fmt: Optional[str] = "html"):
#     r = ""
#     if fmt == "html":
#         cvt = HtmlCvt(api_token=os.environ["NOTION_API_TOKEN"], block_id=block_id.replace("-", ""), is_page=is_page)
#         r = cvt.convert()
#     elif fmt == "md":
#         cvt = MDCvt(api_token=os.environ["NOTION_API_TOKEN"], block_id=block_id.replace("-", ""), is_page=is_page)
#         r = cvt.convert()
#     return r


# 获取数据库内容
@router.get("/database/{database_id}", response_class=JSONResponse)
def database(database_id: str):
    r = []
    db = DB(api_token=os.environ["NOTION_API_TOKEN"], database_id=database_id)
    for i in db.traversal():
        r.append(i)
    return r
