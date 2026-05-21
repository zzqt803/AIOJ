import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

const userRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresGuest: true },
  },
  {
    path: '/',
    name: 'Problems',
    component: () => import('../views/user/Problems.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/problems/:id',
    name: 'ProblemDetail',
    component: () => import('../views/user/ProblemDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/problem-sets',
    name: 'ProblemSets',
    component: () => import('../views/user/ProblemSets.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/problem-sets/:id',
    name: 'ProblemSetDetail',
    component: () => import('../views/user/ProblemSetDetail.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/leaderboard',
    name: 'Leaderboard',
    component: () => import('../views/user/Leaderboard.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/bookmarks',
    name: 'Bookmarks',
    component: () => import('../views/user/Bookmarks.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/submissions',
    name: 'Submissions',
    component: () => import('../views/user/Submissions.vue'),
    meta: { requiresAuth: true },
  },
]

const adminRoutes = [
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/problems',
    name: 'AdminProblems',
    component: () => import('../views/admin/Problems.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/problem-sets',
    name: 'AdminProblemSets',
    component: () => import('../views/admin/ProblemSets.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('../views/admin/Users.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
  },
]

const routes = [...userRoutes, ...adminRoutes]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresGuest && auth.isLoggedIn) {
    // 已登录用户访问登录页，根据角色跳转
    return auth.isAdmin ? { name: 'AdminDashboard' } : { name: 'Problems' }
  }

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return { name: 'Login' }
  }

  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return { name: 'Problems' }
  }
})

export default router
