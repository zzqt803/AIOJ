# AIOJ - AI Online Judge

一个拥有 AI 服务的在线判题平台。

## 项目结构

```
AIOJ/
├── AIOJ-backend/      # Python 后端 (FastAPI)
├── AIOJ-frontend/     # Vue 3 前端
└── AIOJ-judge/        # C++ 判题进程
```

## 技术栈

### 后端
- Python 3.10+
- FastAPI
- SQLAlchemy (MySQL)
- Redis

### 前端
- Vue 3
- Pinia
- Vue Router
- Axios

### 判题进程
- C++17
- CMake
- hiredis
- nlohmann/json
- isolate (沙箱)

## 快速开始

### 1. 环境准备

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+
- GCC/G++ (支持 C++17)
- isolate (判题沙箱)

### 2. 数据库配置

创建数据库并导入表结构：

```sql
CREATE DATABASE aioj DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE aioj;
-- 执行建表语句
```

### 3. 后端启动

```bash
cd AIOJ-backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env  # 编辑 .env 文件

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 前端启动

```bash
cd AIOJ-frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

访问 http://localhost:5173

### 5. 判题进程

```bash
cd AIOJ-judge

# 安装依赖 (vcpkg)
vcpkg install hiredis nlohmann-json

# 编译
mkdir build && cd build
cmake ..
make

# 运行
./aioj-judge ../config/judge.conf
```

## 功能特性

### 用户端
- 题库浏览（支持难度、标签筛选）
- 题目详情查看
- 代码提交和实时评测
- 提交记录查看
- 题单功能
- 排行榜
- 题目收藏

### 管理端
- 题目管理（CRUD）
- 题单管理
- 用户管理（查看详情、提交记录）

### 判题系统
- 支持 C/C++ 语言
- 使用 isolate 沙箱安全执行
- 多线程并发判题
- Redis 消息队列通信

## 配置说明

### 后端配置 (.env)

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/aioj
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALGORITHM=HS256
HOST=0.0.0.0
PORT=8000
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
TASK_QUEUE=judge_task
RESULT_QUEUE=judge_result
```

### 判题进程配置 (config/judge.conf)

```ini
redis_host=localhost
redis_port=6379
redis_db=0
task_queue=judge_task
result_queue=judge_result
thread_count=4
default_time_limit_ms=2000
default_memory_limit_kb=262144
testcase_root=../testcases
log_level=INFO
```

## 目录结构

```
AIOJ-backend/
├── app/
│   ├── core/          # 配置、安全、依赖注入
│   ├── db/            # 数据库和 Redis 连接
│   ├── models/        # SQLAlchemy 模型
│   ├── routers/       # API 路由
│   ├── schemas/       # Pydantic 模式
│   └── services/      # 业务逻辑
├── .env               # 环境变量
└── requirements.txt   # Python 依赖

AIOJ-frontend/
├── src/
│   ├── api/           # API 调用
│   ├── components/    # 组件
│   ├── router/        # 路由配置
│   ├── store/         # Pinia 状态管理
│   └── views/         # 页面视图
├── index.html
└── package.json

AIOJ-judge/
├── config/            # 配置文件
├── include/           # 头文件
├── src/               # 源代码
├── testcases/         # 测试用例
└── CMakeLists.txt
```

## API 文档

启动后端后访问 http://localhost:8000/docs 查看 Swagger API 文档。

## 许可证

MIT License
