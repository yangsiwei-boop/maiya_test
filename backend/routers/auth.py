from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import random
from typing import Dict

from database import get_db
from models import User
from schemas import UserCreate, UserLogin, Token, UserResponse

router = APIRouter()

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30天

# 验证码存储（生产环境应使用Redis）
verification_codes: Dict[str, Dict] = {}


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # 检查手机号是否已注册
    existing_user = db.query(User).filter(User.phone == user_data.phone).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该手机号已注册"
        )

    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        phone=user_data.phone,
        password_hash=hashed_password,
        username=user_data.username or f"用户{user_data.phone[-4:]}",
        level="普通会员",
        points=0
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 生成Token
    access_token = create_access_token(
        data={"sub": new_user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        user=UserResponse.from_orm(new_user)
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # 第一步：验证验证码
    if user_data.phone not in verification_codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请先获取验证码"
        )

    stored_code_data = verification_codes[user_data.phone]

    # 检查验证码是否过期
    if datetime.utcnow() > stored_code_data["expires"]:
        # 删除过期的验证码
        del verification_codes[user_data.phone]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码已过期，请重新获取"
        )

    # 验证验证码是否正确
    if user_data.code != stored_code_data["code"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="验证码错误"
        )

    # 验证码验证通过，删除已使用的验证码
    del verification_codes[user_data.phone]

    # 第二步：验证账号密码
    user = db.query(User).filter(User.phone == user_data.phone).first()
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="手机号或密码错误"
        )

    # 第三步：生成Token
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(
        access_token=access_token,
        user=UserResponse.from_orm(user)
    )


@router.post("/send-code")
async def send_code(phone: str, db: Session = Depends(get_db)):
    """
    发送验证码
    - 生成6位随机验证码
    - 验证码有效期5分钟
    - 生产环境应调用短信服务API发送
    """
    # 检查发送频率（60秒内只能发送一次）
    if phone in verification_codes:
        last_sent_time = verification_codes[phone]["created"]
        if (datetime.utcnow() - last_sent_time).total_seconds() < 60:
            remaining = 60 - int((datetime.utcnow() - last_sent_time).total_seconds())
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"验证码发送过于频繁，请{remaining}秒后再试"
            )

    # 生成6位随机验证码
    code = str(random.randint(100000, 999999))

    # 保存验证码，设置5分钟过期
    verification_codes[phone] = {
        "code": code,
        "created": datetime.utcnow(),
        "expires": datetime.utcnow() + timedelta(minutes=5)
    }

    # 在实际应用中，这里应该调用短信服务API发送验证码
    # 例如: send_sms(phone, code)
    # 这里我们直接返回验证码用于测试
    return {
        "message": "验证码发送成功",
        "code": code,  # 生产环境应移除此字段
        "expires_in": 300  # 5分钟有效期
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)


@router.put("/me")
async def update_user_info(
    username: str = None,
    avatar: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if username:
        current_user.username = username
    if avatar:
        current_user.avatar = avatar

    db.commit()
    db.refresh(current_user)

    return {"message": "用户信息更新成功", "user": UserResponse.from_orm(current_user)}
