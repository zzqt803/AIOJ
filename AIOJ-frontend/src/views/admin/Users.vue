<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <div class="content-header">
        <div class="header-left">
          <h1>用户管理</h1>
          <span class="count-badge">{{ total }} 个用户</span>
        </div>
      </div>

      <!-- 搜索 -->
      <div class="toolbar">
        <div class="search-box">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
          </svg>
          <input v-model="search" type="text" placeholder="搜索用户名或邮箱..." @input="debounceSearch" />
        </div>
        <div class="filter-group">
          <select v-model="filterRole" @change="loadUsers">
            <option value="">全部角色</option>
            <option value="admin">管理员</option>
            <option value="user">普通用户</option>
          </select>
        </div>
      </div>

      <!-- 用户表格 -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 60px">ID</th>
              <th>用户信息</th>
              <th style="width: 80px">角色</th>
              <th style="width: 80px">状态</th>
              <th style="width: 140px">注册时间</th>
              <th style="width: 100px">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td class="id-cell">{{ user.id }}</td>
              <td>
                <div class="user-cell">
                  <div class="user-avatar">{{ user.username?.charAt(0)?.toUpperCase() || 'U' }}</div>
                  <div class="user-info">
                    <span class="user-name">{{ user.username }}</span>
                    <span class="user-email">{{ user.email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <span :class="['role-badge', user.role]">
                  {{ roleLabel(user.role) }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  {{ user.is_active ? '正常' : '禁用' }}
                </span>
              </td>
              <td class="date-cell">{{ formatDate(user.created_at) }}</td>
              <td>
                <div class="actions">
                  <button class="btn-text" @click="viewUserDetail(user)">详情</button>
                  <button class="btn-text" @click="viewUserSubmissions(user)">提交</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="loading" class="table-loading">
          <div class="spinner"></div>
        </div>

        <div v-if="!loading && users.length === 0" class="table-empty">
          <span>暂无用户</span>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>

    <!-- 用户详情模态框 -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="selectedUser" @click.self="selectedUser = null">
        <div class="modal">
          <div class="modal-header">
            <h2>用户详情</h2>
            <button class="btn-close" @click="selectedUser = null">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="detail-section">
              <div class="detail-header">
                <div class="detail-avatar">{{ selectedUser.username?.charAt(0)?.toUpperCase() || 'U' }}</div>
                <div>
                  <h3>{{ selectedUser.username }}</h3>
                  <p>{{ selectedUser.email }}</p>
                </div>
              </div>
            </div>

            <div class="detail-grid">
              <div class="detail-item">
                <span class="detail-label">用户ID</span>
                <span class="detail-value">{{ selectedUser.id }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">角色</span>
                <span :class="['role-badge', selectedUser.role]">{{ roleLabel(selectedUser.role) }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">状态</span>
                <span :class="['status-badge', selectedUser.is_active ? 'active' : 'inactive']">
                  {{ selectedUser.is_active ? '正常' : '禁用' }}
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">注册时间</span>
                <span class="detail-value">{{ formatDate(selectedUser.created_at) }}</span>
              </div>
            </div>

            <div class="detail-section" v-if="userStats">
              <h3>刷题统计</h3>
              <div class="stats-grid">
                <div class="stat-item">
                  <span class="stat-value">{{ userStats.total_submissions }}</span>
                  <span class="stat-label">总提交</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ userStats.accepted_submissions }}</span>
                  <span class="stat-label">通过</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ userStats.solved_problems }}</span>
                  <span class="stat-label">解决题目</span>
                </div>
                <div class="stat-item">
                  <span class="stat-value">{{ userStats.current_streak }}</span>
                  <span class="stat-label">连续天数</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 用户提交记录模态框 -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="showSubmissions" @click.self="showSubmissions = false">
        <div class="modal modal-wide">
          <div class="modal-header">
            <h2>{{ selectedUser?.username }} 的提交记录</h2>
            <button class="btn-close" @click="showSubmissions = false">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>

          <div class="modal-body">
            <div class="submissions-table">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>题目</th>
                    <th>语言</th>
                    <th>状态</th>
                    <th>结果</th>
                    <th>时间</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sub in userSubmissions" :key="sub.id">
                    <td class="id-cell">{{ sub.id }}</td>
                    <td>#{{ sub.problem_id }}</td>
                    <td><span class="lang-badge">{{ sub.language }}</span></td>
                    <td>
                      <span :class="['status-badge', sub.status === 'pending' ? 'pending' : 'completed']">
                        {{ sub.status === 'pending' ? '判题中' : '已完成' }}
                      </span>
                    </td>
                    <td>
                      <span :class="['result-badge', sub.result]" v-if="sub.result">
                        {{ resultLabel(sub.result) }}
                      </span>
                      <span v-else>-</span>
                    </td>
                    <td class="date-cell">{{ formatDate(sub.created_at) }}</td>
                  </tr>
                </tbody>
              </table>

              <div v-if="userSubmissions.length === 0" class="table-empty">
                暂无提交记录
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminSidebar from '../../components/AdminSidebar.vue'
import request from '../../api/request'

const users = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const search = ref('')
const filterRole = ref('')
const selectedUser = ref(null)
const userStats = ref(null)
const showSubmissions = ref(false)
const userSubmissions = ref([])

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

function roleLabel(role) {
  return { admin: '管理员', user: '普通用户', guest: '游客' }[role] || role
}

function resultLabel(result) {
  return { passed: '已通过', attempted: '尝试过' }[result] || result
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

let searchTimer = null
function debounceSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    loadUsers()
  }, 300)
}

async function loadUsers() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      ...(search.value && { search: search.value }),
      ...(filterRole.value && { role: filterRole.value }),
    }
    const res = await request.get('/admin/users', { params })
    users.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadUsers()
}

async function viewUserDetail(user) {
  selectedUser.value = user
  userStats.value = null
  try {
    const res = await request.get(`/admin/users/${user.id}/stats`)
    userStats.value = res
  } catch (e) {
    console.error(e)
  }
}

async function viewUserSubmissions(user) {
  selectedUser.value = user
  showSubmissions.value = true
  userSubmissions.value = []
  try {
    const res = await request.get(`/admin/users/${user.id}/submissions`, {
      params: { page: 1, page_size: 20 }
    })
    userSubmissions.value = res.items
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadUsers)
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
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 {
  font-size: 20px;
  font-weight: 600;
}

.count-badge {
  font-size: 12px;
  padding: 4px 10px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  border-radius: 10px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-box {
  flex: 1;
  max-width: 320px;
  position: relative;
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

.search-box input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}

.search-box input:focus {
  border-color: var(--accent);
}

.filter-group select {
  padding: 8px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.table-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
}

.data-table td {
  padding: 12px 16px;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover {
  background: var(--bg-hover);
}

.id-cell {
  color: var(--text-muted);
  font-family: monospace;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
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

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 500;
}

.user-email {
  font-size: 12px;
  color: var(--text-muted);
}

.role-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.role-badge.admin { color: #8b5cf6; background: rgba(139, 92, 246, 0.1); }
.role-badge.user { color: #3b82f6; background: rgba(59, 130, 246, 0.1); }

.status-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.status-badge.active { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.status-badge.inactive { color: #ef4444; background: rgba(239, 68, 68, 0.1); }
.status-badge.pending { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.status-badge.completed { color: #10b981; background: rgba(16, 185, 129, 0.1); }

.date-cell {
  color: var(--text-muted);
  font-size: 12px;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn-text {
  padding: 4px 8px;
  background: none;
  border: none;
  color: var(--accent);
  font-size: 13px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.15s;
}

.btn-text:hover {
  background: rgba(var(--accent-rgb), 0.1);
}

.lang-badge {
  font-size: 11px;
  padding: 2px 6px;
  background: var(--bg-tertiary);
  border-radius: 3px;
  font-family: monospace;
}

.result-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.result-badge.passed { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.result-badge.attempted { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.table-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(var(--bg-secondary-rgb), 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.table-empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.page-btn {
  padding: 6px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
}

.page-btn:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.page-info {
  font-size: 13px;
  color: var(--text-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-secondary);
  border-radius: 12px;
  width: 90%;
  max-width: 520px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-wide {
  max-width: 720px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
}

.btn-close {
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h3 {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.detail-avatar {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 600;
}

.detail-header h3 {
  font-size: 16px;
  margin-bottom: 4px;
}

.detail-header p {
  font-size: 13px;
  color: var(--text-muted);
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  padding: 16px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  margin-bottom: 24px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 12px;
  color: var(--text-muted);
}

.detail-value {
  font-size: 14px;
  font-weight: 500;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

.stat-item {
  text-align: center;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: 6px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted);
}

.submissions-table {
  max-height: 400px;
  overflow-y: auto;
}
</style>
