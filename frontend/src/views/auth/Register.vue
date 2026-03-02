<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧 -->
      <div class="login-left">
        <div class="login-left-content">
          <h1>加入购物中心</h1>
          <p>注册即享新人大礼包</p>
          <ul class="login-features">
            <li>100元新人红包</li>
            <li>首单免运费</li>
            <li>会员专属折扣</li>
            <li>积分加倍优惠</li>
            <li>生日专属礼品</li>
          </ul>
        </div>
      </div>

      <!-- 右侧表单 -->
      <div class="login-right">
        <div class="logo" @click="goHome">🛍️ 购物中心</div>
        <div class="form-title">
          <router-link to="/login">登录</router-link>
          |
          <router-link to="/register" class="active">注册</router-link>
        </div>

        <!-- 注册表单 -->
        <el-form ref="registerFormRef" :model="registerForm" :rules="registerRules">
          <el-form-item prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              prefix-icon="Iphone"
              size="large"
            />
          </el-form-item>

          <el-form-item prop="code">
            <div class="verify-code">
              <el-input
                v-model="registerForm.code"
                placeholder="请输入验证码"
                prefix-icon="Key"
                size="large"
              />
              <el-button
                size="large"
                :disabled="codeCountdown > 0"
                @click="sendCode"
              >
                {{ codeCountdown > 0 ? `${codeCountdown}s` : '获取验证码' }}
              </el-button>
            </div>
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码(6-20位)"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              prefix-icon="Lock"
              size="large"
              show-password
            />
          </el-form-item>

          <el-button type="primary" size="large" class="submit-btn" :loading="loading" @click="handleRegister">
            注册
          </el-button>
        </el-form>

        <!-- 第三方登录 -->
        <div class="divider">
          <span>其他注册方式</span>
        </div>

        <div class="social-login">
          <div class="social-btn" title="微信注册">💬</div>
          <div class="social-btn" title="QQ注册">🐧</div>
        </div>

        <div class="agreement">
          注册即表示同意《用户协议》和《隐私政策》
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const registerFormRef = ref()
const loading = ref(false)
const codeCountdown = ref(0)

const registerForm = reactive({
  phone: '',
  code: '',
  password: '',
  confirmPassword: ''
})

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const registerRules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度为6-20位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const sendCode = async () => {
  if (!registerForm.phone) {
    ElMessage.warning('请先输入手机号')
    return
  }

  try {
    const result = await userStore.register('', '')
    ElMessage.success(`验证码已发送: ${result.code}`)

    codeCountdown.value = 60
    const timer = setInterval(() => {
      codeCountdown.value--
      if (codeCountdown.value <= 0) {
        clearInterval(timer)
      }
    }, 1000)
  } catch (error: any) {
    ElMessage.error('发送验证码失败')
  }
}

const handleRegister = async () => {
  try {
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    loading.value = true
    await userStore.register(registerForm.phone, registerForm.password)

    ElMessage.success('注册成功')
    router.push('/home')
  } catch (error: any) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}
</script>

<style scoped src="../auth/Login.vue?vue&type=style&index=0&lang=css"></style>
