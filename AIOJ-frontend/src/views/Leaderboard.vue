<template>
  <div class="page">
    <Navbar />

    <div class="container">
      <h1 class="page-title">排行榜</h1>

      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th style="width: 60px">排名</th>
              <th>用户</th>
              <th style="width: 80px">通过数</th>
              <th style="width: 60px">简单</th>
              <th style="width: 60px">中等</th>
              <th style="width: 60px">困难</th>
              <th style="width: 80px">提交数</th>
              <th style="width: 80px">连续天数</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in leaderboard" :key="item.user_id" class="table-row">
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

      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="!loading && leaderboard.length === 0" class="empty">暂无数据</div>

      <!-- 分页 -->
      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import { statsApi } from '../api/stats'

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
  max-width: 900px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
}

.table-wrap {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.table {
  width: 100%;
  border-collapse: collapse;
}

.table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid var(--border);
}

.table-row {
  border-bottom: 1px solid var(--border);
}

.table-row:last-child {
  border-bottom: none;
}

.table td {
  padding: 14px 16px;
  font-size: 14px;
}

.rank-cell {
  text-align: center;
}

.rank {
  display: inline-block;
  width: 28px;
  height: 28px;
  line-height: 28px;
  text-align: center;
  border-radius: 50%;
  font-size: 13px;
  font-weight: 600;
}

.rank-1 { background: #FFD700; color: #000; }
.rank-2 { background: #C0C0C0; color: #000; }
.rank-3 { background: #CD7F32; color: #000; }

.username-cell {
  font-weight: 500;
}

.solved-cell {
  font-weight: 600;
  color: var(--accent);
}

.easy-cell { color: var(--easy-color); }
.medium-cell { color: var(--medium-color); }
.hard-cell { color: var(--hard-color); }

.muted {
  color: var(--text-muted);
}

.streak-cell {
  color: var(--yellow);
}

.loading, .empty {
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 24px;
}

.page-btn {
  padding: 7px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
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
</style>
