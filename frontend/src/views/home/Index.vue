<template>
  <div class="home-page">
    <div class="container">
      <!-- 轮播图 -->
      <div class="banner-section">
        <el-carousel height="400px" :interval="5000" arrow="hover">
          <el-carousel-item v-for="i in 3" :key="i">
            <div class="banner">
              <div class="banner-content">
                <h2>春季大促 {{ i }}</h2>
                <p>全场低至5折起</p>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>
      </div>

      <!-- 商品分类 -->
      <div class="category-section">
        <h2 class="section-title">商品分类</h2>
        <div class="category-grid">
          <div
            v-for="category in categories"
            :key="category.id"
            class="category-item"
            @click="goToCategory(category.id)"
          >
            <div class="category-icon">{{ category.icon }}</div>
            <div class="category-name">{{ category.name }}</div>
          </div>
        </div>
      </div>

      <!-- 热门商品 -->
      <div class="product-section">
        <h2 class="section-title">热门商品</h2>
        <div v-loading="loading" class="product-grid">
          <div
            v-for="product in hotProducts"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <div class="product-image">{{ product.image || '📱' }}</div>
            <div class="product-info">
              <div class="product-name">{{ product.name }}</div>
              <div class="product-desc">{{ product.description }}</div>
              <div class="product-price">¥{{ product.price }}</div>
              <div class="product-sales">月销 {{ product.sales }}+</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 新品推荐 -->
      <div class="product-section">
        <h2 class="section-title">新品推荐</h2>
        <div v-loading="loading" class="product-grid">
          <div
            v-for="product in newProducts"
            :key="product.id"
            class="product-card"
            @click="goToProduct(product.id)"
          >
            <div class="product-image">{{ product.image || '📱' }}</div>
            <div class="product-info">
              <div class="product-name">{{ product.name }}</div>
              <div class="product-desc">{{ product.description }}</div>
              <div class="product-price">¥{{ product.price }}</div>
              <div class="product-sales">月销 {{ product.sales }}+</div>
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
import { productApi } from '../../api'
import type { Category, Product } from '../../types'

const router = useRouter()
const categories = ref<Category[]>([])
const hotProducts = ref<Product[]>([])
const newProducts = ref<Product[]>([])
const loading = ref(false)

const loadData = async () => {
  try {
    loading.value = true
    const [categoriesData, hotData, newData] = await Promise.all([
      productApi.getCategories(),
      productApi.getHotProducts(8),
      productApi.getNewProducts(8)
    ])
    categories.value = categoriesData
    hotProducts.value = hotData
    newProducts.value = newData
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

const goToCategory = (categoryId: number) => {
  router.push({
    name: 'ProductList',
    query: { category_id: categoryId }
  })
}

const goToProduct = (productId: number) => {
  router.push({
    name: 'ProductDetail',
    params: { id: productId }
  })
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.home-page {
  padding-bottom: 40px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 轮播图 */
.banner-section {
  margin-top: 20px;
}

.banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  height: 400px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  text-align: center;
}

.banner-content h2 {
  font-size: 48px;
  margin-bottom: 20px;
}

.banner-content p {
  font-size: 20px;
  opacity: 0.9;
}

/* 分类区域 */
.category-section {
  margin: 40px 0;
}

.section-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 24px;
  background-color: #ff6700;
  margin-right: 10px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 20px;
}

.category-item {
  background-color: #fff;
  padding: 25px 15px;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.category-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.category-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.category-name {
  font-size: 14px;
  color: #333;
}

/* 商品区域 */
.product-section {
  margin: 40px 0;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.product-card {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
}

.product-image {
  width: 100%;
  height: 250px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 10px;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-desc {
  font-size: 13px;
  color: #999;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  font-size: 20px;
  color: #ff6700;
  font-weight: bold;
}

.product-sales {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}
</style>
