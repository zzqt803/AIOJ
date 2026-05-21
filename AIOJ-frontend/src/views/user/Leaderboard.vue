<template>
  <div class="page">
    <UserNavbar />

    <div class="container">
      <div class="page-header">
        <div>
          <h1>排行榜</h1>
          <p class="subtitle">按通过题目数排名</p>
        </div>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 60px">排名</th>
              <th>用户</th>
              <th style="width: 80px">通过</th>
              <th style="width: 60px">简单</th>
              <th style="width: 60px">中等</th>
              <th style="width: 60px">困难</th>
              <th style="width: 80px">提交</th>
              <th style="width: 80px">连续</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in leaderboard" :key="item.user_id">
              <td class="rank-cell">
                <span :class="['rank', `rank-${item.rank}`]">{{ item.rank }}</span>
              </td>
              <td class="username-cell">{{ item.username }}</td>
              <td class="solved-cell">{{ item.solved_problems }}</td>
              <td class="easy-cell">{{ item.easy_solved }}</td>
              <td class="medium-cell">{{ item.medium_solved }}</td>
              <td class="hard-cell">{{ item.hard_solved }}</td>
              <td class="muted">{{ item.total_submissions }}</td>
              <td class="streak-cell">{{ item.current_streak }}天</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && leaderboard.length === 0" class="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
        </svg>
        <span>暂无数据</span>
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">
          <svg viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/></svg>
        </button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">
          <svg viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/></svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import UserNavbar from '../../components/UserNavbar.vue'
import { statsApi } from '../../api/stats'

const leaderboard = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

async function loadLeaderboard() {
  loading.value = true
  try {
    const res = await statsApi.getLeaderboard({ page: page.value, page_size: pageSize })
    leaderboard.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadLeaderboard()
}

onMounted(loadLeaderboard)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: var(--bg-primary);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: var(--text-muted);
}

.table-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
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
  padding: 14px 16px;
  font-size: 14px;
  border-bottom: 1px solid var(--border);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover {
  background: var(--bg-hover);
}

.rank-cell {
  text-align: center;
}

.rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 700;
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
}

.rank-1 { background: #fbbf24; color: #000; }
.rank-2 { background: #94a3b8; color: #000; }
.rank-3 { background: #b45309; color: #fff; }

.username-cell {
  font-weight: 600;
}

.solved-cell {
  font-weight: 700;
  color: var(--accent);
}

.easy-cell { color: #10b981; font-weight: 600; }
.medium-cell { color: #f59e0b; font-weight: 600; }
.hard-cell { color: #ef4444; font-weight: 600; }

.muted {
  color: var(--text-muted);
}

.streak-cell {
  color: #f59e0b;
  font-weight: 600;
}

.loading, .empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px;
  color: var(--text-muted);
  gap: 12px;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty svg {
  width: 40px;
  height: 40px;
  opacity: 0.4;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 24px;
}

.page-btn {
  width: 36px;
  height: 36px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.page-btn:hover:not(:disabled) { border-color: var(--text-muted); color: var(--text-primary); }
.page-btn:disabled { opacity: 0.3; cursor: not-allowed; }

.page-btn svg {
  width: 14px;
  height: 14px;
}

.page-info {
  font-size: 13px;
  color: var(--text-muted);
  min-width: 50px;
  text-align: center;
  font-weight: 500;
}
</style>
