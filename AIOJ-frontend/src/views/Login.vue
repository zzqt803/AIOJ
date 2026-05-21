<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Logo -->
      <div class="logo">
        <span class="logo-bracket">{</span>
        <span class="logo-text">OJ</span>
        <span class="logo-bracket">}</span>
      </div>
      <p class="subtitle">在线评测平台</p>

      <!-- Tab 切换 -->
      <div class="tabs">
        <button :class="['tab', { active: mode === 'login' }]" @click="mode = 'login'">登录</button>
        <button :class="['tab', { active: mode === 'register' }]" @click="mode = 'register'">注册</button>
      </div>

      <!-- 登录表单 -->
      <form v-if="mode === 'login'" class="form" @submit.prevent="handleLogin">
        <div class="field">
          <label>邮箱</label>
          <input v-model="loginForm.email" type="email" placeholder="请输入邮箱" required />
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="loginForm.password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>

      <!-- 注册表单 -->
      <form v-else class="form" @submit.prevent="handleRegister">
        <div class="field">
          <label>用户名</label>
          <input v-model="registerForm.username" type="text" placeholder="3-20位字母、数字或下划线" required />
        </div>
        <div class="field">
          <label>邮箱</label>
          <input v-model="registerForm.email" type="email" placeholder="请输入邮箱" required />
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="registerForm.password" type="password" placeholder="至少8位" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'

const router = useRouter()
const auth = useAuthStore()

const mode = ref('login')
const loading = ref(false)
const error = ref('')

const loginForm = ref({ email: '', password: '' })
const registerForm = ref({ username: '', email: '', password: '' })

// 切换模式时清空错误
watch(mode, () => { error.value = '' })

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await auth.login(loginForm.value.email, loginForm.value.password)
    // 根据角色跳转
    if (auth.isAdmin) {
      router.push('/admin')
    } else {
      router.push('/')
    }
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败，请检查邮箱和密码'
  } finally {
    loading.value = false
  }
}

async function handleRegister() {
  loading.value = true
  error.value = ''
  try {
    await auth.register(registerForm.value.username, registerForm.value.email, registerForm.value.password)
    mode.value = 'login'
    error.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || '注册失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-primary);
  background-image: radial-gradient(ellipse at 20% 50%, rgba(255, 161, 22, 0.04) 0%, transparent 60%),
                    radial-gradient(ellipse at 80% 20%, rgba(0, 184, 163, 0.04) 0%, transparent 60%);
}

.login-card {
  width: 380px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 40px 36px;
}

.logo {
  text-align: center;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -1px;
  margin-bottom: 8px;
}

.logo-bracket {
  color: var(--accent);
}

.logo-text {
  color: var(--text-primary);
  margin: 0 4px;
}

.subtitle {
  text-align: center;
  color: var(--text-muted);
  font-size: 13px;
  margin-bottom: 28px;
}

.tabs {
  display: flex;
  border-bottom: 1px solid var(--border);
  margin-bottom: 24px;
}

.tab {
  flex: 1;
  padding: 10px;
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: all 0.2s;
}

.tab.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.tab:hover:not(.active) {
  color: var(--text-primary);
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field label {
  font-size: 13px;
  color: var(--text-secondary);
}

.field input {
  background: var(--bg-tertiary);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  color: var(--text-primary);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.field input:focus {
  border-color: var(--accent);
}

.field input::placeholder {
  color: var(--text-muted);
}

.error {
  color: var(--red);
  font-size: 13px;
  padding: 8px 12px;
  background: rgba(239, 71, 67, 0.1);
  border-radius: var(--radius-sm);
  border: 1px solid rgba(239, 71, 67, 0.2);
}

.btn-submit {
  width: 100%;
  padding: 11px;
  background: var(--accent);
  color: #1a1a1a;
  font-weight: 600;
  font-size: 14px;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.2s;
  margin-top: 4px;
}

.btn-submit:hover:not(:disabled) {
  background: var(--accent-hover);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>