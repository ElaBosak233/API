import uvicorn
from fastapi import FastAPI, Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from mcbbs.main import router as mcbbs_router

__VERSION__ = "1.0.0 alpha"
__TITLE__ = "Ela's API"
__DESCRIPTION__ = """
Ela's API is a RESTful API for the Ela's project.

## 详情请见
- [GitHub README](https://github.com/ElaBosak233/api/blob/main/README.md)
"""

# FastAPI 对象
app: FastAPI = FastAPI(
    title=__TITLE__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    contact={
        "name": "Ela",
        "url": "https://github.com/ElaBosak233",
        "email": "ElaBosak233@e23.dev"
    },
    license_info={
        "name": "GNU GENERAL PUBLIC LICENSE v3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
    },
    redoc_url=None
)

# 路由对象
router: APIRouter = APIRouter()

# 模板对象
pages: Jinja2Templates = Jinja2Templates(directory="pages")


# 创建 Serverless 函数
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


# 首页
@router.get("/")
async def index(request: Request):
    return pages.TemplateResponse("index.html", {"request": request})


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 挂载静态文件
app.mount("/statics", StaticFiles(directory="./statics"), name="statics")


# 挂载路由
app.include_router(router)  # 挂载主路由
app.include_router(mcbbs_router, prefix="/mcbbs", tags=["MCBBS 我的世界中文论坛"])  # 挂载 MCBBS 路由


# 注册跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=9000, reload=True, debug=True)
