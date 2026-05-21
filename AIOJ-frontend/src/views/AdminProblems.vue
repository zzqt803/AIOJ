<template>
  <div class="page">
    <Navbar />

    <div class="container">
      <div class="header">
        <h1>题目管理</h1>
        <button class="btn-primary" @click="showCreateModal = true">新建题目</button>
      </div>

      <!-- 题目表格 -->
      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th style="width: 60px">#</th>
              <th>标题</th>
              <th style="width: 100px">难度</th>
              <th style="width: 100px">状态</th>
              <th style="width: 150px">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="problem in problems" :key="problem.id" class="table-row">
              <td class="id-cell">{{ problem.id }}</td>
              <td class="title-cell">{{ problem.title }}</td>
              <td>
                <span :class="['difficulty-badge', problem.difficulty]">
                  {{ difficultyLabel(problem.difficulty) }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', problem.is_public ? 'public' : 'private']">
                  {{ problem.is_public ? '公开' : '隐藏' }}
                </span>
              </td>
              <td class="actions">
                <button class="btn-edit" @click="editProblem(problem)">编辑</button>
                <button class="btn-delete" @click="deleteProblem(problem.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">第 {{ page }} 页 / 共 {{ totalPages }} 页</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>

    <!-- 创建/编辑模态框 -->
    <div class="modal-overlay" v-if="showCreateModal || editingProblem" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingProblem ? '编辑题目' : '新建题目' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>标题</label>
            <input v-model="form.title" type="text" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>难度</label>
              <select v-model="form.difficulty">
                <option value="easy">简单</option>
                <option value="medium">中等</option>
                <option value="hard">困难</option>
              </select>
            </div>
            <div class="form-group">
              <label>时间限制 (ms)</label>
              <input v-model.number="form.time_limit" type="number" min="100" max="10000" />
            </div>
            <div class="form-group">
              <label>内存限制 (MB)</label>
              <input v-model.number="form.memory_limit" type="number" min="16" max="1024" />
            </div>
          </div>
          <div class="form-group">
            <label>标签（逗号分隔）</label>
            <input v-model="tagsInput" type="text" placeholder="数组,哈希表" />
          </div>
          <div class="form-group">
            <label>题目描述</label>
            <textarea v-model="form.description" rows="4" required></textarea>
          </div>
          <div class="form-group">
            <label>输入格式</label>
            <textarea v-model="form.input_format" rows="2" required></textarea>
          </div>
          <div class="form-group">
            <label>输出格式</label>
            <textarea v-model="form.output_format" rows="2" required></textarea>
          </div>
          <div class="form-group">
            <label>样例输入</label>
            <textarea v-model="form.sample_input" rows="2" required></textarea>
          </div>
          <div class="form-group">
            <label>样例输出</label>
            <textarea v-model="form.sample_output" rows="2" required></textarea>
          </div>
          <div class="form-group">
            <label>提示（可选）</label>
            <textarea v-model="form.hint" rows="2"></textarea>
          </div>
          <div class="form-group">
            <label>
              <input v-model="form.is_public" type="checkbox" />
              公开题目
            </label>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn-primary">{{ editingProblem ? '保存' : '创建' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import request from '../api/request'

const problems = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const showCreateModal = ref(false)
const editingProblem = ref(null)

const tagsInput = ref('')
const form = ref({
  title: '',
  difficulty: 'easy',
  tags: [],
  description: '',
  input_format: '',
  output_format: '',
  sample_input: '',
  sample_output: '',
  hint: '',
  time_limit: 1000,
  memory_limit: 256,
  is_public: true,
})

const totalPages = computed(() => Math.ceil(total.value / pageSize) || 1)

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

async function loadProblems() {
  try {
    const res = await request.get('/problems', {
      params: { page: page.value, page_size: pageSize }
    })
    problems.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  }
}

function changePage(p) {
  page.value = p
  loadProblems()
}

function editProblem(problem) {
  editingProblem.value = problem
  form.value = { ...problem }
  tagsInput.value = (problem.tags || []).join(',')
}

function closeModal() {
  showCreateModal.value = false
  editingProblem.value = null
  resetForm()
}

function resetForm() {
  form.value = {
    title: '',
    difficulty: 'easy',
    tags: [],
    description: '',
    input_format: '',
    output_format: '',
    sample_input: '',
    sample_output: '',
    hint: '',
    time_limit: 1000,
    memory_limit: 256,
    is_public: true,
  }
  tagsInput.value = ''
}

async function submitForm() {
  form.value.tags = tagsInput.value.split(',').map(t => t.trim()).filter(Boolean)

  try {
    if (editingProblem.value) {
      await request.put(`/problems/${editingProblem.value.id}`, form.value)
    } else {
      await request.post('/problems', form.value)
    }
    closeModal()
    loadProblems()
  } catch (e) {
    alert(e.response?.data?.detail || '操作失败')
  }
}

async function deleteProblem(id) {
  if (!confirm('确定要删除这道题目吗？')) return
  try {
    await request.delete(`/problems/${id}`)
    loadProblems()
  } catch (e) {
    alert(e.response?.data?.detail || '删除失败')
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

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
}

.btn-primary {
  padding: 8px 20px;
  background: var(--accent);
  color: #1a1a1a;
  font-weight: 600;
  font-size: 14px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.btn-primary:hover {
  background: var(--accent-hover);
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

.id-cell {
  color: var(--text-muted);
  font-size: 13px;
}

.title-cell {
  color: var(--text-primary);
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

.status-badge {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 10px;
}

.status-badge.public { color: var(--green); background: rgba(0, 184, 163, 0.1); }
.status-badge.private { color: var(--text-muted); background: var(--bg-tertiary); }

.actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  padding: 4px 12px;
  font-size: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
}

.btn-edit:hover { border-color: var(--accent); color: var(--accent); }
.btn-delete:hover { border-color: var(--red); color: var(--red); }

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
  border-radius: var(--radius);
  padding: 24px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h2 {
  margin-bottom: 20px;
  font-size: 18px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--accent);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-secondary {
  padding: 8px 20px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: var(--text-secondary);
}
</style>
