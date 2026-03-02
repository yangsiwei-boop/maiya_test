# 购物中心后端API

基于 FastAPI + MySQL 的购物中心后端服务。

## 技术栈

- FastAPI - Web框架
- SQLAlchemy - ORM
- MySQL - 数据库
- PyMySQL - MySQL驱动
- Pydantic - 数据验证
- JWT - 认证
- Alembic - 数据库迁移

## 环境要求

- Python 3.8+
- MySQL 5.7+ / MySQL 8.0+

## 安装步骤

### 1. 安装MySQL数据库

确保已安装MySQL数据库服务。

### 2. 创建数据库

使用提供的SQL脚本创建数据库和表：

```bash
# 方法1：使用命令行
mysql -u root -p < init_mysql.sql

# 方法2：登录MySQL后执行
mysql -u root -p
source init_mysql.sql;
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，修改数据库连接信息：

```env
MYSQL_USER=root
MYSQL_PASSWORD=你的MySQL密码
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=shopping_mall
```

### 4. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 5. 初始化测试数据（可选）

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

## 测试数据库连接

在Python中测试MySQL连接：

```python
from database import test_connection
test_connection()
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
