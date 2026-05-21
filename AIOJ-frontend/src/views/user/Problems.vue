<template>
  <div class="page">
    <UserNavbar />

    <div class="container">
      <div class="page-header">
        <div>
          <h1>题库</h1>
          <p class="subtitle">挑战自己，提升编程能力</p>
        </div>
        <div class="header-stats">
          <div class="stat">
            <span class="stat-value">{{ total }}</span>
            <span class="stat-label">道题目</span>
          </div>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filters">
        <div class="filter-group">
          <button
            v-for="d in difficulties"
            :key="d.value"
            :class="['filter-btn', { active: filters.difficulty === d.value }]"
            @click="setDifficulty(d.value)"
          >
            {{ d.label }}
          </button>
        </div>
        <div class="search-box">
          <svg class="search-icon" viewBox="0 0 16 16" fill="currentColor">
            <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001c.03.04.062.078.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1.007 1.007 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0z"/>
          </svg>
          <input
            v-model="filters.tag"
            type="text"
            placeholder="搜索标签..."
            @keyup.enter="loadProblems"
          />
        </div>
      </div>

      <!-- 题目卡片网格 -->
      <div class="problems-grid">
        <div
          v-for="problem in problems"
          :key="problem.id"
          class="problem-card"
          @click="router.push(`/problems/${problem.id}`)"
        >
          <div class="card-top">
            <span class="problem-id">{{ problem.id }}</span>
            <span :class="['difficulty-badge', problem.difficulty]">
              {{ difficultyLabel(problem.difficulty) }}
            </span>
          </div>
          <h3 class="card-title">{{ problem.title }}</h3>
          <div class="card-tags">
            <span v-for="tag in (problem.tags || []).slice(0, 3)" :key="tag" class="tag">
              {{ tag }}
            </span>
          </div>
          <div class="card-bottom">
            <div class="limit">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 3.5a.5.5 0 0 0-1 0V8a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 7.71V3.5z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/></svg>
              <span>{{ problem.time_limit }}ms</span>
            </div>
            <div class="limit">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>
              <span>{{ problem.memory_limit }}MB</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && problems.length === 0" class="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
        </svg>
        <span>暂无题目</span>
      </div>

      <!-- 分页 -->
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
import { useRouter } from 'vue-router'
import UserNavbar from '../../components/UserNavbar.vue'
import { problemApi } from '../../api/problem'

const router = useRouter()
const problems = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const filters = ref({ difficulty: '', tag: '' })

const difficulties = [
  { value: '', label: '全部' },
  { value: 'easy', label: '简单' },
  { value: 'medium', label: '中等' },
  { value: 'hard', label: '困难' },
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
    problems.value = res.items
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
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

.header-stats {
  display: flex;
  gap: 24px;
}

.stat {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 14px;
  color: var(--text-muted);
}

.filters {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
}

.filter-group {
  display: flex;
  gap: 6px;
}

.filter-btn {
  padding: 7px 16px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease-out;
}

.filter-btn:hover {
  border-color: var(--text-muted);
  color: var(--text-primary);
}

.filter-btn.active {
  background: var(--text-primary);
  border-color: var(--text-primary);
  color: var(--bg-primary);
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 14px;
  height: 14px;
  color: var(--text-muted);
}

.search-box input {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 7px 12px 7px 34px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  width: 220px;
  transition: border-color 0.15s;
}

.search-box input:focus {
  border-color: var(--accent);
}

.search-box input::placeholder {
  color: var(--text-muted);
}

.problems-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.problem-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.15s ease-out;
}

.problem-card:hover {
  border-color: var(--text-muted);
  transform: translateY(-1px);
}

.card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.problem-id {
  font-size: 12px;
  color: var(--text-muted);
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
}

.difficulty-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 600;
  letter-spacing: 0.3px;
}

.difficulty-badge.easy {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.difficulty-badge.medium {
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.difficulty-badge.hard {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
  line-height: 1.4;
  color: var(--text-primary);
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}

.tag {
  font-size: 11px;
  padding: 3px 8px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  border-radius: 4px;
  font-weight: 500;
}

.card-bottom {
  display: flex;
  gap: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.limit {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
}

.limit svg {
  width: 13px;
  height: 13px;
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
  margin-top: 32px;
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

.page-btn:hover:not(:disabled) {
  border-color: var(--text-muted);
  color: var(--text-primary);
}

.page-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

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
