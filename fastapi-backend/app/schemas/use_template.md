# schemas/user.py

# 前端注册时提交的数据（不包含密码哈希）
class UserCreate(BaseModel):
    username: str
    email: str
    password: str          # 明文密码，后端会加密
    role: str

# 接口返回给前端的数据（不包含密码）
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    created_at: datetime