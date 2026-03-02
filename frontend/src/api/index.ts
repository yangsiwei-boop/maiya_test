import request from './request'
import type { User, Category, Product, CartItem, Address, Order } from '../types'

// 认证相关API
export const authApi = {
  // 登录
  login: (data: { phone: string; password: string }) =>
    request.post<any, { access_token: string; user: User }>('/api/auth/login', data),

  // 注册
  register: (data: { phone: string; password: string; username?: string }) =>
    request.post<any, { access_token: string; user: User }>('/api/auth/register', data),

  // 获取当前用户信息
  getCurrentUser: () =>
    request.get<any, User>('/api/auth/me'),

  // 发送验证码
  sendCode: (phone: string) =>
    request.post<any, { code: string }>('/api/auth/send-code', null, { params: { phone } })
}

// 商品相关API
export const productApi = {
  // 获取分类列表
  getCategories: (parent_id?: number) =>
    request.get<any, Category[]>('/api/products/categories', { params: { parent_id } }),

  // 获取商品列表
  getProducts: (params: {
    category_id?: number
    keyword?: string
    brand?: string
    min_price?: number
    max_price?: number
    sort_by?: string
    page?: number
    page_size?: number
  }) =>
    request.get<any, Product[]>('/api/products/products', { params }),

  // 获取商品详情
  getProductDetail: (id: number) =>
    request.get<any, Product>(`/api/products/products/${id}`),

  // 获取热门商品
  getHotProducts: (limit = 10) =>
    request.get<any, Product[]>('/api/products/hot', { params: { limit } }),

  // 获取新品
  getNewProducts: (limit = 10) =>
    request.get<any, Product[]>('/api/products/new', { params: { limit } }),

  // 收藏/取消收藏商品
  toggleFavorite: (id: number) =>
    request.post<any, { message: string; is_favorite: boolean }>(`/api/products/products/${id}/favorite`)
}

// 购物车相关API
export const cartApi = {
  // 获取购物车列表
  getCart: () =>
    request.get<any, CartItem[]>('/api/cart/'),

  // 添加商品到购物车
  addToCart: (data: { product_id: number; quantity: number; specs?: any }) =>
    request.post<any, CartItem>('/api/cart/', data),

  // 更新购物车商品数量
  updateCartItem: (id: number, quantity: number) =>
    request.put<any, { message: string }>(`/api/cart/${id}`, null, { params: { quantity } }),

  // 删除购物车商品
  removeCartItem: (id: number) =>
    request.delete<any, { message: string }>(`/api/cart/${id}`),

  // 清空购物车
  clearCart: () =>
    request.delete<any, { message: string }>('/api/cart/')
}

// 订单相关API
export const orderApi = {
  // 创建订单
  createOrder: (data: {
    address_id: number
    items: { product_id: number; quantity: number; specs?: any }[]
    payment_method: string
    remark?: string
  }) =>
    request.post<any, Order>('/api/orders/', data),

  // 获取订单列表
  getOrders: (params: { status?: string; page?: number; page_size?: number }) =>
    request.get<any, Order[]>('/api/orders/', { params }),

  // 获取订单详情
  getOrderDetail: (id: number) =>
    request.get<any, Order>(`/api/orders/${id}`),

  // 取消订单
  cancelOrder: (id: number) =>
    request.put<any, { message: string }>(`/api/orders/${id}/cancel`),

  // 支付订单
  payOrder: (id: number) =>
    request.put<any, { message: string }>(`/api/orders/${id}/pay`),

  // 确认收货
  confirmOrder: (id: number) =>
    request.put<any, { message: string }>(`/api/orders/${id}/confirm`)
}

// 用户相关API
export const userApi = {
  // 获取地址列表
  getAddresses: () =>
    request.get<any, Address[]>('/api/users/addresses'),

  // 添加地址
  addAddress: (data: Address) =>
    request.post<any, Address>('/api/users/addresses', data),

  // 更新地址
  updateAddress: (id: number, data: Address) =>
    request.put<any, Address>(`/api/users/addresses/${id}`, data),

  // 删除地址
  deleteAddress: (id: number) =>
    request.delete<any, { message: string }>(`/api/users/addresses/${id}`),

  // 获取用户统计信息
  getUserStats: () =>
    request.get<any, {
      total_orders: number
      pending_orders: number
      shipped_orders: number
      completed_orders: number
      favorite_count: number
      coupon_count: number
      points: number
      level: string
    }>('/api/users/stats')
}
