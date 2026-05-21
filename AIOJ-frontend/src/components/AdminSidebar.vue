<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <router-link to="/admin" class="logo">
        <span class="logo-mark">A</span>
        <span class="logo-text">AIOJ</span>
      </router-link>
      <span class="badge">Admin</span>
    </div>

    <nav class="sidebar-nav">
      <router-link to="/admin" class="nav-item" :class="{ active: route.path === '/admin' }">
        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
          <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
        </svg>
        <span>仪表盘</span>
      </router-link>

      <div class="nav-section">内容管理</div>

      <router-link to="/admin/problems" class="nav-item" :class="{ active: route.path.startsWith('/admin/problems') }">
        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
          <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
        </svg>
        <span>题目管理</span>
      </router-link>

      <router-link to="/admin/problem-sets" class="nav-item" :class="{ active: route.path.startsWith('/admin/problem-sets') }">
        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
          <path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/>
        </svg>
        <span>题单管理</span>
      </router-link>

      <div class="nav-section">用户管理</div>

      <router-link to="/admin/users" class="nav-item" :class="{ active: route.path.startsWith('/admin/users') }">
        <svg class="nav-icon" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/>
        </svg>
        <span>用户管理</span>
      </router-link>
    </nav>

    <div class="sidebar-footer">
      <div class="user-info">
        <div class="avatar">{{ user?.username?.charAt(0)?.toUpperCase() || 'A' }}</div>
        <div class="user-meta">
          <span class="user-name">{{ user?.username || '管理员' }}</span>
          <span class="user-role">管理员</span>
        </div>
      </div>
      <button class="btn-logout" @click="handleLogout" title="退出登录">
        <svg viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"/>
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const user = computed(() => auth.user)

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  width: 240px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
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
}

.logo-text {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
}

.badge {
  font-size: 10px;
  padding: 2px 8px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  border-radius: 4px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.sidebar-nav {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
}

.nav-section {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 16px 12px 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 6px;
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s ease-out;
}

.nav-item:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.nav-item.active {
  background: rgba(var(--accent-rgb), 0.1);
  color: var(--accent);
}

.nav-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
}

.user-meta {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}

.user-role {
  font-size: 11px;
  color: var(--text-muted);
}

.btn-logout {
  width: 32px;
  height: 32px;
  background: none;
  border: none;
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.btn-logout:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-logout svg {
  width: 16px;
  height: 16px;
}
</style>
