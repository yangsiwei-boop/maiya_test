import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { User } from '../types'
import { authApi } from '../api'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string>('')
  const isLoggedIn = ref<boolean>(false)

  // 初始化：从localStorage恢复登录状态
  const init = () => {
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')

    if (savedToken && savedUser) {
      token.value = savedToken
      user.value = JSON.parse(savedUser)
      isLoggedIn.value = true
    }
  }

  // 登录
  const login = async (phone: string, password: string) => {
    const response = await authApi.login({ phone, password })

    token.value = response.access_token
    user.value = response.user
    isLoggedIn.value = true

    // 保存到localStorage
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))

    return response
  }

  // 注册
  const register = async (phone: string, password: string, username?: string) => {
    const response = await authApi.register({ phone, password, username })

    token.value = response.access_token
    user.value = response.user
    isLoggedIn.value = true

    // 保存到localStorage
    localStorage.setItem('token', response.access_token)
    localStorage.setItem('user', JSON.stringify(response.user))

    return response
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = ''
    isLoggedIn.value = false

    // 清除localStorage
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 更新用户信息
  const updateUser = (newUser: User) => {
    user.value = newUser
    localStorage.setItem('user', JSON.stringify(newUser))
  }

  return {
    user,
    token,
    isLoggedIn,
    init,
    login,
    register,
    logout,
    updateUser
  }
})
