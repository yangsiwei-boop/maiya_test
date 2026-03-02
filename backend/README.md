# 购物中心后端API

基于 FastAPI 的购物中心后端服务。

## 技术栈

- FastAPI - Web框架
- SQLAlchemy - ORM
- SQLite - 数据库
- Pydantic - 数据验证
- JWT - 认证

## 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

## 初始化数据库

```bash
python init_data.py
```

测试账号: 13800138000 / 123456

## 运行服务

```bash
python main.py
```

或使用 uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API文档

启动服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API接口

### 认证模块 `/api/auth`
- POST `/register` - 用户注册
- POST `/login` - 用户登录
- GET `/me` - 获取当前用户信息
- POST `/send-code` - 发送验证码

### 商品模块 `/api/products`
- GET `/products` - 获取商品列表
- GET `/products/{id}` - 获取商品详情
- GET `/categories` - 获取分类列表
- GET `/hot` - 获取热门商品
- GET `/new` - 获取新品
- POST `/products/{id}/favorite` - 收藏商品

### 购物车模块 `/api/cart`
- GET `/` - 获取购物车
- POST `/` - 添加商品到购物车
- PUT `/{item_id}` - 更新购物车商品数量
- DELETE `/{item_id}` - 删除购物车商品

### 订单模块 `/api/orders`
- POST `/` - 创建订单
- GET `/` - 获取订单列表
- GET `/{order_id}` - 获取订单详情
- PUT `/{order_id}/cancel` - 取消订单
- PUT `/{order_id}/pay` - 支付订单
- PUT `/{order_id}/confirm` - 确认收货

### 用户模块 `/api/users`
- GET `/addresses` - 获取地址列表
- POST `/addresses` - 添加地址
- PUT `/addresses/{id}` - 更新地址
- DELETE `/addresses/{id}` - 删除地址
- GET `/stats` - 获取用户统计信息
