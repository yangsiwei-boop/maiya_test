import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Layout',
    component: () => import('../components/layout/MainLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: '/home',
        name: 'Home',
        component: () => import('../views/home/Index.vue'),
        meta: { title: '首页' }
      },
      {
        path: '/products',
        name: 'ProductList',
        component: () => import('../views/product/List.vue'),
        meta: { title: '商品列表' }
      },
      {
        path: '/products/:id',
        name: 'ProductDetail',
        component: () => import('../views/product/Detail.vue'),
        meta: { title: '商品详情' }
      },
      {
        path: '/cart',
        name: 'Cart',
        component: () => import('../views/cart/Index.vue'),
        meta: { title: '购物车', requiresAuth: true }
      },
      {
        path: '/orders',
        name: 'OrderList',
        component: () => import('../views/order/List.vue'),
        meta: { title: '我的订单', requiresAuth: true }
      },
      {
        path: '/orders/confirm',
        name: 'OrderConfirm',
        component: () => import('../views/order/Confirm.vue'),
        meta: { title: '确认订单', requiresAuth: true }
      },
      {
        path: '/user',
        name: 'UserCenter',
        component: () => import('../views/user/Index.vue'),
        meta: { title: '个人中心', requiresAuth: true }
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { title: '注册' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/home'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 初始化用户状态
  if (!userStore.isLoggedIn && localStorage.getItem('token')) {
    userStore.init()
  }

  // 需要登录的路由
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 购物中心`
  }
})

export default router
