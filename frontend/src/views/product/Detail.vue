<template>
  <div v-loading="loading" class="product-detail-page">
    <div v-if="product" class="container">
      <!-- 面包屑 -->
      <el-breadcrumb class="breadcrumb" separator=">">
        <el-breadcrumb-item to="/home">首页</el-breadcrumb-item>
        <el-breadcrumb-item to="/products">商品列表</el-breadcrumb-item>
        <el-breadcrumb-item>{{ product.name }}</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 商品详情 -->
      <div class="product-detail">
        <div class="detail-content">
          <!-- 左侧图片 -->
          <div class="product-images">
            <div class="main-image">
              {{ product.image || '📱' }}
              <span v-if="product.is_hot" class="image-badge">热销</span>
            </div>
          </div>

          <!-- 右侧信息 -->
          <div class="product-info">
            <h1 class="product-title">{{ product.name }}</h1>
            <p class="product-subtitle">{{ product.description }}</p>

            <!-- 价格信息 -->
            <div class="product-price-box">
              <div class="price-row">
                <span class="price-label">价　格</span>
                <span class="current-price">¥{{ product.price }}</span>
                <span v-if="product.original_price" class="original-price">
                  ¥{{ product.original_price }}
                </span>
              </div>
              <div class="sales-info">
                <span>月销 {{ product.sales }}+</span> |
                <span>库存 {{ product.stock }} 件</span>
              </div>
            </div>

            <!-- 数量选择 -->
            <div class="quantity-section">
              <span class="quantity-label">数　量</span>
              <el-input-number v-model="quantity" :min="1" :max="product.stock" />
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <el-button type="primary" size="large" class="btn-primary" @click="addToCart">
                加入购物车
              </el-button>
              <el-button size="large" @click="toggleFavorite">
                {{ isFavorited ? '已收藏' : '收藏' }}
              </el-button>
            </div>

            <!-- 服务保障 -->
            <div class="service-guarantee">
              <div class="service-list">
                <div class="service-item">正品保障</div>
                <div class="service-item">7天无理由退换</div>
                <div class="service-item">运费险</div>
                <div class="service-item">全国联保</div>
                <div class="service-item">顺丰包邮</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 详情标签页 -->
      <div class="detail-tabs">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="商品详情" name="detail">
            <div class="tab-content">
              <div v-html="product.detail || '暂无详情'"></div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="规格参数" name="params">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="商品名称">{{ product.name }}</el-descriptions-item>
              <el-descriptions-item label="品牌">{{ product.brand || '-' }}</el-descriptions-item>
              <el-descriptions-item label="库存">{{ product.stock }}</el-descriptions-item>
              <el-descriptions-item label="销量">{{ product.sales }}</el-descriptions-item>
            </el-descriptions>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { productApi } from '../../api'
import { useCartStore } from '../../stores/cart'
import { ElMessage } from 'element-plus'
import type { Product } from '../../types'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()

const product = ref<Product>()
const loading = ref(false)
const quantity = ref(1)
const activeTab = ref('detail')
const isFavorited = ref(false)

const loadProduct = async () => {
  try {
    loading.value = true
    const id = Number(route.params.id)
    product.value = await productApi.getProductDetail(id)
  } catch (error) {
    ElMessage.error('加载商品详情失败')
    router.push('/products')
  } finally {
    loading.value = false
  }
}

const addToCart = async () => {
  if (!product.value) return

  try {
    await cartStore.addToCart(product.value.id, quantity.value)
    ElMessage.success('已加入购物车')
  } catch (error) {
    ElMessage.error('加入购物车失败')
  }
}

const toggleFavorite = async () => {
  if (!product.value) return

  try {
    const result = await productApi.toggleFavorite(product.value.id)
    isFavorited.value = result.is_favorite
    ElMessage.success(result.message)
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  loadProduct()
})
</script>

<style scoped>
.product-detail-page {
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

/* 商品详情 */
.product-detail {
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
  margin-bottom: 20px;
}

.detail-content {
  display: flex;
  gap: 40px;
}

/* 左侧图片区 */
.product-images {
  width: 450px;
  flex-shrink: 0;
}

.main-image {
  width: 100%;
  height: 450px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 150px;
  position: relative;
}

.image-badge {
  position: absolute;
  top: 15px;
  left: 15px;
  background-color: #ff6700;
  color: #fff;
  padding: 6px 15px;
  border-radius: 4px;
  font-size: 14px;
}

/* 右侧信息区 */
.product-info {
  flex: 1;
}

.product-title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.product-subtitle {
  font-size: 14px;
  color: #999;
  margin-bottom: 20px;
}

.product-price-box {
  background-color: #fff8f0;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.price-row {
  display: flex;
  align-items: baseline;
  margin-bottom: 10px;
}

.price-label {
  font-size: 14px;
  color: #999;
  margin-right: 10px;
}

.current-price {
  font-size: 36px;
  color: #ff6700;
  font-weight: bold;
}

.original-price {
  font-size: 18px;
  color: #999;
  text-decoration: line-through;
  margin-left: 15px;
}

.sales-info {
  font-size: 14px;
  color: #999;
}

/* 数量选择 */
.quantity-section {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
}

.quantity-label {
  font-size: 14px;
  color: #666;
  margin-right: 20px;
  width: 70px;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 30px;
}

.btn-primary {
  flex: 1;
  height: 50px;
  background: linear-gradient(135deg, #ff6700 0%, #ff4500 100%);
  border: none;
}

/* 服务保障 */
.service-guarantee {
  margin-top: 25px;
  padding-top: 25px;
  border-top: 1px solid #e5e5e5;
}

.service-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.service-item {
  font-size: 14px;
  color: #666;
}

.service-item:before {
  content: '✓';
  color: #52c41a;
  margin-right: 5px;
}

/* 详情标签页 */
.detail-tabs {
  background-color: #fff;
  border-radius: 8px;
  margin-top: 20px;
  overflow: hidden;
}

.tab-content {
  padding: 30px;
  min-height: 400px;
}
</style>
