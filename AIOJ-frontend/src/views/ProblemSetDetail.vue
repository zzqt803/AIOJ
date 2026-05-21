<template>
  <div class="page">
    <Navbar />

    <div class="container" v-if="problemSet">
      <div class="header">
        <div>
          <h1 class="title">{{ problemSet.title }}</h1>
          <p class="desc">{{ problemSet.description }}</p>
          <div class="meta">
            <span>创建者：{{ problemSet.creator_name }}</span>
            <span>{{ problemSet.problems.length }} 题</span>
          </div>
        </div>
      </div>

      <div class="problems-list">
        <div
          v-for="(problem, index) in problemSet.problems"
          :key="problem.problem_id"
          class="problem-item"
          @click="router.push(`/problems/${problem.problem_id}`)"
        >
          <span class="problem-order">{{ index + 1 }}</span>
          <span class="problem-title">{{ problem.title }}</span>
          <span :class="['difficulty-badge', problem.difficulty]">
            {{ difficultyLabel(problem.difficulty) }}
          </span>
        </div>
      </div>

      <div v-if="problemSet.problems.length === 0" class="empty">
        题单中暂无题目
      </div>
    </div>

    <div v-else-if="loading" class="loading">加载中...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { problemSetApi } from '../api/problemSet'

const route = useRoute()
const router = useRouter()
const problemSetId = Number(route.params.id)

const problemSet = ref(null)
const loading = ref(true)

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

async function loadProblemSet() {
  try {
    problemSet.value = await problemSetApi.getDetail(problemSetId)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(loadProblemSet)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: var(--bg-primary);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 32px 24px;
}

.header {
  margin-bottom: 32px;
}

.title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.desc {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 12px;
}

.meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--text-muted);
}

.problems-list {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

.problem-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background 0.15s;
}

.problem-item:last-child {
  border-bottom: none;
}

.problem-item:hover {
  background: var(--bg-hover);
}

.problem-order {
  font-size: 14px;
  color: var(--text-muted);
  min-width: 30px;
}

.problem-title {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
}

.difficulty-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

.difficulty-badge.easy { color: var(--easy-color); background: rgba(0, 184, 163, 0.1); }
.difficulty-badge.medium { color: var(--medium-color); background: rgba(255, 192, 30, 0.1); }
.difficulty-badge.hard { color: var(--hard-color); background: rgba(239, 71, 67, 0.1); }

.loading, .empty {
  text-align: center;
  padding: 60px;
  color: var(--text-muted);
}
</style>
