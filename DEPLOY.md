# 医学科研管理平台 - 部署指南

## 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 内存：8GB+
- 磁盘：50GB+

## 快速启动

### 1. 克隆代码
```bash
git clone https://github.com/yangmaomao2025-netizen/medical-research-analysis.git
cd medical-research-analysis/medical-research-platform
```

### 2. 配置环境变量
```bash
cp backend/.env.example backend/.env
# 编辑 .env 文件，配置数据库、Redis、Kimi API等
```

### 3. 启动服务
```bash
cd deploy
docker-compose up -d
```

### 4. 初始化数据库
```bash
docker-compose exec backend alembic upgrade head
```

### 5. 访问系统
- 前端：http://localhost:3000
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| Frontend | 3000 | Vue3前端 |
| Backend | 8000 | FastAPI后端 |
| PostgreSQL | 5432 | 数据库 |
| Redis | 6379 | 缓存 |
| RabbitMQ | 5672 | 消息队列 |
| RabbitMQ管理 | 15672 | 管理界面 |
| Elasticsearch | 9200 | 搜索引擎 |
| MinIO | 9000 | 文件存储 |
| MinIO控制台 | 9001 | 管理界面 |

## 默认账号

- 系统管理员：admin/admin123
- 普通用户：注册即可

## 功能清单

### ✅ 已实现功能

- [x] 用户注册/登录/认证
- [x] 个人信息管理
- [x] 文献上传/检索/管理
- [x] PDF在线预览
- [x] 项目管理与跟踪
- [x] AI文献总结
- [x] AI翻译
- [x] 智能选题
- [x] 研究方案生成
- [x] 实验设计
- [x] 统计分析方案
- [x] 论文大纲生成
- [x] 文本润色
- [x] 参考文献推荐

### 🚧 待开发功能

- [ ] 文献批量导入
- [ ] 全文检索
- [ ] 数据可视化
- [ ] 团队协作
- [ ] 消息通知
- [ ] 系统监控

## 技术栈

- **前端**: Vue3 + TypeScript + ElementPlus3
- **后端**: FastAPI + SQLAlchemy 2.0
- **数据库**: PostgreSQL 15
- **缓存**: Redis 7
- **搜索**: Elasticsearch 8
- **消息队列**: RabbitMQ + Celery
- **文件存储**: MinIO
- **AI**: Kimi API

## 目录结构

```
medical-research-platform/
├── backend/          # FastAPI后端
├── frontend/         # Vue3前端
├── deploy/           # Docker部署配置
└── docs/             # 文档
```

## 开发团队

宁唐KIMI牛马 - AI开发助手
