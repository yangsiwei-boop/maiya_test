# 登录验证流程说明

## 修改内容

### 后端修改

#### 1. 更新 `schemas.py`
- 在 `UserLogin` schema 中添加 `code` 字段（必填）

#### 2. 更新 `routers/auth.py`

##### 验证码存储
```python
# 验证码存储（生产环境应使用Redis）
verification_codes: Dict[str, Dict] = {}
```

##### 发送验证码接口增强
- 添加频率限制（60秒内只能发送一次）
- 验证码有效期：5分钟
- 返回过期时间信息

##### 登录接口逻辑修改
**原逻辑**：
1. 验证账号密码
2. 生成Token

**新逻辑**：
1. **验证验证码**
   - 检查验证码是否存在
   - 检查验证码是否过期
   - 验证码是否正确
2. **验证账号密码**
   - 验证手机号是否存在
   - 验证密码是否正确
3. **生成Token**

### 前端修改

#### 1. 更新 `Login.vue`
- 添加验证码输入框
- 添加"获取验证码"按钮
- 实现60秒倒计时功能
- 验证码必填验证（6位数字）

#### 2. 更新 `stores/user.ts`
- `login` 方法添加 `code` 参数

#### 3. 更新 `api/index.ts`
- `authApi.login` 接口添加 `code` 字段
- `authApi.sendCode` 接口返回类型更新

## 使用流程

### 用户登录流程

1. **输入手机号**
   ```
   用户输入手机号：13800138000
   ```

2. **获取验证码**
   - 点击"获取验证码"按钮
   - 后端生成6位随机验证码
   - 验证码有效期5分钟
   - 60秒内不能重复发送

   **接口**: `POST /api/auth/send-code?phone=13800138000`

   **响应**:
   ```json
   {
     "message": "验证码发送成功",
     "code": "123456",  // 生产环境不返回
     "expires_in": 300
   }
   ```

3. **输入验证码**
   ```
   用户输入收到的验证码：123456
   ```

4. **输入密码**
   ```
   用户输入密码：123456
   ```

5. **点击登录**
   - 先验证验证码
   - 再验证账号密码
   - 验证通过后生成Token

   **接口**: `POST /api/auth/login`

   **请求体**:
   ```json
   {
     "phone": "13800138000",
     "password": "123456",
     "code": "123456"
   }
   ```

   **响应**:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer",
     "user": {
       "id": 1,
       "phone": "13800138000",
       "username": "张三",
       "level": "黄金会员",
       "points": 1280
     }
   }
   ```

## 错误处理

### 验证码错误
```json
{
  "detail": "请先获取验证码"
}
```

```json
{
  "detail": "验证码已过期，请重新获取"
}
```

```json
{
  "detail": "验证码错误"
}
```

### 账号密码错误
```json
{
  "detail": "手机号或密码错误"
}
```

### 频率限制
```json
{
  "detail": "验证码发送过于频繁，请30秒后再试"
}
```

## 测试账号

- **手机号**: 13800138000
- **密码**: 123456
- **验证码**: 点击"获取验证码"按钮获得（测试环境会返回验证码）

## 安全建议

### 生产环境注意事项

1. **使用Redis存储验证码**
   - 替换内存存储 `verification_codes`
   - 利用Redis的TTL自动过期机制

2. **真正的短信服务**
   - 集成阿里云、腾讯云等短信服务
   - 不要在响应中返回验证码

3. **验证码复杂度**
   - 可考虑增加图形验证码
   - 防止短信轰炸

4. **IP限制**
   - 同一IP每小时发送次数限制
   - 同一手机号每天发送次数限制

5. **日志记录**
   - 记录验证码发送日志
   - 记录登录失败日志
   - 异常登录告警

## API文档

### 发送验证码

**端点**: `POST /api/auth/send-code`

**参数**:
- `phone` (query): 手机号

**响应**:
```json
{
  "message": "验证码发送成功",
  "code": "123456",
  "expires_in": 300
}
```

**状态码**:
- `200`: 发送成功
- `400`: 手机号格式错误
- `429`: 发送频率过高

### 用户登录

**端点**: `POST /api/auth/login`

**请求体**:
```json
{
  "phone": "string",
  "password": "string",
  "code": "string"
}
```

**响应**:
```json
{
  "access_token": "string",
  "token_type": "bearer",
  "user": {
    "id": "integer",
    "phone": "string",
    "username": "string",
    "avatar": "string|null",
    "level": "string",
    "points": "integer",
    "created_at": "datetime"
  }
}
```

**状态码**:
- `200`: 登录成功
- `400`: 验证码错误或已过期
- `401`: 手机号或密码错误
