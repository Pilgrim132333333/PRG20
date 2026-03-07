# api/routes/users.py

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    # 1. user_data 已被 Pydantic 按 UserCreate 校验
    # 2. 用 ORM 创建 User 对象（models）并保存
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),  # 加密后存储
        role=user_data.role,
    )
    db.add(user)
    await db.commit()
    # 3. 按 UserResponse 的字段返回，自动不包含 hashed_password
    return user