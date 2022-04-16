from fastapi import FastAPI, Request

# FastAPI 对象
app: FastAPI = FastAPI()


# 创建 Serverless 函数
@app.middleware("http")
async def add_no_cache_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache"
    return response


# 首页
@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}