<template>
  <div class="product-list-page">
    <div class="container">
      <!-- 面包屑 -->
      <el-breadcrumb class="breadcrumb" separator=">">
        <el-breadcrumb-item to="/home">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="categoryId">商品分类</el-breadcrumb-item>
        <el-breadcrumb-item v-if="keyword">搜索结果</el-breadcrumb-item>
        <el-breadcrumb-item>全部商品</el-breadcrumb-item>
      </el-breadcrumb>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <div class="filter-group">
          <span class="filter-label">分类:</span>
          <div class="filter-options">
            <div
              v-for="cat in categories"
              :key="cat.id"
              class="filter-option"
              :class="{ active: categoryId === cat.id }"
              @click="selectCategory(cat.id)"
            >
              {{ cat.name }}
            </div>
          </div>
        </div>
      </div>

      <!-- 排序栏 -->
      <div class="sort-bar">
        <div class="sort-options">
          <div
            class="sort-option"
            :class="{ active: sortBy === 'default' }"
            @click="changeSort('default')"
          >
            综合排序
          </div>
          <div
            class="sort-option"
            :class="{ active: sortBy === 'sales' }"
            @click="changeSort('sales')"
          >
            销量优先
          </div>
          <div
            class="sort-option"
            :class="{ active: sortBy === 'price_asc' }"
            @click="changeSort('price_asc')"
          >
            价格从低到高
          </div>
          <div
            class="sort-option"
            :class="{ active: sortBy === 'price_desc' }"
            @click="changeSort('price_desc')"
          >
            价格从高到低
          </div>
        </div>
        <div class="result-count">共找到 {{ total }} 件商品</div>
      </div>

      <!-- 商品列表 -->
      <div v-loading="loading" class="product-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-card"
          @click="goToDetail(product.id)"
        >
          <div class="product-image">
            {{ product.image || '📱' }}
            <span v-if="product.is_hot" class="product-badge">热销</span>
            <span v-else-if="product.is_new" class="product-badge">新品</span>
          </div>
          <div class="product-info">
            <div class="product-name">{{ product.name }}</div>
            <div class="product-desc">{{ product.description }}</div>
            <div class="product-price-row">
              <div class="product-price">¥{{ product.price }}</div>
              <div v-if="product.original_price" class="product-old-price">
                ¥{{ product.original_price }}
              </div>
            </div>
            <div class="product-sales">月销 {{ product.sales }}+</div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="total > 0" class="pagination">
        <el-pagination
          v-model:current-page="page"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[20, 40, 60, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { productApi } from '../../api'
import type { Product, Category } from '../../types'

const router = useRouter()
const route = useRoute()

const categories = ref<Category[]>([])
const products = ref<Product[]>([])
const loading = ref(false)
const total = ref(0)

const categoryId = ref<number>()
const keyword = ref<string>()
const sortBy = ref('default')
const page = ref(1)
const pageSize = ref(20)

const loadCategories = async () => {
  try {
    categories.value = await productApi.getCategories()
  } catch (error) {
    console.error('加载分类失败:', error)
  }
}

const loadProducts = async () => {
  try {
    loading.value = true
    const data = await productApi.getProducts({
      category_id: categoryId.value,
      keyword: keyword.value,
      sort_by: sortBy.value,
      page: page.value,
      page_size: pageSize.value
    })
    products.value = data
    // 假设返回的是全部数据,实际应该有分页信息
    total.value = data.length
  } catch (error) {
    console.error('加载商品失败:', error)
  } finally {
    loading.value = false
  }
}

const selectCategory = (id: number) => {
  categoryId.value = id
  page.value = 1
  loadProducts()
}

const changeSort = (sort: string) => {
  sortBy.value = sort
  page.value = 1
  loadProducts()
}

const handlePageChange = (p: number) => {
  page.value = p
  loadProducts()
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  page.value = 1
  loadProducts()
}

const goToDetail = (id: number) => {
  router.push({
    name: 'ProductDetail',
    params: { id }
  })
}

onMounted(() => {
  loadCategories()

  // 从路由参数获取筛选条件
  if (route.query.category_id) {
    categoryId.value = Number(route.query.category_id)
  }
  if (route.query.keyword) {
    keyword.value = route.query.keyword as string
  }

  loadProducts()
})
</script>

<style scoped>
.product-list-page {
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

/* 筛选区域 */
.filter-section {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-label {
  font-weight: bold;
  margin-bottom: 10px;
  display: block;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-option {
  padding: 6px 15px;
  border: 1px solid #e5e5e5;
  border-radius: 15px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.filter-option:hover {
  border-color: #ff6700;
  color: #ff6700;
}

.filter-option.active {
  background-color: #ff6700;
  color: #fff;
  border-color: #ff6700;
}

/* 排序栏 */
.sort-bar {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px 20px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sort-options {
  display: flex;
  gap: 20px;
}

.sort-option {
  cursor: pointer;
  font-size: 14px;
  color: #666;
  transition: color 0.3s;
}

.sort-option:hover {
  color: #ff6700;
}

.sort-option.active {
  color: #ff6700;
  font-weight: bold;
}

.result-count {
  color: #999;
  font-size: 14px;
}

/* 商品列表 */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
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
  height: 220px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
  position: relative;
}

.product-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #ff6700;
  color: #fff;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 12px;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
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

.product-price-row {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.product-price {
  font-size: 20px;
  color: #ff6700;
  font-weight: bold;
}

.product-old-price {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
  margin-left: 8px;
}

.product-sales {
  font-size: 12px;
  color: #999;
  margin-top: 8px;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: center;
  padding: 40px 0;
}
</style>
