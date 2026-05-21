<template>
  <div class="page">
    <Navbar />

    <div class="container">
      <h1 class="page-title">题单</h1>

      <div class="sets-grid">
        <div
          v-for="set in problemSets"
          :key="set.id"
          class="set-card"
          @click="router.push(`/problem-sets/${set.id}`)"
        >
          <h3 class="set-title">{{ set.title }}</h3>
          <p class="set-desc">{{ set.description || '暂无描述' }}</p>
          <div class="set-meta">
            <span class="set-count">{{ set.problem_count }} 题</span>
            <span class="set-creator">{{ set.creator_name }}</span>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">加载中...</div>
      <div v-if="!loading && problemSets.length === 0" class="empty">暂无题单</div>

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
import { useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { problemSetApi } from '../api/problemSet'

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
  max-width: 1000px;
  margin: 0 auto;
  padding: 32px 24px;
}

.page-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 24px;
}

.sets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.set-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.set-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
}

.set-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
}

.set-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.set-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
}

.set-count {
  color: var(--accent);
}

.loading, .empty {
  text-align: center;
  padding: 40px;
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
