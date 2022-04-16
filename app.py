from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

# FastAPI 对象
app: FastAPI = FastAPI()
pages: Jinja2Templates = Jinja2Templates(directory="__pages__")


# 创建 Serverless 函数
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


# 首页
@app.get("/")
async def index(request: Request):
    return pages.TemplateResponse("index.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}