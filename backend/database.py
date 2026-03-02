from sqlalchemy import create_engine
from sqlalchemy import pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# MySQL数据库配置
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "shopping_mall")

# MySQL连接URL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# 创建数据库引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # 自动检测连接是否有效
    pool_recycle=3600,   # 1小时后回收连接
    echo=False           # 设置为True可以看到SQL日志
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()


# 依赖项：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 测试数据库连接
def test_connection():
    """测试数据库连接是否正常"""
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ MySQL数据库连接成功!")
        return True
    except Exception as e:
        print(f"❌ MySQL数据库连接失败: {e}")
        return False
