<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <div class="content-header">
        <h1>仪表盘</h1>
        <p class="subtitle">欢迎回来，{{ user?.username }}</p>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/><path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalProblems || 0 }}</div>
            <div class="stat-label">题目总数</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalSubmissions || 0 }}</div>
            <div class="stat-label">提交总数</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalUsers || 0 }}</div>
            <div class="stat-label">用户总数</div>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/></svg>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalProblemSets || 0 }}</div>
            <div class="stat-label">题单总数</div>
          </div>
        </div>
      </div>

      <div class="quick-actions">
        <h2>快捷操作</h2>
        <div class="actions-grid">
          <router-link to="/admin/problems" class="action-card">
            <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
            <span>添加题目</span>
          </router-link>
          <router-link to="/admin/problem-sets" class="action-card">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/></svg>
            <span>管理题单</span>
          </router-link>
          <router-link to="/admin/users" class="action-card">
            <svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/></svg>
            <span>用户管理</span>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminSidebar from '../../components/AdminSidebar.vue'
import { useAuthStore } from '../../store/auth'
import request from '../../api/request'

const auth = useAuthStore()
const user = computed(() => auth.user)
const stats = ref({})

onMounted(async () => {
  // 这里可以加载统计数据
})
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

.admin-content {
  flex: 1;
  padding: 24px 32px;
}

.content-header {
  margin-bottom: 32px;
}

.content-header h1 {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: var(--text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 40px;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon svg {
  width: 20px;
  height: 20px;
  color: var(--text-muted);
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
}

.stat-label {
  font-size: 13px;
  color: var(--text-muted);
  margin-top: 2px;
}

.quick-actions h2 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.action-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: all 0.15s ease-out;
}

.action-card:hover {
  border-color: var(--text-muted);
  transform: translateY(-1px);
}

.action-card svg {
  width: 24px;
  height: 24px;
  color: var(--text-muted);
}

.action-card span {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-primary);
}
</style>
