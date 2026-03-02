<template>
  <div class="order-confirm-page">
    <div class="container">
      <!-- 面包屑 -->
      <el-breadcrumb class="breadcrumb" separator=">">
        <el-breadcrumb-item to="/home">首页</el-breadcrumb-item>
        <el-breadcrumb-item to="/cart">购物车</el-breadcrumb-item>
        <el-breadcrumb-item>确认订单</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 收货地址 -->
      <div class="section-card">
        <h2 class="section-title">收货地址</h2>
        <el-button type="primary" @click="showAddressDialog = true">
          添加新地址
        </el-button>
        <div class="address-list">
          <div
            v-for="addr in addresses"
            :key="addr.id"
            class="address-item"
            :class="{ active: selectedAddress?.id === addr.id }"
            @click="selectAddress(addr)"
          >
            <span v-if="addr.tag" class="address-tag" :class="addr.tag">
              {{ addr.tag }}
            </span>
            <div class="address-name">{{ addr.receiver_name }}</div>
            <div class="address-phone">{{ addr.receiver_phone }}</div>
            <div class="address-detail">
              {{ addr.province }} {{ addr.city }} {{ addr.district }} {{ addr.detail }}
            </div>
          </div>
        </div>
      </div>

      <!-- 商品清单 -->
      <div class="section-card">
        <h2 class="section-title">商品清单</h2>
        <div class="product-list">
          <div
            v-for="item in cartItems"
            :key="item.id"
            class="product-item"
          >
            <div class="product-img">{{ item.product.image || '📱' }}</div>
            <div class="product-info">
              <div class="product-name">{{ item.product.name }}</div>
              <div class="product-spec">{{ item.specs || '默认规格' }}</div>
              <div class="product-price">¥{{ item.product.price }}</div>
            </div>
            <div class="product-quantity">x{{ item.quantity }}</div>
            <div class="product-subtotal">
              ¥{{ (item.product.price * item.quantity).toFixed(2) }}
            </div>
          </div>
        </div>
      </div>

      <!-- 价格明细 -->
      <div class="section-card">
        <h2 class="section-title">价格明细</h2>
        <div class="price-detail">
          <div class="price-row">
            <span class="price-label">商品总价</span>
            <span class="price-value">¥{{ totalAmount.toFixed(2) }}</span>
          </div>
          <div class="price-row">
            <span class="price-label">运费</span>
            <span class="price-value">¥{{ freight.toFixed(2) }}</span>
          </div>
          <div class="price-row total">
            <span class="price-label">应付总额</span>
            <span class="price-value">¥{{ (totalAmount + freight).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- 底部提交栏 -->
      <div class="submit-bar">
        <div class="submit-info">
          <div class="submit-price">
            应付总额: <span class="price">¥{{ (totalAmount + freight).toFixed(2) }}</span>
          </div>
          <div class="submit-tip">共{{ cartItems.length }}件商品</div>
        </div>
        <el-button type="primary" size="large" :loading="loading" @click="handleSubmit">
          提交订单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { userApi, orderApi } from '../../api'
import { useCartStore } from '../../stores/cart'
import { useUserStore } from '../../stores/user'
import { ElMessage } from 'element-plus'
import type { Address, CartItem } from '../../types'

const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const addresses = ref<Address[]>([])
const selectedAddress = ref<Address>()
const cartItems = ref<CartItem[]>([])
const loading = ref(false)
const showAddressDialog = ref(false)

const totalAmount = computed(() => {
  return cartItems.value.reduce(
    (sum, item) => sum + item.product.price * item.quantity,
    0
  )
})

const freight = computed(() => {
  return totalAmount.value >= 99 ? 0 : 10
})

const loadData = async () => {
  try {
    addresses.value = await userApi.getAddresses()
    if (addresses.value.length > 0) {
      const defaultAddr = addresses.value.find(a => a.is_default)
      selectedAddress.value = defaultAddr || addresses.value[0]
    }

    // 获取购物车已选中的商品
    cartItems.value = cartStore.cartItems.filter(item => (item as any).checked)
    if (cartItems.value.length === 0) {
      ElMessage.warning('请先选择要结算的商品')
      router.push('/cart')
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const selectAddress = (addr: Address) => {
  selectedAddress.value = addr
}

const handleSubmit = async () => {
  if (!selectedAddress.value) {
    ElMessage.warning('请选择收货地址')
    return
  }

  try {
    loading.value = true
    const order = await orderApi.createOrder({
      address_id: selectedAddress.value.id,
      items: cartItems.value.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity,
        specs: item.specs
      })),
      payment_method: '在线支付'
    })

    ElMessage.success('订单创建成功')

    // 清空购物车
    await cartStore.clearCart()

    // 跳转到支付页面或订单详情
    router.push(`/orders/${order.id}`)
  } catch (error) {
    ElMessage.error('提交订单失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  loadData()
})
</script>

<style scoped>
.order-confirm-page {
  padding: 20px 0 60px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumb {
  padding: 20px 0;
  font-size: 14px;
}

.section-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 25px;
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #ff6700;
}

.address-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-top: 15px;
}

.address-item {
  border: 2px solid #e5e5e5;
  border-radius: 8px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.address-item:hover {
  border-color: #ff6700;
}

.address-item.active {
  border-color: #ff6700;
  background-color: #fff8f0;
}

.address-tag {
  display: inline-block;
  background-color: #ff6700;
  color: #fff;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
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
}

.product-list {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  overflow: hidden;
}

.product-item {
  display: flex;
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
}

.product-item:last-child {
  border-bottom: none;
}

.product-img {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  margin-right: 20px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
}

.product-spec {
  font-size: 13px;
  color: #999;
  margin-bottom: 5px;
}

.product-price {
  font-size: 16px;
  color: #ff6700;
  font-weight: bold;
}

.product-quantity {
  font-size: 14px;
  color: #666;
  margin: 0 20px;
}

.product-subtotal {
  font-size: 18px;
  color: #ff6700;
  font-weight: bold;
  min-width: 100px;
  text-align: right;
}

.price-detail {
  background-color: #fff8f0;
  padding: 20px;
  border-radius: 8px;
}

.price-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 14px;
}

.price-row.total {
  border-top: 1px solid #e5e5e5;
  padding-top: 15px;
  margin-top: 15px;
  font-size: 16px;
}

.price-row.total .price-value {
  font-size: 24px;
  color: #ff6700;
  font-weight: bold;
}

.submit-bar {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-top: 20px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 30px;
}

.submit-info {
  text-align: right;
}

.submit-price {
  font-size: 14px;
  color: #666;
}

.submit-price .price {
  font-size: 28px;
  color: #ff6700;
  font-weight: bold;
}

.submit-tip {
  font-size: 13px;
  color: #999;
  margin-top: 5px;
}
</style>
