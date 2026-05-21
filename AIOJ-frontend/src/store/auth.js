import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'
import { userApi } from '../api/user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')

  async function login(email, password) {
    const res = await authApi.login({ email, password })
    token.value = res.access_token
    localStorage.setItem('token', res.access_token)

    // 获取用户信息
    await fetchUser()
  }

  async function register(username, email, password) {
    const res = await authApi.register({ username, email, password })
    user.value = res
    localStorage.setItem('user', JSON.stringify(res))
  }

  async function fetchUser() {
    try {
      const userInfo = await userApi.getMe()
      user.value = userInfo
      localStorage.setItem('user', JSON.stringify(userInfo))
    } catch (e) {
      console.error('Failed to fetch user info:', e)
    }
  }

  function logout() {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { token, user, isLoggedIn, isAdmin, login, register, fetchUser, logout }
})
