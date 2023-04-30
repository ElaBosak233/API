import codecs

import uvicorn
from fastapi import FastAPI, Request, APIRouter, applications
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from api.mcbbs import router as mcbbs_router
from api.notion import router as notion_router

__VERSION__ = "1.0.0"
__TITLE__ = "埃拉の应用程序接口"
__DESCRIPTION__ = codecs.open("README.md", "r", "utf-8").read()

# FastAPI 对象
app: FastAPI = FastAPI(
    title=__TITLE__,
    version=__VERSION__,
    description=__DESCRIPTION__,
    redoc_url=None
)


# 重写 Swagger UI 的 CDN
def swagger_monkey_patch(*args, **kwargs):
    return get_swagger_ui_html(
        *args,
        **kwargs,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="https://e23.dev/fav.svg"
    )


applications.get_swagger_ui_html = swagger_monkey_patch

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


# 挂载静态文件
app.mount("/static", StaticFiles(directory="./static"), name="static")

# 挂载路由
app.include_router(router, tags=["主路由"])  # 挂载主路由
app.include_router(mcbbs_router, prefix="/mcbbs", tags=["MCBBS"])  # 挂载 MCBBS 路由
app.include_router(notion_router, prefix="/notion", tags=["Notion"])  # 挂载 Notion 路由

# 注册跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app="app:app", host="0.0.0.0", port=8080, reload=True, debug=True)
