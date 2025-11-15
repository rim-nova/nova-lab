import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/datasets',
    name: 'Datasets',
    component: () => import('@/views/datasets/DatasetListView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/datasets/:id',
    name: 'DatasetDetail',
    component: () => import('@/views/datasets/DatasetDetailView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analyze',
    name: 'Analyze',
    component: () => import('@/views/analysis/AnalyzeView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ml',
    name: 'MachineLearning',
    component: () => import('@/views/ml/MLView.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/chat',
    name: 'Chat',
    component: () => import('@/views/ChatView.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (!to.meta.requiresAuth && authStore.isAuthenticated && to.path !== '/dashboard') {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
