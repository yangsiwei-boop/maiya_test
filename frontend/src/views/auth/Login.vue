<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧 -->
      <div class="login-left">
        <div class="login-left-content">
          <h1>欢迎来到购物中心</h1>
          <p>随时随地，享受购物乐趣</p>
          <ul class="login-features">
            <li>正品保障，假一赔十</li>
            <li>7天无理由退换货</li>
            <li>全国联保，售后无忧</li>
            <li>极速物流，次日送达</li>
            <li>会员专享优惠折扣</li>
          </ul>
        </div>
      </div>

      <!-- 右侧表单 -->
      <div class="login-right">
        <div class="logo" @click="goHome">🛍️ 购物中心</div>
        <div class="form-title">
          <router-link to="/login" class="active">登录</router-link>
          |
          <router-link to="/register">注册</router-link>
        </div>

        <!-- 登录表单 -->
        <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules" @submit.prevent="handleLogin">
          <el-form-item prop="phone">
            <el-input
              v-model="loginForm.phone"
              placeholder="请输入手机号"
              prefix-icon="Iphone"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="code">
            <div class="code-input-wrapper">
              <el-input
                v-model="loginForm.code"
                placeholder="请输入验证码"
                prefix-icon="Key"
                size="large"
                maxlength="6"
              />
              <el-button
                type="primary"
                size="large"
                :disabled="countdown > 0"
                :loading="sendingCode"
                @click="handleSendCode"
                class="send-code-btn"
              >
                {{ countdown > 0 ? `${countdown}秒后重试` : '获取验证码' }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>

          <div class="form-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <a class="forgot-password">忘记密码?</a>
          </div>

          <el-button type="primary" size="large" class="submit-btn" :loading="loading" @click="handleLogin">
            登录
          </el-button>
        </el-form>

        <!-- 第三方登录 -->
        <div class="divider">
          <span>其他登录方式</span>
        </div>

        <div class="social-login">
          <div class="social-btn" title="微信登录">💬</div>
          <div class="social-btn" title="QQ登录">🐧</div>
          <div class="social-btn" title="支付宝登录">💳</div>
          <div class="social-btn" title="微博登录">🔶</div>
        </div>

        <div class="agreement">
          登录即表示同意《用户协议》和《隐私政策》
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loginFormRef = ref()
const loading = ref(false)
const rememberMe = ref(false)
const sendingCode = ref(false)
const countdown = ref(0)

const loginForm = reactive({
  phone: '13800138000',
  password: '123456',
  code: ''
})

const loginRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码必须是6位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 发送验证码
const handleSendCode = async () => {
  // 先验证手机号
  try {
    await loginFormRef.value.validateField('phone')
  } catch (error) {
    return
  }

  try {
    sendingCode.value = true
    const response = await axios.post('/api/auth/send-code', null, {
      params: { phone: loginForm.phone }
    })

    ElMessage.success(`验证码已发送: ${response.data.code}`)

    // 开始倒计时
    countdown.value = 60
    const timer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '验证码发送失败')
  } finally {
    sendingCode.value = false
  }
}

// 登录
const handleLogin = async () => {
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    loading.value = true

    // 调用登录接口，传入手机号、密码和验证码
    await userStore.login(loginForm.phone, loginForm.password, loginForm.code)

    ElMessage.success('登录成功')

    // 跳转到之前的页面或首页
    const redirect = route.query.redirect as string
    router.push(redirect || '/home')
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-container {
  width: 100%;
  max-width: 900px;
  background-color: #fff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  display: flex;
}

/* 左侧 */
.login-left {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 60px 40px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.login-left::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.login-left-content {
  position: relative;
  z-index: 2;
}

.login-left h1 {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 20px;
}

.login-left p {
  font-size: 16px;
  opacity: 0.9;
  line-height: 1.6;
  margin-bottom: 30px;
}

.login-features {
  list-style: none;
}

.login-features li {
  padding: 12px 0;
  font-size: 15px;
  display: flex;
  align-items: center;
}

.login-features li::before {
  content: '✓';
  width: 24px;
  height: 24px;
  background-color: rgba(255,255,255,0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  flex-shrink: 0;
}

/* 右侧 */
.login-right {
  width: 450px;
  padding: 50px 40px;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: #ff6700;
  margin-bottom: 10px;
  cursor: pointer;
}

.form-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 30px;
}

.form-title a {
  color: #666;
  margin: 0 5px;
  transition: color 0.3s;
}

.form-title a:hover,
.form-title a.router-link-active {
  color: #ff6700;
  font-weight: bold;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 14px;
}

.forgot-password {
  color: #666;
  cursor: pointer;
}

.forgot-password:hover {
  color: #ff6700;
}

.submit-btn {
  width: 100%;
  height: 50px;
  background: linear-gradient(135deg, #ff6700 0%, #ff4500 100%);
  border: none;
  border-radius: 25px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
}

.divider {
  display: flex;
  align-items: center;
  margin: 30px 0;
  color: #999;
  font-size: 14px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #e5e5e5;
}

.divider span {
  padding: 0 15px;
}

.social-login {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.social-btn {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 1px solid #e5e5e5;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.social-btn:hover {
  border-color: #ff6700;
  color: #ff6700;
  transform: translateY(-3px);
}

.agreement {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #999;
}

/* 验证码输入框样式 */
.code-input-wrapper {
  display: flex;
  gap: 10px;
  width: 100%;
}

.code-input-wrapper .el-input {
  flex: 1;
}

.send-code-btn {
  white-space: nowrap;
  min-width: 120px;
}
</style>
