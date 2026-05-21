<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <div class="content-header">
        <div class="header-left">
          <h1>题目管理</h1>
          <span class="count-badge">{{ total }} 道题目</span>
        </div>
        <button class="btn-primary" @click="openCreateModal">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/>
          </svg>
          新建题目
        </button>
      </div>

      <!-- 搜索和筛选 -->
      <div class="toolbar">
        <div class="search-box">
          <svg viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/>
          </svg>
          <input v-model="search" type="text" placeholder="搜索题目..." @input="debounceSearch" />
        </div>
        <div class="filter-group">
          <select v-model="filterDifficulty" @change="loadProblems">
            <option value="">全部难度</option>
            <option value="easy">简单</option>
            <option value="medium">中等</option>
            <option value="hard">困难</option>
          </select>
        </div>
      </div>

      <!-- 题目表格 -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width: 60px">ID</th>
              <th>标题</th>
              <th style="width: 80px">难度</th>
              <th style="width: 160px">标签</th>
              <th style="width: 80px">状态</th>
              <th style="width: 100px">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="problem in problems" :key="problem.id">
              <td class="id-cell">{{ problem.id }}</td>
              <td>
                <div class="title-cell">
                  <span class="title">{{ problem.title }}</span>
                  <span class="limits">{{ problem.time_limit }}ms / {{ problem.memory_limit }}MB</span>
                </div>
              </td>
              <td>
                <span :class="['difficulty-badge', problem.difficulty]">
                  {{ difficultyLabel(problem.difficulty) }}
                </span>
              </td>
              <td>
                <div class="tags-cell">
                  <span v-for="tag in (problem.tags || []).slice(0, 2)" :key="tag" class="tag">
                    {{ tag }}
                  </span>
                  <span v-if="(problem.tags || []).length > 2" class="tag-more">
                    +{{ problem.tags.length - 2 }}
                  </span>
                </div>
              </td>
              <td>
                <span :class="['status-badge', problem.is_public ? 'public' : 'private']">
                  {{ problem.is_public ? '公开' : '隐藏' }}
                </span>
              </td>
              <td>
                <div class="actions">
                  <button class="btn-icon" @click="editProblem(problem)" title="编辑">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                      <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"/>
                    </svg>
                  </button>
                  <button class="btn-icon btn-danger" @click="deleteProblem(problem.id)" title="删除">
                    <svg viewBox="0 0 20 20" fill="currentColor">
                      <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"/>
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="loading" class="table-loading">
          <div class="spinner"></div>
        </div>

        <div v-if="!loading && problems.length === 0" class="table-empty">
          <span>暂无题目</span>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="totalPages > 1">
        <button class="page-btn" :disabled="page === 1" @click="changePage(page - 1)">上一页</button>
        <span class="page-info">{{ page }} / {{ totalPages }}</span>
        <button class="page-btn" :disabled="page >= totalPages" @click="changePage(page + 1)">下一页</button>
      </div>
    </div>

    <!-- 创建/编辑模态框 -->
    <Teleport to="body">
      <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
        <div class="modal">
          <div class="modal-header">
            <h2>{{ editingProblem ? '编辑题目' : '新建题目' }}</h2>
            <button class="btn-close" @click="closeModal">
              <svg viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>

          <form @submit.prevent="submitForm" class="modal-body">
            <div class="form-section">
              <h3>基本信息</h3>
              <div class="form-group">
                <label>题目标题</label>
                <input v-model="form.title" type="text" required placeholder="输入题目标题" />
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
                <label>标签</label>
                <div class="tags-input">
                  <div class="tag-list">
                    <span v-for="(tag, index) in form.tags" :key="index" class="tag-item">
                      {{ tag }}
                      <button type="button" @click="removeTag(index)">&times;</button>
                    </span>
                  </div>
                  <input
                    v-model="newTag"
                    type="text"
                    placeholder="输入标签后按回车"
                    @keydown.enter.prevent="addTag"
                  />
                </div>
              </div>

              <div class="form-group">
                <label class="checkbox-label">
                  <input v-model="form.is_public" type="checkbox" />
                  <span>公开题目</span>
                </label>
              </div>
            </div>

            <div class="form-section">
              <h3>题目内容</h3>
              <div class="form-group">
                <label>题目描述</label>
                <textarea v-model="form.description" rows="4" required placeholder="详细描述题目要求"></textarea>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>输入格式</label>
                  <textarea v-model="form.input_format" rows="2" required placeholder="描述输入格式"></textarea>
                </div>
                <div class="form-group">
                  <label>输出格式</label>
                  <textarea v-model="form.output_format" rows="2" required placeholder="描述输出格式"></textarea>
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label>样例输入</label>
                  <textarea v-model="form.sample_input" rows="2" required placeholder="样例输入"></textarea>
                </div>
                <div class="form-group">
                  <label>样例输出</label>
                  <textarea v-model="form.sample_output" rows="2" required placeholder="样例输出"></textarea>
                </div>
              </div>

              <div class="form-group">
                <label>提示（可选）</label>
                <textarea v-model="form.hint" rows="2" placeholder="解题提示"></textarea>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn-secondary" @click="closeModal">取消</button>
              <button type="submit" class="btn-primary" :disabled="submitting">
                {{ submitting ? '保存中...' : (editingProblem ? '保存修改' : '创建题目') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import AdminSidebar from '../../components/AdminSidebar.vue'
import request from '../../api/request'

const problems = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 20
const loading = ref(false)
const search = ref('')
const filterDifficulty = ref('')
const showModal = ref(false)
const editingProblem = ref(null)
const submitting = ref(false)
const newTag = ref('')

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

let searchTimer = null
function debounceSearch() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    page.value = 1
    loadProblems()
  }, 300)
}

async function loadProblems() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      ...(filterDifficulty.value && { difficulty: filterDifficulty.value }),
      ...(search.value && { tag: search.value }),
    }
    const res = await request.get('/problems', { params })
    problems.value = res.items
    total.value = res.total
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

function changePage(p) {
  page.value = p
  loadProblems()
}

function openCreateModal() {
  editingProblem.value = null
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
  showModal.value = true
}

function editProblem(problem) {
  editingProblem.value = problem
  form.value = {
    title: problem.title,
    difficulty: problem.difficulty,
    tags: [...(problem.tags || [])],
    description: problem.description || '',
    input_format: problem.input_format || '',
    output_format: problem.output_format || '',
    sample_input: problem.sample_input || '',
    sample_output: problem.sample_output || '',
    hint: problem.hint || '',
    time_limit: problem.time_limit,
    memory_limit: problem.memory_limit,
    is_public: problem.is_public,
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingProblem.value = null
}

function addTag() {
  const tag = newTag.value.trim()
  if (tag && !form.value.tags.includes(tag)) {
    form.value.tags.push(tag)
  }
  newTag.value = ''
}

function removeTag(index) {
  form.value.tags.splice(index, 1)
}

async function submitForm() {
  submitting.value = true
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
  } finally {
    submitting.value = false
  }
}

async function deleteProblem(id) {
  if (!confirm('确定要删除这道题目吗？此操作不可撤销。')) return
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
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

.admin-content {
  flex: 1;
  padding: 24px 32px;
  overflow-y: auto;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-left h1 {
  font-size: 20px;
  font-weight: 600;
}

.count-badge {
  font-size: 12px;
  padding: 4px 10px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
  border-radius: 10px;
}

.btn-primary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  font-size: 13px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-primary svg {
  width: 16px;
  height: 16px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-box {
  flex: 1;
  max-width: 320px;
  position: relative;
}

.search-box svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: var(--text-muted);
}

.search-box input {
  width: 100%;
  padding: 8px 12px 8px 36px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}

.search-box input:focus {
  border-color: var(--accent);
}

.filter-group select {
  padding: 8px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  cursor: pointer;
}

.table-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
  position: relative;
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
  padding: 12px 16px;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
}

.data-table tr:last-child td {
  border-bottom: none;
}

.data-table tr:hover {
  background: var(--bg-hover);
}

.id-cell {
  color: var(--text-muted);
  font-family: monospace;
}

.title-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title {
  font-weight: 500;
}

.limits {
  font-size: 11px;
  color: var(--text-muted);
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

.tags-cell {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.tag {
  font-size: 11px;
  padding: 2px 6px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border-radius: 3px;
}

.tag-more {
  font-size: 11px;
  padding: 2px 6px;
  color: var(--text-muted);
}

.status-badge {
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  font-weight: 500;
}

.status-badge.public { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.status-badge.private { color: var(--text-muted); background: var(--bg-tertiary); }

.actions {
  display: flex;
  gap: 4px;
}

.btn-icon {
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 4px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.btn-icon:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-icon.btn-danger:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.btn-icon svg {
  width: 14px;
  height: 14px;
}

.table-loading {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(var(--bg-secondary-rgb), 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
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

.table-empty {
  padding: 40px;
  text-align: center;
  color: var(--text-muted);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.page-btn {
  padding: 6px 14px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
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
  border-radius: 12px;
  width: 90%;
  max-width: 720px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid var(--border);
}

.modal-header h2 {
  font-size: 18px;
  font-weight: 600;
}

.btn-close {
  width: 28px;
  height: 28px;
  background: none;
  border: none;
  border-radius: 6px;
  color: var(--text-muted);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.form-section {
  margin-bottom: 24px;
}

.form-section h3 {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  outline: none;
  transition: border-color 0.15s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: var(--accent);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
  line-height: 1.5;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

.tags-input {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 6px 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.tags-input:focus-within {
  border-color: var(--accent);
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  background: var(--bg-secondary);
  border-radius: 4px;
  font-size: 12px;
}

.tag-item button {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 14px;
  line-height: 1;
}

.tag-item button:hover {
  color: var(--text-primary);
}

.tags-input input {
  flex: 1;
  min-width: 100px;
  padding: 4px;
  background: none;
  border: none;
  outline: none;
  font-size: 13px;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input {
  width: auto !important;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border);
}

.btn-secondary {
  padding: 8px 16px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
}

.btn-secondary:hover {
  border-color: var(--text-secondary);
}
</style>
