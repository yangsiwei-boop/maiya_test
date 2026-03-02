<template>
  <div class="user-center-page">
    <div class="container">
      <!-- 用户信息头部 -->
      <div class="user-header">
        <div class="user-header-content">
          <div class="user-avatar">{{ userStore.user?.username?.[0] || '👤' }}</div>
          <div class="user-info">
            <div class="user-name">{{ userStore.user?.username }}</div>
            <div class="user-level">{{ userStore.user?.level }}</div>
            <div class="user-stats">
              <div class="stat-item">
                <span>{{ stats.points }}</span> 积分
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 主体内容 -->
      <div class="main-layout">
        <!-- 左侧菜单 -->
        <div class="sidebar">
          <div class="menu-card">
            <div class="menu-item active" @click="currentTab = 'orders'">
              <span class="menu-icon">📋</span>
              我的订单
            </div>
            <div class="menu-item" @click="currentTab = 'address'">
              <span class="menu-icon">📍</span>
              收货地址
            </div>
            <div class="menu-item" @click="handleLogout">
              <span class="menu-icon">🚪</span>
              退出登录
            </div>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="main-content">
          <!-- 订单列表 -->
          <div v-if="currentTab === 'orders'" class="content-card">
            <h2 class="card-title">我的订单</h2>
            <div class="order-tabs">
              <div
                class="order-tab"
                :class="{ active: orderStatus === '' }"
                @click="orderStatus = ''; loadOrders()"
              >
                全部订单
              </div>
              <div
                class="order-tab"
                :class="{ active: orderStatus === 'pending' }"
                @click="orderStatus = 'pending'; loadOrders()"
              >
                待付款
              </div>
              <div
                class="order-tab"
                :class="{ active: orderStatus === 'shipped' }"
                @click="orderStatus = 'shipped'; loadOrders()"
              >
                待收货
              </div>
              <div
                class="order-tab"
                :class="{ active: orderStatus === 'completed' }"
                @click="orderStatus = 'completed'; loadOrders()"
              >
                待评价
              </div>
            </div>
            <div v-loading="loading" class="simple-order-list">
              <div v-for="order in orders" :key="order.id" class="simple-order-item">
                <div class="order-info">
                  <span class="order-number">{{ order.order_number }}</span>
                  <span class="order-time">{{ formatDate(order.created_at) }}</span>
                </div>
                <div class="order-status">{{ getStatusText(order.status) }}</div>
                <div class="order-amount">¥{{ order.pay_amount }}</div>
              </div>
            </div>
          </div>

          <!-- 地址管理 -->
          <div v-if="currentTab === 'address'" class="content-card">
            <h2 class="card-title">收货地址</h2>
            <el-button type="primary" @click="showAddressDialog = true">
              添加新地址
            </el-button>
            <div class="address-grid">
              <div
                v-for="addr in addresses"
                :key="addr.id"
                class="address-card"
              >
                <div v-if="addr.tag" class="address-tag" :class="addr.tag">
                  {{ addr.tag }}
                </div>
                <div class="address-name">{{ addr.receiver_name }}</div>
                <div class="address-phone">{{ addr.receiver_phone }}</div>
                <div class="address-detail">
                  {{ addr.province }} {{ addr.city }} {{ addr.district }} {{ addr.detail }}
                </div>
                <div class="address-actions">
                  <el-button link @click="editAddress(addr)">编辑</el-button>
                  <el-button link type="danger" @click="deleteAddress(addr.id)">
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { userApi, orderApi } from '../../api'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Address, Order } from '../../types'

const router = useRouter()
const userStore = useUserStore()

const currentTab = ref('orders')
const orderStatus = ref('')
const orders = ref<Order[]>([])
const addresses = ref<Address[]>([])
const stats = ref<any>({})
const loading = ref(false)
const showAddressDialog = ref(false)

const loadOrders = async () => {
  try {
    loading.value = true
    orders.value = await orderApi.getOrders({ status: orderStatus.value })
  } catch (error) {
    ElMessage.error('加载订单失败')
  } finally {
    loading.value = false
  }
}

const loadAddresses = async () => {
  try {
    addresses.value = await userApi.getAddresses()
  } catch (error) {
    ElMessage.error('加载地址失败')
  }
}

const loadStats = async () => {
  try {
    stats.value = await userApi.getUserStats()
  } catch (error) {
    console.error('加载统计信息失败:', error)
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待付款',
    paid: '已付款',
    shipped: '已发货',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

const editAddress = (addr: Address) => {
  // TODO: 实现编辑地址功能
  ElMessage.info('编辑地址功能待实现')
}

const deleteAddress = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个地址吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await userApi.deleteAddress(id)
    ElMessage.success('删除成功')
    loadAddresses()
  } catch (error) {
    // 用户取消
  }
}

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}

onMounted(() => {
  loadOrders()
  loadAddresses()
  loadStats()
})
</script>

<style scoped>
.user-center-page {
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 用户信息头部 */
.user-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 40px 0;
  margin-bottom: 20px;
}

.user-header-content {
  display: flex;
  align-items: center;
  color: #fff;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 50px;
  margin-right: 25px;
  border: 4px solid rgba(255,255,255,0.3);
}

.user-info {
  flex: 1;
}

.user-name {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
}

.user-level {
  display: inline-block;
  background-color: rgba(255,255,255,0.2);
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 14px;
  margin-bottom: 10px;
}

.user-stats {
  display: flex;
  gap: 30px;
  font-size: 14px;
}

.stat-item span {
  font-weight: bold;
  font-size: 18px;
  margin-right: 5px;
}

/* 主体布局 */
.main-layout {
  display: flex;
  gap: 20px;
}

/* 左侧菜单 */
.sidebar {
  width: 250px;
  flex-shrink: 0;
}

.menu-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px 0;
}

.menu-item {
  padding: 15px 25px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  font-size: 15px;
  color: #666;
}

.menu-item:hover {
  background-color: #f8f8f8;
  color: #ff6700;
}

.menu-item.active {
  background-color: #fff8f0;
  color: #ff6700;
  font-weight: bold;
  border-right: 3px solid #ff6700;
}

.menu-icon {
  margin-right: 12px;
  font-size: 18px;
}

/* 右侧内容 */
.main-content {
  flex: 1;
}

.content-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #ff6700;
}

.order-tabs {
  display: flex;
  gap: 30px;
  margin-bottom: 25px;
  border-bottom: 1px solid #e5e5e5;
}

.order-tab {
  padding: 15px 0;
  cursor: pointer;
  font-size: 15px;
  color: #666;
  position: relative;
}

.order-tab:hover {
  color: #ff6700;
}

.order-tab.active {
  color: #ff6700;
  font-weight: bold;
}

.simple-order-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.simple-order-item {
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 4px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.address-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.address-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  padding: 15px;
  position: relative;
}

.address-tag {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff6700;
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

.address-name {
  font-weight: bold;
  margin-bottom: 5px;
}

.address-phone {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.address-detail {
  font-size: 14px;
  color: #999;
  line-height: 1.5;
  margin-bottom: 10px;
}

.address-actions {
  display: flex;
  gap: 10px;
}
</style>
