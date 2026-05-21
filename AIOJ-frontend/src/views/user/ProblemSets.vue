<template>
  <div class="page">
    <UserNavbar />

    <div class="container">
      <div class="page-header">
        <div>
          <h1>题单</h1>
          <p class="subtitle">按专题刷题，系统提升</p>
        </div>
      </div>

      <div class="sets-grid">
        <div
          v-for="set in problemSets"
          :key="set.id"
          class="set-card"
          @click="router.push(`/problem-sets/${set.id}`)"
        >
          <h3 class="set-title">{{ set.title }}</h3>
          <p class="set-desc">{{ set.description || '暂无描述' }}</p>
          <div class="set-footer">
            <div class="set-count">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M7 3a1 1 0 000 2h6a1 1 0 100-2H7zM4 7a1 1 0 011-1h10a1 1 0 110 2H5a1 1 0 01-1-1zM2 11a2 2 0 012-2h12a2 2 0 012 2v4a2 2 0 01-2 2H4a2 2 0 01-2-2v-4z"/></svg>
              <span>{{ set.problem_count }} 题</span>
            </div>
            <span class="set-creator">{{ set.creator_name }}</span>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && problemSets.length === 0" class="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>
        </svg>
        <span>暂无题单</span>
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
import { useRouter } from 'vue-router'
import UserNavbar from '../../components/UserNavbar.vue'
import { problemSetApi } from '../../api/problemSet'

const router = useRouter()
const problemSets = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

async function loadProblemSets() {
  loading.value = true
  try {
    const res = await problemSetApi.getList({ page: page.value, page_size: pageSize })
    problemSets.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadProblemSets()
}

onMounted(loadProblemSets)
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
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 4px;
  letter-spacing: -0.5px;
}

.subtitle {
  font-size: 14px;
  color: var(--text-muted);
}

.sets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 12px;
}

.set-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.15s ease-out;
}

.set-card:hover {
  border-color: var(--text-muted);
  transform: translateY(-1px);
}

.set-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.set-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

.set-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.set-count {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--accent);
  font-weight: 600;
}

.set-count svg {
  width: 14px;
  height: 14px;
}

.set-creator {
  font-size: 12px;
  color: var(--text-muted);
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
