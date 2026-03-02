from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import engine, Base
from routers import auth, products, cart, orders, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    Base.metadata.create_all(bind=engine)
    yield
    # 关闭时的清理工作
    pass


app = FastAPI(
    title="购物中心 API",
    description="购物中心后端API接口文档",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(products.router, prefix="/api/products", tags=["商品"])
app.include_router(cart.router, prefix="/api/cart", tags=["购物车"])
app.include_router(orders.router, prefix="/api/orders", tags=["订单"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])


@app.get("/")
async def root():
    return {"message": "购物中心 API 服务正在运行"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
