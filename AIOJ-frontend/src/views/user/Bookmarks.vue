<template>
  <div class="page">
    <UserNavbar />

    <div class="container">
      <div class="page-header">
        <div>
          <h1>我的收藏</h1>
          <p class="subtitle">收藏的题目</p>
        </div>
      </div>

      <div class="bookmarks-grid">
        <div
          v-for="bookmark in bookmarks"
          :key="bookmark.id"
          class="bookmark-card"
          @click="router.push(`/problems/${bookmark.problem_id}`)"
        >
          <div class="card-top">
            <span class="problem-id">{{ bookmark.problem_id }}</span>
            <span :class="['difficulty-badge', bookmark.difficulty]">
              {{ difficultyLabel(bookmark.difficulty) }}
            </span>
          </div>
          <h3 class="card-title">{{ bookmark.title }}</h3>
          <div class="card-footer">
            <span class="bookmark-time">{{ formatDate(bookmark.created_at) }}</span>
            <button class="btn-unbookmark" @click.stop="unbookmark(bookmark.problem_id)">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 2v13.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2z"/></svg>
              取消收藏
            </button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>加载中...</span>
      </div>

      <div v-if="!loading && bookmarks.length === 0" class="empty">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <path d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
        </svg>
        <span>暂无收藏</span>
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
import { bookmarkApi } from '../../api/bookmark'

const router = useRouter()
const bookmarks = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('zh-CN')
}

async function loadBookmarks() {
  loading.value = true
  try {
    const res = await bookmarkApi.getList({ page: page.value, page_size: pageSize })
    bookmarks.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadBookmarks()
}

async function unbookmark(problemId) {
  try {
    await bookmarkApi.delete(problemId)
    loadBookmarks()
  } catch (e) {
    console.error(e)
  }
}

onMounted(loadBookmarks)
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

.bookmarks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.bookmark-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.15s ease-out;
}

.bookmark-card:hover {
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
}

.difficulty-badge.easy { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.difficulty-badge.medium { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.difficulty-badge.hard { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.card-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-primary);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.bookmark-time {
  font-size: 12px;
  color: var(--text-muted);
}

.btn-unbookmark {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  padding: 4px 10px;
  background: none;
  border: 1px solid var(--border);
  border-radius: 4px;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.15s;
}

.btn-unbookmark:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-unbookmark svg {
  width: 12px;
  height: 12px;
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
