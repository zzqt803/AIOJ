<template>
  <nav class="navbar">
    <div class="nav-left">
      <router-link to="/" class="logo">
        <span class="logo-mark">A</span>
        <span class="logo-text">AIOJ</span>
      </router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link" :class="{ active: route.path === '/' }">
          题库
        </router-link>
        <router-link to="/problem-sets" class="nav-link" :class="{ active: route.path.startsWith('/problem-sets') }">
          题单
        </router-link>
        <router-link to="/leaderboard" class="nav-link" :class="{ active: route.path === '/leaderboard' }">
          排行榜
        </router-link>
        <router-link to="/submissions" class="nav-link" :class="{ active: route.path === '/submissions' }">
          提交记录
        </router-link>
        <router-link to="/bookmarks" class="nav-link" :class="{ active: route.path === '/bookmarks' }">
          收藏
        </router-link>
      </div>
    </div>
    <div class="nav-right">
      <div class="user-menu" @click="showMenu = !showMenu">
        <div class="avatar">{{ user?.username?.charAt(0)?.toUpperCase() || 'U' }}</div>
        <span class="username">{{ user?.username || '用户' }}</span>
        <svg class="arrow" viewBox="0 0 16 16" fill="currentColor">
          <path d="M4.646 5.646a.5.5 0 0 1 .708 0L8 8.293l2.646-2.647a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 0 1 0-.708z"/>
        </svg>
      </div>
      <div class="dropdown" v-if="showMenu">
        <div class="dropdown-item" @click="router.push('/submissions')">
          <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>
          我的提交
        </div>
        <div class="dropdown-item" @click="router.push('/bookmarks')">
          <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/></svg>
          我的收藏
        </div>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item danger" @click="handleLogout">
          <svg viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M10 12.5a.5.5 0 0 1-.5.5h-8a.5.5 0 0 1-.5-.5v-9a.5.5 0 0 1 .5-.5h8a.5.5 0 0 1 .5.5v2a.5.5 0 0 0 1 0v-2A1.5 1.5 0 0 0 9.5 2h-8A1.5 1.5 0 0 0 0 3.5v9A1.5 1.5 0 0 0 1.5 14h8a1.5 1.5 0 0 0 1.5-1.5v-2a.5.5 0 0 0-1 0v2z"/><path fill-rule="evenodd" d="M15.854 8.354a.5.5 0 0 0 0-.708l-3-3a.5.5 0 0 0-.708.708L14.293 7.5H5.5a.5.5 0 0 0 0 1h8.793l-2.147 2.146a.5.5 0 0 0 .708.708l3-3z"/></svg>
          退出登录
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const showMenu = ref(false)

const user = computed(() => auth.user)

function handleLogout() {
  auth.logout()
  router.push('/login')
}

// 点击外部关闭菜单
document.addEventListener('click', (e) => {
  if (!e.target.closest('.user-menu') && !e.target.closest('.dropdown')) {
    showMenu.value = false
  }
})
</script>

<style scoped>
.navbar {
  height: 56px;
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
  gap: 32px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}

.logo-mark {
  width: 28px;
  height: 28px;
  background: var(--accent);
  color: #fff;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: -0.5px;
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-link {
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  border-radius: 6px;
  transition: all 0.15s ease-out;
}

.nav-link:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.nav-link.active {
  color: var(--accent);
  background: rgba(var(--accent-rgb), 0.08);
}

.nav-right {
  position: relative;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.user-menu:hover {
  background: var(--bg-hover);
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}

.arrow {
  width: 14px;
  height: 14px;
  color: var(--text-muted);
  transition: transform 0.15s;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  min-width: 180px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  overflow: hidden;
  padding: 4px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: var(--bg-hover);
}

.dropdown-item svg {
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

.dropdown-item.danger {
  color: #ef4444;
}

.dropdown-item.danger svg {
  color: #ef4444;
}

.dropdown-divider {
  height: 1px;
  background: var(--border);
  margin: 4px 0;
}
</style>
