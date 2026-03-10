# FastAPI 入口：注册路由、CORS、 lifespan
# main.py （临时测试部分）
from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv() 

print("当前读取到的 DATABASE_URL:", os.getenv("DATABASE_URL"))
print("SECRET_KEY 是否存在:", "有" if os.getenv("SECRET_KEY") else "无")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}