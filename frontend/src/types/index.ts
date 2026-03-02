// 通用类型定义

export interface User {
  id: number
  phone: string
  username?: string
  avatar?: string
  level: string
  points: number
  created_at: string
}

export interface Category {
  id: number
  name: string
  icon?: string
  parent_id?: number
}

export interface Product {
  id: number
  name: string
  description?: string
  price: number
  original_price?: number
  stock: number
  sales: number
  image?: string
  images?: string[]
  category_id?: number
  brand?: string
  is_hot: boolean
  is_new: boolean
  specs?: any
  detail?: string
  created_at: string
}

export interface CartItem {
  id: number
  product_id: number
  quantity: number
  specs?: any
  product: Product
}

export interface Address {
  id: number
  receiver_name: string
  receiver_phone: string
  province: string
  city: string
  district: string
  detail: string
  tag?: string
  is_default: boolean
}

export interface Order {
  id: number
  order_number: string
  total_amount: number
  discount_amount: number
  freight_amount: number
  pay_amount: number
  status: string
  payment_method: string
  items: OrderItem[]
  created_at: string
}

export interface OrderItem {
  id: number
  product_id: number
  product_name: string
  product_image?: string
  product_spec?: string
  price: number
  quantity: number
  subtotal: number
}

export interface ApiResponse<T = any> {
  code?: number
  message?: string
  data?: T
}
