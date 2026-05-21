<template>
  <div class="page">
    <UserNavbar />

    <div class="workspace">
      <!-- 左侧：题目详情 -->
      <div class="left-panel">
        <div class="panel-header">
          <router-link to="/" class="back-link">
            <svg viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/></svg>
          </router-link>
          <span class="problem-id">{{ problem?.id }}</span>
          <span :class="['difficulty-badge', problem?.difficulty]">
            {{ difficultyLabel(problem?.difficulty) }}
          </span>
        </div>

        <div class="panel-body" v-if="problem">
          <h1 class="problem-title">{{ problem.title }}</h1>

          <div class="tags" v-if="problem.tags?.length">
            <span v-for="tag in problem.tags" :key="tag" class="tag">{{ tag }}</span>
          </div>

          <div class="meta">
            <div class="meta-item">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 3.5a.5.5 0 0 0-1 0V8a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 7.71V3.5z"/><path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/></svg>
              <span>{{ problem.time_limit }}ms</span>
            </div>
            <div class="meta-item">
              <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2zm3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v4a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"/></svg>
              <span>{{ problem.memory_limit }}MB</span>
            </div>
          </div>

          <section class="section">
            <h3>题目描述</h3>
            <div class="content">{{ problem.description }}</div>
          </section>

          <section class="section">
            <h3>输入格式</h3>
            <div class="content">{{ problem.input_format }}</div>
          </section>

          <section class="section">
            <h3>输出格式</h3>
            <div class="content">{{ problem.output_format }}</div>
          </section>

          <section class="section">
            <h3>样例</h3>
            <div class="example-grid">
              <div class="example">
                <span class="example-label">输入</span>
                <pre class="code-block">{{ problem.sample_input }}</pre>
              </div>
              <div class="example">
                <span class="example-label">输出</span>
                <pre class="code-block">{{ problem.sample_output }}</pre>
              </div>
            </div>
          </section>

          <section class="section" v-if="problem.hint">
            <h3>提示</h3>
            <div class="content hint">{{ problem.hint }}</div>
          </section>
        </div>

        <div class="panel-body" v-else-if="loading">
          <div class="skeleton" style="width: 40%; height: 20px; margin-bottom: 16px"></div>
          <div class="skeleton" style="width: 100%; height: 14px; margin-bottom: 8px"></div>
          <div class="skeleton" style="width: 90%; height: 14px; margin-bottom: 8px"></div>
          <div class="skeleton" style="width: 80%; height: 14px"></div>
        </div>
      </div>

      <!-- 右侧：代码编辑区 -->
      <div class="right-panel">
        <div class="editor-header">
          <select v-model="language" class="lang-select">
            <option value="cpp">C++</option>
            <option value="c">C</option>
            <option value="java">Java</option>
            <option value="python">Python</option>
          </select>
          <button class="btn-submit" :disabled="submitting || judging" @click="handleSubmit">
            {{ judging ? '评测中...' : submitting ? '提交中...' : '提交代码' }}
          </button>
        </div>

        <textarea
          v-model="code"
          class="code-editor"
          spellcheck="false"
          :placeholder="`// 在此输入 ${language} 代码`"
        ></textarea>

        <!-- 提交结果面板 -->
        <div class="result-panel" v-if="submission">
          <div class="result-header">
            <span class="result-label">评测结果</span>
            <span :class="['result-status', submission.result || 'pending']">
              {{ statusLabel(submission) }}
            </span>
          </div>

          <div class="result-meta" v-if="submission.status === 'completed' && submission.result === 'passed'">
            <span>{{ submission.time_used }}ms</span>
            <span>{{ Math.round(submission.memory_used / 1024) }}MB</span>
          </div>

          <div class="test-cases" v-if="submission.test_case_details?.length">
            <div class="test-case" v-for="tc in submission.test_case_details" :key="tc.test_case_id">
              <span class="tc-label">测试点 {{ tc.test_case_id }}</span>
              <span :class="['tc-status', tc.status]">{{ testCaseStatusLabel(tc.status) }}</span>
              <span class="tc-meta">{{ tc.time_used_ms }}ms</span>
              <span class="tc-meta">{{ Math.round(tc.memory_used_kb / 1024) }}MB</span>
            </div>
          </div>

          <div class="polling" v-if="submission.status === 'pending'">
            <div class="polling-dots">
              <span></span>
              <span></span>
              <span></span>
            </div>
            <span class="polling-text">评测中</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import UserNavbar from '../../components/UserNavbar.vue'
import { problemApi } from '../../api/problem'
import { submissionApi } from '../../api/submission'

const route = useRoute()
const problemId = Number(route.params.id)

const problem = ref(null)
const loading = ref(true)
const language = ref('cpp')
const code = ref('')
const submitting = ref(false)
const judging = ref(false)
const submission = ref(null)
let pollTimer = null

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

function statusLabel(s) {
  if (s.status === 'pending') return '等待评测'
  if (s.status === 'completed') {
    if (s.result === 'passed') return '通过'
    if (s.result === 'attempted') return '未通过'
    return '已完成'
  }
  return s.status
}

function testCaseStatusLabel(status) {
  const map = {
    accepted: '通过',
    wrong_answer: '错误',
    time_limit: '超时',
    memory_limit: '超内存',
    runtime_error: '运行错误',
    compile_error: '编译错误',
    system_error: '系统错误',
  }
  return map[status] || status
}

async function loadProblem() {
  try {
    problem.value = await problemApi.getDetail(problemId)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleSubmit() {
  // 防止重复提交
  if (submitting.value || judging.value) return
  if (!code.value.trim()) return

  submitting.value = true
  judging.value = false
  submission.value = null

  try {
    const res = await submissionApi.submit({
      problem_id: problemId,
      language: language.value,
      code: code.value,
    })
    submission.value = res
    judging.value = true
    startPolling(res.id)
  } catch (e) {
    console.error(e)
    judging.value = false
  } finally {
    submitting.value = false
  }
}

function startPolling(submissionId) {
  stopPolling()
  pollTimer = setInterval(async () => {
    try {
      const res = await submissionApi.getDetail(submissionId)
      submission.value = res
      if (res.status !== 'pending') {
        stopPolling()
      }
    } catch (e) {
      stopPolling()
    }
  }, 1000)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  judging.value = false
}

onMounted(loadProblem)
onUnmounted(stopPolling)
</script>

<style scoped>
.page {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
  overflow: hidden;
}

.workspace {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.left-panel {
  width: 45%;
  min-width: 360px;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
  flex-shrink: 0;
}

.back-link {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  color: var(--text-muted);
  transition: all 0.15s;
}

.back-link:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.back-link svg {
  width: 16px;
  height: 16px;
}

.problem-id {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 600;
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
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

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.problem-title {
  font-size: 20px;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.4;
  letter-spacing: -0.3px;
}

.tags {
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

.meta {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding: 12px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--text-muted);
}

.meta-item svg {
  width: 14px;
  height: 14px;
}

.section {
  margin-bottom: 24px;
}

.section h3 {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 12px;
}

.content {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.7;
  white-space: pre-wrap;
}

.content.hint {
  padding: 12px 16px;
  background: var(--bg-tertiary);
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-secondary);
}

.example-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.example {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.example-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.code-block {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 12px;
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
  font-size: 13px;
  color: var(--text-primary);
  white-space: pre-wrap;
  line-height: 1.5;
}

.right-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.editor-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
}

.lang-select {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text-primary);
  font-size: 13px;
  font-weight: 500;
  padding: 6px 10px;
  outline: none;
  cursor: pointer;
}

.btn-submit {
  padding: 7px 16px;
  background: var(--text-primary);
  color: var(--bg-primary);
  font-weight: 600;
  font-size: 13px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: opacity 0.15s;
}

.btn-submit:hover:not(:disabled) {
  opacity: 0.9;
}

.btn-submit:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.code-editor {
  flex: 1;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  padding: 16px;
  border: none;
  outline: none;
  resize: none;
  tab-size: 4;
}

.code-editor::placeholder {
  color: var(--text-muted);
}

.result-panel {
  border-top: 1px solid var(--border);
  background: var(--bg-secondary);
  padding: 16px;
  flex-shrink: 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.result-label {
  font-size: 13px;
  color: var(--text-muted);
  font-weight: 500;
}

.result-status {
  font-size: 13px;
  font-weight: 600;
}

.result-status.passed { color: #10b981; }
.result-status.attempted { color: #ef4444; }
.result-status.pending { color: var(--text-muted); }

.result-meta {
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 12px;
}

.test-cases {
  border-top: 1px solid var(--border);
  padding-top: 12px;
}

.test-case {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 6px 0;
  font-size: 13px;
}

.tc-label {
  color: var(--text-muted);
  min-width: 60px;
}

.tc-status {
  font-weight: 600;
  min-width: 50px;
}

.tc-status.accepted { color: #10b981; }
.tc-status.wrong_answer { color: #ef4444; }
.tc-status.time_limit { color: #f59e0b; }
.tc-status.memory_limit { color: #f59e0b; }
.tc-status.runtime_error { color: #ef4444; }
.tc-status.compile_error { color: #ef4444; }
.tc-status.system_error { color: #ef4444; }

.tc-meta {
  color: var(--text-muted);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
  font-size: 12px;
}

.polling {
  display: flex;
  align-items: center;
  gap: 10px;
}

.polling-dots {
  display: flex;
  gap: 4px;
}

.polling-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent);
  animation: pulse 1.2s infinite;
}

.polling-dots span:nth-child(2) { animation-delay: 0.2s; }
.polling-dots span:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
  0%, 80%, 100% { opacity: 0.3; }
  40% { opacity: 1; }
}

.polling-text {
  font-size: 13px;
  color: var(--text-muted);
}

.skeleton {
  background: linear-gradient(90deg, var(--bg-tertiary) 25%, var(--bg-hover) 50%, var(--bg-tertiary) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 12px;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
