<template>
  <div class="page">
    <Navbar />

    <div class="container">
      <!-- 筛选栏 -->
      <div class="filters">
        <div class="filter-group">
          <button
            v-for="d in difficulties"
            :key="d.value"
            :class="['filter-btn', { active: filters.difficulty === d.value }]"
            :style="filters.difficulty === d.value ? { color: d.color, borderColor: d.color } : {}"
            @click="setDifficulty(d.value)"
          >
            {{ d.label }}
          </button>
        </div>
        <div class="search-box">
          <input
            v-model="filters.tag"
            type="text"
            placeholder="搜索标签..."
            @keyup.enter="loadProblems"
          />
        </div>
      </div>

      <!-- 题目表格 -->
      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th style="width: 60px">#</th>
              <th>题目</th>
              <th style="width: 100px">难度</th>
              <th style="width: 120px">标签</th>
              <th style="width: 100px">时间限制</th>
            </tr>
          </thead>
          <tbody>
            <template v-if="loading">
              <tr v-for="i in 10" :key="i" class="skeleton-row">
                <td><div class="skeleton" style="width: 30px"></div></td>
                <td><div class="skeleton" style="width: 200px"></div></td>
                <td><div class="skeleton" style="width: 50px"></div></td>
                <td><div class="skeleton" style="width: 80px"></div></td>
                <td><div class="skeleton" style="width: 60px"></div></td>
              </tr>
            </template>
            <template v-else>
              <tr
                v-for="problem in problems"
                :key="problem.id"
                class="table-row"
                @click="router.push(`/problems/${problem.id}`)"
              >
                <td class="id-cell">{{ problem.id }}</td>
                <td class="title-cell">{{ problem.title }}</td>
                <td>
                  <span :class="['difficulty-badge', problem.difficulty]">
                    {{ difficultyLabel(problem.difficulty) }}
                  </span>
                </td>
                <td>
                  <span v-for="tag in (problem.tags || []).slice(0, 2)" :key="tag" class="tag">
                    {{ tag }}
                  </span>
                </td>
                <td class="muted">{{ problem.time_limit }}ms</td>
              </tr>
            </template>
          </tbody>
        </table>

        <!-- 空状态 -->
        <div v-if="!loading && problems.length === 0" class="empty">
          暂无题目
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { problemApi } from '../api/problem'

const router = useRouter()

const problems = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const filters = ref({ difficulty: '', tag: '' })

const difficulties = [
  { value: '', label: '全部', color: 'var(--text-primary)' },
  { value: 'easy', label: '简单', color: 'var(--easy-color)' },
  { value: 'medium', label: '中等', color: 'var(--medium-color)' },
  { value: 'hard', label: '困难', color: 'var(--hard-color)' },
]

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

function setDifficulty(val) {
  filters.value.difficulty = val
  page.value = 1
  loadProblems()
}

function changePage(p) {
  page.value = p
  loadProblems()
}

async function loadProblems() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      ...(filters.value.difficulty && { difficulty: filters.value.difficulty }),
      ...(filters.value.tag && { tag: filters.value.tag }),
    }
    const res = await problemApi.getList(params)
    problems.value = (res.items || []).map(p => ({
      ...p,
      tags: typeof p.tags === 'string' ? JSON.parse(p.tags) : (p.tags || []),
    }))
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadProblems)
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

.filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 16px;
}

.filter-group {
  display: flex;
  gap: 8px;
}

.filter-btn {
  padding: 6px 14px;
  background: none;
  border: 1px solid var(--border);
  border-radius: 20px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: var(--text-secondary);
  color: var(--text-primary);
}

.filter-btn.active {
  background: rgba(255, 161, 22, 0.08);
}

.search-box input {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 7px 12px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  width: 200px;
  transition: border-color 0.2s;
}

.search-box input:focus {
  border-color: var(--accent);
}

.search-box input::placeholder {
  color: var(--text-muted);
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

.table thead tr {
  border-bottom: 1px solid var(--border);
}

.table th {
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.table-row {
  cursor: pointer;
  border-bottom: 1px solid var(--border);
  transition: background 0.15s;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: var(--bg-hover);
}

.table td {
  padding: 14px 16px;
  font-size: 14px;
}

.id-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.title-cell {
  color: var(--text-primary);
  font-weight: 500;
}

.table-row:hover .title-cell {
  color: var(--accent);
}

.difficulty-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.difficulty-badge.easy {
  color: var(--easy-color);
  background: rgba(0, 184, 163, 0.1);
}

.difficulty-badge.medium {
  color: var(--medium-color);
  background: rgba(255, 192, 30, 0.1);
}

.difficulty-badge.hard {
  color: var(--hard-color);
  background: rgba(239, 71, 67, 0.1);
}

.tag {
  display: inline-block;
  font-size: 11px;
  padding: 2px 7px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border-radius: 4px;
  margin-right: 4px;
}

.muted {
  color: var(--text-muted);
  font-size: 13px;
}

/* Skeleton loading */
.skeleton {
  height: 14px;
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-hover) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
}

.skeleton-row td {
  padding: 18px 16px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.empty {
  padding: 60px;
  text-align: center;
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
  transition: all 0.2s;
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
  font-size: 13px;
  color: var(--text-muted);
}
</style>