# AIOJ - AI Online Judge

一个拥有 AI 代码分析功能的在线判题平台。

## 项目结构

```
AIOJ/
├── AIOJ-backend/      # Python 后端 (FastAPI)
├── AIOJ-frontend/     # Vue 3 前端
├── AIOJ-judge/        # C++ 判题进程
├── docker-compose.yml # Docker 编排
├── 建表语句.sql        # 数据库初始化
└── init-admin.sql     # 管理员账号初始化
```

## 技术栈

| 模块 | 技术 |
|------|------|
| 后端 | Python 3.11, FastAPI, SQLAlchemy, Gunicorn |
| 前端 | Vue 3, Pinia, Axios |
| 判题 | C++17, isolate 沙箱, Redis 消息队列 |
| 数据库 | MySQL 8.0, Redis 7 |
| 部署 | Docker, Docker Compose, Nginx |

## 功能特性

### 用户端
- 题库浏览（难度、标签筛选、分页）
- 代码提交和实时评测（C/C++/Java/Python）
- AI 代码分析（复杂度、问题、改进建议）
- 提交记录查看
- 题单练习
- 排行榜
- 题目收藏
- 讨论区

### 管理端
- 仪表盘（用户/题目/提交/题单统计）
- 题目管理（CRUD、测试数据）
- 题单管理（创建、添加/移除题目）
- 用户管理（查看详情、提交记录、统计数据）

## Docker 部署

### 前置条件

- Docker 20.10+
- Docker Compose 2.0+

### 1. 克隆项目

```bash
git clone https://github.com/zzqt803/AIOJ.git
cd AIOJ
```

### 2. 配置环境变量

创建 `.env` 文件：

```bash
cat > .env << 'EOF'
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_PASSWORD=your_db_password
SECRET_KEY=your_jwt_secret_key
AI_API_KEY=your_ai_api_key
AI_MODEL=mimo-v2.5
AI_BASE_URL=https://api.xiaomimimo.com/anthropic
EOF
```

各变量说明：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MYSQL_ROOT_PASSWORD` | MySQL root 密码 | root123456 |
| `MYSQL_PASSWORD` | 应用数据库密码 | aioj123456 |
| `SECRET_KEY` | JWT 签名密钥 | 内置默认值 |
| `AI_API_KEY` | AI 分析 API Key | 无（必填） |
| `AI_MODEL` | AI 模型名称 | mimo-v2.5 |
| `AI_BASE_URL` | AI API 地址 | https://api.xiaomimimo.com/anthropic |

### 3. 启动服务

```bash
docker compose up -d
```

首次启动会自动：
- 构建后端、前端、判题三个镜像
- 初始化数据库（建表、创建管理员账号）

启动后包含 5 个容器：

| 容器 | 端口 | 说明 |
|------|------|------|
| aioj-frontend | 80 | Nginx + Vue 前端 |
| aioj-backend | 8000 | FastAPI 后端 |
| aioj-judge | - | C++ 判题进程 |
| aioj-mysql | 3306 | MySQL 数据库 |
| aioj-redis | 6379 | Redis 缓存 |

### 4. 访问

浏览器打开 `http://你的服务器IP`

默认管理员账号：`admin@aioj.com` / `admin123`

### 常用命令

```bash
# 查看容器状态
docker compose ps

# 查看日志
docker compose logs -f backend
docker compose logs -f judge

# 重启某个服务
docker compose restart backend

# 重新构建并启动（代码更新后）
docker compose up -d --build

# 停止所有服务
docker compose down

# 停止并删除数据卷（会清空数据库）
docker compose down -v
```

## 本地开发

如果不使用 Docker，也可以本地开发：

### 后端

```bash
cd AIOJ-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # 配置数据库等连接信息
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端

```bash
cd AIOJ-frontend
npm install
npm run dev
```

### 判题进程

```bash
cd AIOJ-judge
mkdir build && cd build
cmake .. && make
./aioj-judge ../judge.conf
```

## API 文档

后端启动后访问 `http://localhost:8000/docs` 查看 Swagger 文档。

## 许可证

MIT License
