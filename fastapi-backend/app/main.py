"""FastAPI 入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import questions, courseworks, materials, auth

app = FastAPI(title="AI Programming Question Bank API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(questions.router, prefix="/api")
app.include_router(courseworks.router, prefix="/api")
app.include_router(materials.router, prefix="/api")
app.include_router(auth.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "AI Programming Question Bank API"}
