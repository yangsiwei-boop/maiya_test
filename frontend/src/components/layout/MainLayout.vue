<template>
  <div class="main-layout">
    <!-- 顶部导航 -->
    <div class="top-bar">
      <div class="container">
        <div class="top-bar-content">
          <div class="top-bar-text">欢迎来到购物中心!</div>
          <div class="top-bar-links">
            <template v-if="userStore.isLoggedIn">
              <span>{{ userStore.user?.username }}</span>
              <a href="/user">个人中心</a>
              <a @click="handleLogout">退出登录</a>
            </template>
            <template v-else>
              <router-link to="/login">登录</router-link>
              <router-link to="/register">注册</router-link>
            </template>
            <router-link to="/orders">我的订单</router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 主导航 -->
    <div class="main-header">
      <div class="container header-content">
        <router-link to="/" class="logo">🛍️ 购物中心</router-link>
        <nav class="nav-menu">
          <router-link to="/home">首页</router-link>
          <router-link to="/products?category=1">手机</router-link>
          <router-link to="/products?category=2">电脑</router-link>
          <router-link to="/products?category=3">电视</router-link>
          <router-link to="/products?category=4">耳机</router-link>
        </nav>
        <div class="search-box">
          <input
            v-model="searchKeyword"
            type="text"
            placeholder="搜索商品"
            @keyup.enter="handleSearch"
          />
          <button @click="handleSearch">搜索</button>
        </div>
        <router-link to="/cart" class="cart-icon">
          🛒
          <span v-if="cartStore.totalQuantity > 0" class="cart-badge">
            {{ cartStore.totalQuantity }}
          </span>
        </router-link>
      </div>
    </div>

    <!-- 主要内容 -->
    <div class="main-content">
      <router-view />
    </div>

    <!-- 底部 -->
    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-section">
            <h3>购物指南</h3>
            <ul>
              <li><a href="#">购物流程</a></li>
              <li><a href="#">常见问题</a></li>
              <li><a href="#">退换货政策</a></li>
              <li><a href="#">配送说明</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h3>支付方式</h3>
            <ul>
              <li><a href="#">在线支付</a></li>
              <li><a href="#">银行转账</a></li>
              <li><a href="#">货到付款</a></li>
              <li><a href="#">分期付款</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h3>售后服务</h3>
            <ul>
              <li><a href="#">售后政策</a></li>
              <li><a href="#">价格保护</a></li>
              <li><a href="#">退款说明</a></li>
              <li><a href="#">取消订单</a></li>
            </ul>
          </div>
          <div class="footer-section">
            <h3>关于我们</h3>
            <ul>
              <li><a href="#">公司介绍</a></li>
              <li><a href="#">联系我们</a></li>
              <li><a href="#">加入我们</a></li>
              <li><a href="#">友情链接</a></li>
            </ul>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© 2026 购物中心 版权所有 | 客服热线:400-888-8888</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useCartStore } from '../../stores/cart'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const cartStore = useCartStore()

const searchKeyword = ref('')

// 初始化购物车
if (userStore.isLoggedIn) {
  cartStore.fetchCart()
}

const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    router.push({
      name: 'ProductList',
      query: { keyword: searchKeyword.value }
    })
  }
}

const handleLogout = () => {
  userStore.logout()
  cartStore.cartItems = []
  ElMessage.success('退出登录成功')
  router.push('/login')
}
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 顶部导航 */
.top-bar {
  background-color: #f8f8f8;
  border-bottom: 1px solid #e5e5e5;
  padding: 8px 0;
  font-size: 12px;
}

.top-bar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top-bar-links a {
  color: #666;
  margin-left: 20px;
  cursor: pointer;
  transition: color 0.3s;
}

.top-bar-links a:hover {
  color: #ff6700;
}

/* 主导航 */
.main-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.header-content {
  display: flex;
  align-items: center;
  height: 80px;
}

.logo {
  font-size: 28px;
  font-weight: bold;
  color: #ff6700;
  margin-right: 50px;
  cursor: pointer;
}

.nav-menu {
  display: flex;
  flex: 1;
}

.nav-menu a {
  padding: 0 20px;
  height: 80px;
  line-height: 80px;
  font-size: 16px;
  color: #333;
  transition: color 0.3s;
}

.nav-menu a:hover,
.nav-menu a.router-link-active {
  color: #ff6700;
}

.search-box {
  display: flex;
  margin-left: auto;
}

.search-box input {
  width: 250px;
  height: 40px;
  padding: 0 15px;
  border: 1px solid #e5e5e5;
  border-radius: 20px 0 0 20px;
  outline: none;
  font-size: 14px;
}

.search-box button {
  width: 60px;
  height: 40px;
  background-color: #ff6700;
  border: none;
  border-radius: 0 20px 20px 0;
  color: #fff;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.search-box button:hover {
  background-color: #ff4500;
}

.cart-icon {
  margin-left: 30px;
  position: relative;
  cursor: pointer;
  font-size: 24px;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background-color: #ff6700;
  color: #fff;
  font-size: 12px;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 主内容区 */
.main-content {
  flex: 1;
}

/* 底部 */
.footer {
  background-color: #fff;
  margin-top: 60px;
  padding: 40px 0 20px;
  border-top: 1px solid #e5e5e5;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h3 {
  font-size: 16px;
  margin-bottom: 20px;
  color: #333;
}

.footer-section ul {
  list-style: none;
}

.footer-section ul li {
  margin-bottom: 10px;
}

.footer-section ul li a {
  color: #666;
  font-size: 14px;
  transition: color 0.3s;
}

.footer-section ul li a:hover {
  color: #ff6700;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e5e5e5;
  color: #999;
  font-size: 14px;
}
</style>
