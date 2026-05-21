<template>
  <div class="page">
    <UserNavbar />

    <div class="container">
      <div class="page-header">
        <h1>提交记录</h1>
        <p class="subtitle">查看我的所有提交</p>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>题目</th>
              <th>语言</th>
              <th>状态</th>
              <th>结果</th>
              <th>耗时</th>
              <th>内存</th>
              <th>提交时间</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sub in submissions" :key="sub.id" @click="router.push(`/problems/${sub.problem_id}`)">
              <td class="id-cell">{{ sub.id }}</td>
              <td class="problem-cell">#{{ sub.problem_id }}</td>
              <td>
                <span class="lang-badge">{{ sub.language }}</span>
              </td>
              <td>
                <span :class="['status-badge', sub.status]">
                  {{ sub.status === 'pending' ? '判题中' : '已完成' }}
                </span>
              </td>
              <td>
                <span :class="['result-badge', sub.result]" v-if="sub.result">
                  {{ resultLabel(sub.result) }}
                </span>
                <span v-else class="muted">-</span>
              </td>
              <td class="muted">{{ sub.time_used ? `${sub.time_used}ms` : '-' }}</td>
              <td class="muted">{{ sub.memory_used ? `${Math.round(sub.memory_used / 1024)}MB` : '-' }}</td>
              <td class="date-cell">{{ formatDate(sub.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && submissions.length === 0" class="empty">
        <span class="empty-icon">📝</span>
        <span>暂无提交记录</span>
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import UserNavbar from '../../components/UserNavbar.vue'
import { submissionApi } from '../../api/submission'

const router = useRouter()
const submissions = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

function resultLabel(result) {
  const map = {
    passed: '已通过',
    attempted: '尝试过',
  }
  return map[result] || result
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

async function loadSubmissions() {
  loading.value = true
  try {
    const res = await submissionApi.getList({ page: page.value, page_size: pageSize })
    submissions.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadSubmissions()
}

onMounted(loadSubmissions)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: var(--bg-primary);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 15px;
  color: var(--text-secondary);
}

.table-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  padding: 14px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border);
}

.data-table td {
  padding: 16px;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr {
  cursor: pointer;
  transition: background 0.15s;
}

.data-table tr:hover {
  background: var(--bg-hover);
}

.id-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.problem-cell {
  font-weight: 600;
}

.lang-badge {
  font-size: 12px;
  padding: 3px 10px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-family: monospace;
}

.status-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.status-badge.pending {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.status-badge.completed {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.result-badge {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 12px;
  font-weight: 600;
}

.result-badge.passed {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.result-badge.attempted {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.muted {
  color: var(--text-muted);
}

.date-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.loading, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: var(--text-muted);
  gap: 12px;
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

.empty-icon {
  font-size: 32px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.page-btn {
  padding: 8px 20px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: var(--text-muted);
}
</style>
