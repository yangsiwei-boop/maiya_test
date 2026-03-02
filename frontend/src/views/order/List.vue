<template>
  <div class="order-list-page">
    <div class="container">
      <!-- 快捷入口 -->
      <div class="quick-actions">
        <div class="quick-action-item" @click="filterByStatus('')">
          <div class="action-icon">📋</div>
          <div class="action-name">全部订单</div>
        </div>
        <div class="quick-action-item" @click="filterByStatus('pending')">
          <div class="action-icon">💳</div>
          <div class="action-name">待付款</div>
        </div>
        <div class="quick-action-item" @click="filterByStatus('shipped')">
          <div class="action-icon">🚚</div>
          <div class="action-name">待收货</div>
        </div>
        <div class="quick-action-item" @click="filterByStatus('completed')">
          <div class="action-icon">⭐</div>
          <div class="action-name">待评价</div>
        </div>
        <div class="quick-action-item" @click="$router.push('/cart')">
          <div class="action-icon">🛒</div>
          <div class="action-name">购物车</div>
        </div>
      </div>

      <!-- 订单列表 -->
      <div v-loading="loading" class="order-list">
        <div v-for="order in orders" :key="order.id" class="order-item">
          <div class="order-header">
            <div>
              <span class="order-number">订单号: {{ order.order_number }}</span>
              <span class="order-time">{{ formatDate(order.created_at) }}</span>
            </div>
            <span class="order-status">{{ getStatusText(order.status) }}</span>
          </div>

          <div class="order-products">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="order-product"
            >
              <div class="order-product-img">{{ item.product_image || '📱' }}</div>
              <div class="order-product-info">
                <div class="order-product-name">{{ item.product_name }}</div>
                <div class="order-product-spec">{{ item.product_spec || '默认规格' }}</div>
              </div>
              <div class="order-product-quantity">x{{ item.quantity }}</div>
              <div class="order-product-price">¥{{ item.price }}</div>
            </div>
          </div>

          <div class="order-footer">
            <div class="order-total">
              共{{ order.items.length }}件，合计: <span class="price">¥{{ order.pay_amount }}</span>
            </div>
            <div class="order-actions">
              <el-button v-if="order.status === 'pending'" @click="cancelOrder(order.id)">
                取消订单
              </el-button>
              <el-button v-if="order.status === 'pending'" type="primary" @click="payOrder(order.id)">
                立即付款
              </el-button>
              <el-button v-if="order.status === 'shipped'" type="primary" @click="confirmOrder(order.id)">
                确认收货
              </el-button>
              <el-button v-if="order.status === 'completed'" @click="buyAgain(order)">
                再次购买
              </el-button>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="!loading && orders.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <div class="empty-text">暂无订单</div>
          <el-button type="primary" @click="$router.push('/home')">
            去购物
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { orderApi } from '../../api'
import { useCartStore } from '../../stores/cart'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Order } from '../../types'

const router = useRouter()
const cartStore = useCartStore()

const orders = ref<Order[]>([])
const loading = ref(false)

const loadOrders = async (status = '') => {
  try {
    loading.value = true
    orders.value = await orderApi.getOrders({ status })
  } catch (error) {
    ElMessage.error('加载订单列表失败')
  } finally {
    loading.value = false
  }
}

const filterByStatus = (status: string) => {
  loadOrders(status)
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
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

const cancelOrder = async (orderId: number) => {
  try {
    await ElMessageBox.confirm('确定要取消这个订单吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await orderApi.cancelOrder(orderId)
    ElMessage.success('订单已取消')
    loadOrders()
  } catch (error) {
    // 用户取消
  }
}

const payOrder = async (orderId: number) => {
  try {
    await orderApi.payOrder(orderId)
    ElMessage.success('支付成功')
    loadOrders()
  } catch (error) {
    ElMessage.error('支付失败')
  }
}

const confirmOrder = async (orderId: number) => {
  try {
    await ElMessageBox.confirm('确认已收到商品吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await orderApi.confirmOrder(orderId)
    ElMessage.success('确认收货成功')
    loadOrders()
  } catch (error) {
    // 用户取消
  }
}

const buyAgain = async (order: Order) => {
  try {
    for (const item of order.items) {
      await cartStore.addToCart(item.product_id, item.quantity)
    }
    ElMessage.success('已加入购物车')
    router.push('/cart')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.order-list-page {
  padding: 20px 0 60px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 快捷入口 */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.quick-action-item {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}

.quick-action-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.action-icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.action-name {
  font-size: 14px;
  color: #666;
}

/* 订单列表 */
.order-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.order-item {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.order-header {
  background-color: #f8f8f8;
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #666;
}

.order-number {
  font-weight: bold;
}

.order-time {
  margin: 0 20px;
}

.order-status {
  color: #ff6700;
}

.order-products {
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
}

.order-product {
  display: flex;
  margin-bottom: 15px;
}

.order-product:last-child {
  margin-bottom: 0;
}

.order-product-img {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-right: 15px;
}

.order-product-info {
  flex: 1;
}

.order-product-name {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 5px;
}

.order-product-spec {
  font-size: 13px;
  color: #999;
}

.order-product-quantity {
  color: #999;
  font-size: 14px;
}

.order-product-price {
  font-size: 16px;
  color: #ff6700;
  font-weight: bold;
  text-align: right;
  min-width: 100px;
}

.order-footer {
  padding: 15px 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 20px;
}

.order-total {
  font-size: 14px;
  color: #666;
}

.order-total .price {
  font-size: 20px;
  color: #ff6700;
  font-weight: bold;
}

.order-actions {
  display: flex;
  gap: 10px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 0;
  background-color: #fff;
  border-radius: 8px;
}

.empty-icon {
  font-size: 100px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
  color: #999;
  margin-bottom: 30px;
}
</style>
