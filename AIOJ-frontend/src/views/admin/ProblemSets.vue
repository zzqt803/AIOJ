<template>
  <div class="admin-layout">
    <AdminSidebar />
    <div class="admin-content">
      <div class="content-header">
        <div>
          <h1>题单管理</h1>
          <p class="subtitle">管理所有题单</p>
        </div>
        <button class="btn-primary" @click="showCreateModal = true">
          + 新建题单
        </button>
      </div>

      <!-- 题单列表 -->
      <div class="sets-grid">
        <div v-for="set in problemSets" :key="set.id" class="set-card">
          <div class="set-header">
            <h3>{{ set.title }}</h3>
            <span :class="['status-badge', set.is_public ? 'public' : 'private']">
              {{ set.is_public ? '公开' : '隐藏' }}
            </span>
          </div>
          <p class="set-desc">{{ set.description || '暂无描述' }}</p>
          <div class="set-meta">
            <span>{{ set.problem_count || 0 }} 题</span>
            <span>{{ set.creator_name }}</span>
          </div>
          <div class="set-actions">
            <button class="btn-edit" @click="editSet(set)">编辑</button>
            <button class="btn-manage" @click="manageProblems(set)">管理题目</button>
            <button class="btn-delete" @click="deleteSet(set.id)">删除</button>
          </div>
        </div>
      </div>

      <div v-if="problemSets.length === 0" class="empty">暂无题单</div>
    </div>

    <!-- 创建/编辑模态框 -->
    <div class="modal-overlay" v-if="showCreateModal || editingSet" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingSet ? '编辑题单' : '新建题单' }}</h2>
        <form @submit.prevent="submitForm">
          <div class="form-group">
            <label>标题</label>
            <input v-model="form.title" type="text" required placeholder="题单标题" />
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="form.description" rows="3" placeholder="题单描述"></textarea>
          </div>
          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.is_public" type="checkbox" />
              <span>公开题单</span>
            </label>
          </div>
          <div class="form-actions">
            <button type="button" class="btn-secondary" @click="closeModal">取消</button>
            <button type="submit" class="btn-primary">{{ editingSet ? '保存' : '创建' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 管理题目模态框 -->
    <div class="modal-overlay" v-if="managingSet" @click.self="closeManageModal">
      <div class="modal modal-wide">
        <h2>管理题目 - {{ managingSet.title }}</h2>

        <div class="add-problem-row">
          <input
            v-model="addProblemId"
            type="number"
            placeholder="输入题目 ID"
            class="input-id"
            @keyup.enter="addProblem"
          />
          <button class="btn-primary btn-sm" @click="addProblem" :disabled="!addProblemId || addingProblem">
            {{ addingProblem ? '添加中...' : '添加' }}
          </button>
        </div>

        <div class="problem-list">
          <div v-if="managingProblems.length === 0" class="empty-list">题单中暂无题目</div>
          <div v-for="p in managingProblems" :key="p.problem_id" class="problem-row">
            <span class="problem-id">{{ p.problem_id }}</span>
            <span class="problem-title">{{ p.title }}</span>
            <span :class="['difficulty-badge', p.difficulty]">{{ difficultyLabel(p.difficulty) }}</span>
            <span class="problem-order">排序: {{ p.sort_order }}</span>
            <button class="btn-remove" @click="removeProblem(p.problem_id)">移除</button>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" class="btn-secondary" @click="closeManageModal">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AdminSidebar from '../../components/AdminSidebar.vue'
import { problemSetApi } from '../../api/problemSet'

const problemSets = ref([])
const showCreateModal = ref(false)
const editingSet = ref(null)
const managingSet = ref(null)
const managingProblems = ref([])
const addProblemId = ref('')
const addingProblem = ref(false)

const form = ref({
  title: '',
  description: '',
  is_public: true,
})

async function loadProblemSets() {
  try {
    const res = await problemSetApi.getList({ page: 1, page_size: 100 })
    problemSets.value = res.items
  } catch (e) {
    console.error(e)
  }
}

function editSet(set) {
  editingSet.value = set
  form.value = { ...set }
}

function closeModal() {
  showCreateModal.value = false
  editingSet.value = null
  form.value = { title: '', description: '', is_public: true }
}

async function submitForm() {
  try {
    if (editingSet.value) {
      await problemSetApi.update(editingSet.value.id, form.value)
    } else {
      await problemSetApi.create(form.value)
    }
    closeModal()
    loadProblemSets()
  } catch (e) {
    alert(e.response?.data?.detail || '操作失败')
  }
}

async function deleteSet(id) {
  if (!confirm('确定要删除这个题单吗？')) return
  try {
    await problemSetApi.delete(id)
    loadProblemSets()
  } catch (e) {
    alert(e.response?.data?.detail || '删除失败')
  }
}

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

async function manageProblems(set) {
  managingSet.value = set
  await loadManagingProblems(set.id)
}

async function loadManagingProblems(setId) {
  try {
    const res = await problemSetApi.getDetail(setId)
    managingProblems.value = res.problems || []
  } catch (e) {
    console.error(e)
  }
}

function closeManageModal() {
  managingSet.value = null
  managingProblems.value = []
  addProblemId.value = ''
}

async function addProblem() {
  const pid = parseInt(addProblemId.value)
  if (!pid || addingProblem.value) return
  addingProblem.value = true
  try {
    await problemSetApi.addProblem(managingSet.value.id, { problem_id: pid, sort_order: managingProblems.value.length })
    addProblemId.value = ''
    await loadManagingProblems(managingSet.value.id)
  } catch (e) {
    alert(e.response?.data?.detail || '添加失败')
  } finally {
    addingProblem.value = false
  }
}

async function removeProblem(problemId) {
  if (!confirm(`确定要从题单中移除题目 ${problemId} 吗？`)) return
  try {
    await problemSetApi.removeProblem(managingSet.value.id, problemId)
    await loadManagingProblems(managingSet.value.id)
  } catch (e) {
    alert(e.response?.data?.detail || '移除失败')
  }
}

onMounted(loadProblemSets)
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
  background: var(--bg-primary);
}

.admin-content {
  flex: 1;
  padding: 32px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.content-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.btn-primary {
  padding: 10px 20px;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.sets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.set-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px;
}

.set-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.set-header h3 {
  font-size: 16px;
  font-weight: 600;
}

.status-badge {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 12px;
  font-weight: 500;
}

.status-badge.public {
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.status-badge.private {
  color: var(--text-muted);
  background: var(--bg-tertiary);
}

.set-desc {
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}

.set-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--border);
}

.set-actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  flex: 1;
  padding: 8px;
  font-size: 13px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  transition: all 0.15s;
}

.btn-edit:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-delete:hover {
  border-color: #ef4444;
  color: #ef4444;
}

.empty {
  text-align: center;
  padding: 60px;
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
  max-width: 500px;
}

.modal h2 {
  margin-bottom: 24px;
  font-size: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--accent);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
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

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.btn-secondary {
  padding: 10px 20px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
}

.btn-manage {
  flex: 1;
  padding: 8px;
  font-size: 13px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  transition: all 0.15s;
}

.btn-manage:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.modal-wide {
  max-width: 640px;
}

.add-problem-row {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.input-id {
  flex: 1;
  padding: 8px 12px;
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
}

.input-id:focus {
  border-color: var(--accent);
}

.btn-sm {
  padding: 8px 16px;
  font-size: 13px;
}

.problem-list {
  max-height: 320px;
  overflow-y: auto;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  margin-bottom: 16px;
}

.empty-list {
  text-align: center;
  padding: 24px;
  color: var(--text-muted);
  font-size: 13px;
}

.problem-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--border);
}

.problem-row:last-child {
  border-bottom: none;
}

.problem-row .problem-id {
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  color: var(--text-muted);
  min-width: 30px;
}

.problem-row .problem-title {
  flex: 1;
  font-size: 14px;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.difficulty-badge {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 4px;
  font-weight: 600;
}

.difficulty-badge.easy { color: #10b981; background: rgba(16, 185, 129, 0.1); }
.difficulty-badge.medium { color: #f59e0b; background: rgba(245, 158, 11, 0.1); }
.difficulty-badge.hard { color: #ef4444; background: rgba(239, 68, 68, 0.1); }

.problem-order {
  font-size: 12px;
  color: var(--text-muted);
  min-width: 60px;
}

.btn-remove {
  font-size: 12px;
  color: var(--text-muted);
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
}

.btn-remove:hover {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}
</style>
