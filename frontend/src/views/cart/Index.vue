<template>
  <div class="cart-page">
    <div class="container">
      <!-- 面包屑 -->
      <el-breadcrumb class="breadcrumb" separator=">">
        <el-breadcrumb-item to="/home">首页</el-breadcrumb-item>
        <el-breadcrumb-item>购物车</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 页面标题 -->
      <h1 class="page-title">我的购物车</h1>

      <!-- 购物车内容 -->
      <div v-loading="cartStore.loading" class="cart-content">
        <div v-if="cartStore.cartItems.length > 0">
          <!-- 表头 -->
          <div class="cart-header">
            <div></div>
            <div>商品信息</div>
            <div></div>
            <div>单价</div>
            <div>数量</div>
            <div>小计</div>
            <div>操作</div>
          </div>

          <!-- 商品列表 -->
          <div
            v-for="item in cartStore.cartItems"
            :key="item.id"
            class="cart-item"
          >
            <el-checkbox v-model="item.checked" />
            <div class="product-img" @click="goToProduct(item.product.id)">
              {{ item.product.image || '📱' }}
            </div>
            <div class="product-info" @click="goToProduct(item.product.id)">
              <div class="product-name">{{ item.product.name }}</div>
              <div class="product-spec">{{ item.specs || '默认规格' }}</div>
            </div>
            <div class="product-price">¥{{ item.product.price }}</div>
            <div class="quantity-control">
              <el-input-number
                :model-value="item.quantity"
                :min="1"
                :max="item.product.stock"
                @change="(val) => handleQuantityChange(item, val)"
              />
            </div>
            <div class="subtotal">¥{{ (item.product.price * item.quantity).toFixed(2) }}</div>
            <div class="action-buttons">
              <el-button link type="danger" @click="handleRemove(item.id)">
                删除
              </el-button>
            </div>
          </div>

          <!-- 底部结算栏 -->
          <div class="cart-footer">
            <div class="footer-content">
              <div class="footer-left">
                <el-checkbox v-model="selectAll" @change="handleSelectAll">
                  全选
                </el-checkbox>
                <el-button link type="danger" @click="handleRemoveSelected">
                  删除选中
                </el-button>
              </div>
              <div class="footer-right">
                <div class="selected-info">
                  已选商品 <span>{{ selectedCount }}</span> 件
                </div>
                <div class="total-price">
                  合计: <span class="price">¥{{ selectedTotal.toFixed(2) }}</span>
                </div>
                <el-button
                  type="primary"
                  size="large"
                  :disabled="selectedCount === 0"
                  @click="goToCheckout"
                >
                  去结算
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <!-- 空购物车 -->
        <div v-else class="empty-cart">
          <div class="empty-icon">🛒</div>
          <div class="empty-text">购物车空空如也</div>
          <el-button type="primary" @click="$router.push('/home')">
            继续购物
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../../stores/cart'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { CartItem } from '../../types'

const router = useRouter()
const cartStore = useCartStore()

const selectAll = ref(false)

const selectedCount = computed(() => {
  return cartStore.cartItems.filter(item => (item as any).checked).length
})

const selectedTotal = computed(() => {
  return cartStore.cartItems
    .filter(item => (item as any).checked)
    .reduce((total, item) => total + item.product.price * item.quantity, 0)
})

const handleQuantityChange = async (item: CartItem, quantity: number) => {
  if (quantity < 1) return

  try {
    await cartStore.updateQuantity(item.id, quantity)
  } catch (error) {
    ElMessage.error('更新数量失败')
  }
}

const handleRemove = async (itemId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await cartStore.removeItem(itemId)
    ElMessage.success('删除成功')
  } catch (error) {
    // 用户取消删除
  }
}

const handleRemoveSelected = async () => {
  const selectedItems = cartStore.cartItems.filter(item => (item as any).checked)
  if (selectedItems.length === 0) {
    ElMessage.warning('请先选择要删除的商品')
    return
  }

  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${selectedItems.length} 个商品吗?`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    for (const item of selectedItems) {
      await cartStore.removeItem(item.id)
    }

    ElMessage.success('删除成功')
  } catch (error) {
    // 用户取消删除
  }
}

const handleSelectAll = (checked: boolean) => {
  cartStore.cartItems.forEach(item => {
    (item as any).checked = checked
  })
}

const goToProduct = (productId: number) => {
  router.push({
    name: 'ProductDetail',
    params: { id: productId }
  })
}

const goToCheckout = () => {
  router.push('/orders/confirm')
}

onMounted(() => {
  cartStore.fetchCart()
})
</script>

<style scoped>
.cart-page {
  padding-bottom: 40px;
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

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  padding: 20px 0;
  border-bottom: 2px solid #ff6700;
}

/* 购物车主区域 */
.cart-content {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

/* 表头 */
.cart-header {
  display: grid;
  grid-template-columns: 50px 80px 400px 150px 120px 150px 100px;
  gap: 15px;
  padding: 15px 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  font-weight: bold;
  font-size: 14px;
  color: #666;
}

/* 购物车商品项 */
.cart-item {
  display: grid;
  grid-template-columns: 50px 80px 400px 150px 120px 150px 100px;
  gap: 15px;
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
  align-items: center;
}

.cart-item:last-child {
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
  cursor: pointer;
}

.product-info {
  cursor: pointer;
}

.product-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.product-spec {
  font-size: 13px;
  color: #999;
}

.product-price {
  font-size: 16px;
  color: #ff6700;
  font-weight: bold;
}

.subtotal {
  font-size: 18px;
  color: #ff6700;
  font-weight: bold;
}

/* 底部结算栏 */
.cart-footer {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}

.footer-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.footer-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.footer-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.selected-info {
  font-size: 14px;
  color: #666;
}

.selected-info span {
  color: #ff6700;
  font-weight: bold;
  font-size: 18px;
}

.total-price {
  font-size: 14px;
  color: #666;
}

.total-price .price {
  color: #ff6700;
  font-size: 28px;
  font-weight: bold;
}

/* 空购物车 */
.empty-cart {
  text-align: center;
  padding: 100px 0;
}

.empty-icon {
  font-size: 120px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  color: #999;
  margin-bottom: 30px;
}
</style>
