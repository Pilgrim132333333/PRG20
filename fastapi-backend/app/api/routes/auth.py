"""注册 / 登录 API"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.crud import user as user_crud
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=255)


class LoginBody(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=255)


def _hash_password(plain: str) -> str:
    return pwd_context.hash(plain)


def _verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


@router.post("/register")
def register(body: RegisterBody, db: Session = Depends(get_db)):
    """注册：写入 Users 表"""
    if user_crud.get_by_username(db, body.username.strip()):
        raise HTTPException(status_code=400, detail="Username already exists")
    if user_crud.get_by_email(db, body.email.strip().lower()):
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = _hash_password(body.password)
    try:
        user = user_crud.create_user(
            db,
            username=body.username.strip(),
            email=body.email.strip().lower(),
            password_hash=password_hash,
        )
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username or email already exists") from None

    return {
        "ok": True,
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
    }


@router.post("/login")
def login(body: LoginBody, db: Session = Depends(get_db)):
    """登录：校验用户名与密码"""
    user: User | None = user_crud.get_by_username(db, body.username.strip())
    if not user or not _verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    return {
        "ok": True,
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "role": "student",
    }
