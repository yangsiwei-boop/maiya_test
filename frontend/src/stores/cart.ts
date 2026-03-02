import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { CartItem } from '../types'
import { cartApi } from '../api'

export const useCartStore = defineStore('cart', () => {
  const cartItems = ref<CartItem[]>([])
  const loading = ref<boolean>(false)

  // 购物车总数量
  const totalQuantity = computed(() => {
    return cartItems.value.reduce((total, item) => total + item.quantity, 0)
  })

  // 购物车总金额
  const totalAmount = computed(() => {
    return cartItems.value.reduce(
      (total, item) => total + item.product.price * item.quantity,
      0
    )
  })

  // 获取购物车列表
  const fetchCart = async () => {
    try {
      loading.value = true
      cartItems.value = await cartApi.getCart()
    } catch (error) {
      console.error('获取购物车失败:', error)
    } finally {
      loading.value = false
    }
  }

  // 添加商品到购物车
  const addToCart = async (productId: number, quantity: number = 1, specs?: any) => {
    try {
      const newItem = await cartApi.addToCart({ product_id: productId, quantity, specs })
      const existingIndex = cartItems.value.findIndex(item => item.id === newItem.id)

      if (existingIndex !== -1) {
        cartItems.value[existingIndex] = newItem
      } else {
        cartItems.value.push(newItem)
      }

      return newItem
    } catch (error) {
      console.error('添加到购物车失败:', error)
      throw error
    }
  }

  // 更新商品数量
  const updateQuantity = async (itemId: number, quantity: number) => {
    try {
      await cartApi.updateCartItem(itemId, quantity)

      const item = cartItems.value.find(item => item.id === itemId)
      if (item) {
        item.quantity = quantity
      }
    } catch (error) {
      console.error('更新数量失败:', error)
      throw error
    }
  }

  // 删除商品
  const removeItem = async (itemId: number) => {
    try {
      await cartApi.removeCartItem(itemId)
      cartItems.value = cartItems.value.filter(item => item.id !== itemId)
    } catch (error) {
      console.error('删除商品失败:', error)
      throw error
    }
  }

  // 清空购物车
  const clearCart = async () => {
    try {
      await cartApi.clearCart()
      cartItems.value = []
    } catch (error) {
      console.error('清空购物车失败:', error)
      throw error
    }
  }

  return {
    cartItems,
    loading,
    totalQuantity,
    totalAmount,
    fetchCart,
    addToCart,
    updateQuantity,
    removeItem,
    clearCart
  }
})
