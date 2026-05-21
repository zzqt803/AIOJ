<template>
  <div class="page">
    <Navbar />

    <div class="workspace">
      <!-- 左侧：题目详情 -->
      <div class="left-panel">
        <div class="panel-header">
          <span class="problem-id">#{{ problem?.id }}</span>
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
            <span>时间限制：{{ problem.time_limit }}ms</span>
            <span>内存限制：{{ problem.memory_limit }}MB</span>
          </div>

          <section class="section">
            <h3>题目描述</h3>
            <p>{{ problem.description }}</p>
          </section>

          <section class="section">
            <h3>输入格式</h3>
            <p>{{ problem.input_format }}</p>
          </section>

          <section class="section">
            <h3>输出格式</h3>
            <p>{{ problem.output_format }}</p>
          </section>

          <section class="section">
            <h3>样例输入</h3>
            <pre class="code-block">{{ problem.sample_input }}</pre>
          </section>

          <section class="section">
            <h3>样例输出</h3>
            <pre class="code-block">{{ problem.sample_output }}</pre>
          </section>
        </div>

        <!-- 骨架屏 -->
        <div class="panel-body" v-else-if="problemLoading">
          <div class="skeleton" style="width: 60%; height: 24px; margin-bottom: 16px"></div>
          <div class="skeleton" style="width: 100%; height: 14px; margin-bottom: 8px"></div>
          <div class="skeleton" style="width: 90%; height: 14px; margin-bottom: 8px"></div>
          <div class="skeleton" style="width: 80%; height: 14px"></div>
        </div>
      </div>

      <!-- 右侧：代码编辑区 -->
      <div class="right-panel">
        <!-- 编辑器顶栏 -->
        <div class="editor-header">
          <select v-model="language" class="lang-select">
            <option value="cpp">C++</option>
            <option value="python">Python</option>
            <option value="java">Java</option>
          </select>
          <button class="btn-submit" :disabled="submitting" @click="handleSubmit">
            {{ submitting ? '提交中...' : '提交代码' }}
          </button>
        </div>

        <!-- 代码编辑器 -->
        <textarea
          v-model="code"
          class="code-editor"
          spellcheck="false"
          :placeholder="`// 在此输入 ${language} 代码`"
        ></textarea>

        <!-- 提交结果面板 -->
        <div class="result-panel" v-if="submission">
          <div class="result-header">
            <span class="result-label">提交结果</span>
            <span :class="['result-status', submission.result || 'pending']">
              {{ statusLabel(submission) }}
            </span>
          </div>

          <div class="result-meta" v-if="submission.status === 'completed' && submission.result === 'passed'">
            <span>耗时：{{ submission.time_used }}ms</span>
            <span>内存：{{ Math.round(submission.memory_used / 1024) }}MB</span>
          </div>

          <!-- 测试点详情 -->
          <div class="test-cases" v-if="submission.test_case_details?.length">
            <div class="test-case" v-for="tc in submission.test_case_details" :key="tc.test_case_id">
              <span class="tc-id">#{{ tc.test_case_id }}</span>
              <span :class="['tc-status', tc.status]">{{ testCaseStatusLabel(tc.status) }}</span>
              <span class="tc-time">{{ tc.time_used_ms }}ms</span>
              <span class="tc-memory">{{ Math.round(tc.memory_used_kb / 1024) }}MB</span>
            </div>
          </div>

          <!-- 轮询中的加载动画 -->
          <div class="polling" v-if="submission.status === 'pending'">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="polling-text">判题中...</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '../components/Navbar.vue'
import { problemApi } from '../api/problem'
import { submissionApi } from '../api/submission'

const route = useRoute()
const problemId = Number(route.params.id)

const problem = ref(null)
const problemLoading = ref(true)

const language = ref('cpp')
const code = ref('')
const submitting = ref(false)
const submission = ref(null)

let pollTimer = null

function difficultyLabel(d) {
  return { easy: '简单', medium: '中等', hard: '困难' }[d] || d
}

function statusLabel(s) {
  if (s.status === 'pending') return '等待判题'
  if (s.status === 'completed') {
    if (s.result === 'passed') return '已通过'
    if (s.result === 'attempted') return '尝试过'
    return '已完成'
  }
  return s.status
}

function testCaseStatusLabel(status) {
  const map = {
    accepted: '通过',
    wrong_answer: '答案错误',
    time_limit: '超时',
    memory_limit: '内存超限',
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
    problemLoading.value = false
  }
}

async function handleSubmit() {
  if (!code.value.trim()) return
  submitting.value = true
  submission.value = null

  try {
    const res = await submissionApi.submit({
      problem_id: problemId,
      language: language.value,
      code: code.value,
    })
    submission.value = res
    startPolling(res.id)
  } catch (e) {
    console.error(e)
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

/* 左侧面板 */
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
  padding: 12px 20px;
  border-bottom: 1px solid var(--border);
  background: var(--bg-secondary);
  flex-shrink: 0;
}

.problem-id {
  font-size: 13px;
  color: var(--text-muted);
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

.panel-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px 20px;
}

.problem-title {
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 14px;
  line-height: 1.4;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 14px;
}

.tag {
  font-size: 12px;
  padding: 3px 8px;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  border-radius: 4px;
}

.meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 24px;
  padding: 10px 0;
  border-top: 1px solid var(--border);
  border-bottom: 1px solid var(--border);
}

.section {
  margin-bottom: 22px;
}

.section h3 {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 10px;
}

.section p {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.7;
  white-space: pre-wrap;
}

.code-block {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 13px;
  color: var(--text-primary);
  white-space: pre-wrap;
  line-height: 1.6;
}

/* 右侧面板 */
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
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 13px;
  padding: 6px 10px;
  outline: none;
  cursor: pointer;
}

.btn-submit {
  padding: 7px 20px;
  background: var(--accent);
  color: #1a1a1a;
  font-weight: 600;
  font-size: 13px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.2s;
}

.btn-submit:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.code-editor {
  flex: 1;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
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

/* 结果面板 */
.result-panel {
  border-top: 1px solid var(--border);
  background: var(--bg-secondary);
  padding: 14px 16px;
  flex-shrink: 0;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.result-label {
  font-size: 13px;
  color: var(--text-secondary);
}

.result-status {
  font-size: 14px;
  font-weight: 600;
}

.result-status.passed { color: var(--green); }
.result-status.attempted { color: var(--red); }
.result-status.pending { color: var(--text-muted); }

/* 测试点详情 */
.test-cases {
  margin-top: 12px;
  border-top: 1px solid var(--border);
  padding-top: 10px;
}

.test-case {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
  font-size: 12px;
}

.tc-id {
  color: var(--text-muted);
  min-width: 30px;
}

.tc-status {
  font-weight: 500;
  min-width: 60px;
}

.tc-status.accepted { color: var(--green); }
.tc-status.wrong_answer { color: var(--red); }
.tc-status.time_limit { color: var(--yellow); }
.tc-status.memory_limit { color: var(--yellow); }
.tc-status.runtime_error { color: var(--red); }
.tc-status.compile_error { color: var(--red); }
.tc-status.system_error { color: var(--red); }

.tc-time, .tc-memory {
  color: var(--text-muted);
  min-width: 60px;
}

.result-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--text-muted);
}

/* 轮询动画 */
.polling {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
  animation: bounce 1.2s infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

.polling-text {
  font-size: 13px;
  color: var(--text-muted);
  margin-left: 6px;
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}

/* Skeleton */
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