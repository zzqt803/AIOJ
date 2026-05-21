<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/" class="logo">
        <span class="logo-bracket">{</span>OJ<span class="logo-bracket">}</span>
      </router-link>
      <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">题库</router-link>
      <router-link to="/problem-sets" class="nav-link" :class="{ active: route.path.startsWith('/problem-sets') }">题单</router-link>
      <router-link to="/leaderboard" class="nav-link" :class="{ active: route.path === '/leaderboard' }">排行榜</router-link>
      <router-link to="/admin/problems" class="nav-link" :class="{ active: route.path.startsWith('/admin') }">管理</router-link>
    </div>
    <div class="nav-right">
      <span class="username">{{ auth.user?.username || '用户' }}</span>
      <button class="btn-logout" @click="handleLogout">退出</button>
    </div>
  </nav>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  height: 50px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 24px;
}

.logo {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.logo-bracket {
  color: var(--accent);
}

.nav-link {
  font-size: 14px;
  color: var(--text-secondary);
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: var(--text-primary);
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.username {
  font-size: 13px;
  color: var(--text-secondary);
}

.btn-logout {
  background: none;
  border: 1px solid var(--border);
  color: var(--text-secondary);
  font-size: 13px;
  padding: 5px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  border-color: var(--text-secondary);
  color: var(--text-primary);
}
</style>