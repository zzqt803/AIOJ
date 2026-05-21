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

      <!-- AI 分析面板 -->
      <div class="ai-panel" :class="{ 'ai-panel-open': showAiPanel }">
        <button class="ai-toggle" @click="toggleAiPanel" :title="showAiPanel ? '收起 AI 分析' : '展开 AI 分析'">
          <svg viewBox="0 0 16 16" fill="currentColor">
            <path v-if="showAiPanel" fill-rule="evenodd" d="M4.646 1.646a.5.5 0 0 1 .708 0l6 6a.5.5 0 0 1 0 .708l-6 6a.5.5 0 0 1-.708-.708L10.293 8 4.646 2.354a.5.5 0 0 1 0-.708z"/>
            <path v-else fill-rule="evenodd" d="M11.354 1.646a.5.5 0 0 1 0 .708L5.707 8l5.647 5.646a.5.5 0 0 1-.708.708l-6-6a.5.5 0 0 1 0-.708l6-6a.5.5 0 0 1 .708 0z"/>
          </svg>
        </button>

        <div class="ai-content" v-if="showAiPanel">
          <div class="ai-header">
            <h3>AI 代码分析</h3>
            <button v-if="submission?.ai_analysis_status === 'completed'" class="btn-refresh" @click="refreshAiAnalysis">
              <svg viewBox="0 0 16 16" fill="currentColor"><path fill-rule="evenodd" d="M8 3a5 5 0 1 0 4.546 2.914.5.5 0 1 1 .908-.418A6 6 0 1 1 8 2v1z"/><path d="M8 4.466V.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384L8.41 4.658A.25.25 0 0 1 8 4.466z"/></svg>
            </button>
          </div>

          <!-- 未提交状态 -->
          <div v-if="!submission" class="ai-empty">
            <p>提交代码后，AI 将自动分析你的代码</p>
          </div>

          <!-- 等待分析 -->
          <div v-else-if="submission.ai_analysis_status === 'pending'" class="ai-empty">
            <div class="ai-loading">
              <div class="spinner"></div>
              <span>AI 正在分析中...</span>
            </div>
          </div>

          <!-- 分析中 -->
          <div v-else-if="submission.ai_analysis_status === 'analyzing'" class="ai-empty">
            <div class="ai-loading">
              <div class="spinner"></div>
              <span>AI 正在分析中...</span>
            </div>
          </div>

          <!-- 分析完成 -->
          <div v-else-if="submission.ai_analysis_status === 'completed' && aiAnalysis" class="ai-result">
            <!-- 评分 -->
            <div class="ai-score">
              <span class="score-value">{{ aiAnalysis.score }}</span>
              <span class="score-label">分</span>
            </div>

            <!-- 整体评价 -->
            <div class="ai-section">
              <h4>整体评价</h4>
              <p>{{ aiAnalysis.summary }}</p>
            </div>

            <!-- 复杂度分析 -->
            <div class="ai-complexity">
              <div class="complexity-item">
                <span class="complexity-label">时间复杂度</span>
                <span class="complexity-value">{{ aiAnalysis.time_complexity }}</span>
              </div>
              <div class="complexity-item">
                <span class="complexity-label">空间复杂度</span>
                <span class="complexity-value">{{ aiAnalysis.space_complexity }}</span>
              </div>
            </div>

            <!-- 问题列表 -->
            <div class="ai-section" v-if="aiAnalysis.issues?.length">
              <h4>问题</h4>
              <div class="ai-issues">
                <div class="issue-item" v-for="(issue, index) in aiAnalysis.issues" :key="index">
                  <span class="issue-line" v-if="issue.line">第 {{ issue.line }} 行</span>
                  <span class="issue-desc">{{ issue.description }}</span>
                </div>
              </div>
            </div>

            <!-- 改进建议 -->
            <div class="ai-section" v-if="aiAnalysis.suggestions?.length">
              <h4>改进建议</h4>
              <ul class="ai-suggestions">
                <li v-for="(suggestion, index) in aiAnalysis.suggestions" :key="index">
                  {{ suggestion }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
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
const showAiPanel = ref(false)
const aiAnalysis = ref(null)
let pollTimer = null
let aiPollTimer = null

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

function toggleAiPanel() {
  showAiPanel.value = !showAiPanel.value
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
  if (submitting.value || judging.value) return
  if (!code.value.trim()) return

  submitting.value = true
  judging.value = false
  submission.value = null
  aiAnalysis.value = null

  try {
    const res = await submissionApi.submit({
      problem_id: problemId,
      language: language.value,
      code: code.value,
    })
    submission.value = res
    judging.value = true
    showAiPanel.value = true
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
        // 开始轮询 AI 分析结果
        startAiPolling(submissionId)
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

function startAiPolling(submissionId) {
  stopAiPolling()
  aiPollTimer = setInterval(async () => {
    try {
      const res = await submissionApi.getAiAnalysis(submissionId)
      submission.value = {
        ...submission.value,
        ai_analysis_status: res.ai_analysis_status
      }
      if (res.ai_analysis_status === 'completed') {
        aiAnalysis.value = res.ai_analysis_result
        stopAiPolling()
      } else if (res.ai_analysis_status === 'pending') {
        // 继续等待
      }
    } catch (e) {
      stopAiPolling()
    }
  }, 2000)
}

function stopAiPolling() {
  if (aiPollTimer) {
    clearInterval(aiPollTimer)
    aiPollTimer = null
  }
}

function refreshAiAnalysis() {
  if (submission.value?.id) {
    startAiPolling(submission.value.id)
  }
}

onMounted(loadProblem)
onUnmounted(() => {
  stopPolling()
  stopAiPolling()
})
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
  width: 40%;
  min-width: 320px;
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

/* AI 面板 */
.ai-panel {
  width: 0;
  overflow: hidden;
  border-left: 1px solid var(--border);
  background: var(--bg-secondary);
  transition: width 0.3s ease-out;
  position: relative;
}

.ai-panel-open {
  width: 360px;
}

.ai-toggle {
  position: absolute;
  left: -28px;
  top: 50%;
  transform: translateY(-50%);
  width: 28px;
  height: 56px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-right: none;
  border-radius: 6px 0 0 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  transition: all 0.15s;
  z-index: 10;
}

.ai-toggle:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.ai-toggle svg {
  width: 14px;
  height: 14px;
}

.ai-content {
  height: 100%;
  overflow-y: auto;
  padding: 20px;
}

.ai-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.ai-header h3 {
  font-size: 16px;
  font-weight: 600;
}

.btn-refresh {
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

.btn-refresh:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
}

.btn-refresh svg {
  width: 14px;
  height: 14px;
}

.ai-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
}

.ai-empty p {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
}

.ai-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
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

.ai-loading span {
  font-size: 13px;
  color: var(--text-muted);
}

.ai-result {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.ai-score {
  display: flex;
  align-items: baseline;
  gap: 4px;
  padding: 16px;
  background: var(--bg-tertiary);
  border-radius: 8px;
  text-align: center;
}

.score-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
}

.score-label {
  font-size: 14px;
  color: var(--text-muted);
}

.ai-section h4 {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.ai-section p {
  font-size: 14px;
  color: var(--text-primary);
  line-height: 1.6;
}

.ai-complexity {
  display: flex;
  gap: 16px;
}

.complexity-item {
  flex: 1;
  padding: 12px;
  background: var(--bg-tertiary);
  border-radius: 6px;
}

.complexity-label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.complexity-value {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-primary);
  font-family: 'SF Mono', 'Monaco', 'Menlo', monospace;
}

.ai-issues {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.issue-item {
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: 6px;
  font-size: 13px;
}

.issue-line {
  display: inline-block;
  padding: 2px 6px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 600;
  margin-right: 8px;
}

.issue-desc {
  color: var(--text-primary);
}

.ai-suggestions {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.ai-suggestions li {
  padding: 10px 12px;
  background: var(--bg-tertiary);
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.5;
}

.ai-suggestions li::before {
  content: "•";
  color: var(--accent);
  margin-right: 8px;
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
