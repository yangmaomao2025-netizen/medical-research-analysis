# 医学科研管理平台

## 项目结构
```
medical-research-platform/
├── backend/                 # FastAPI后端
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库模型
│   │   ├── models/         # Pydantic模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── alembic/            # 数据库迁移
│   ├── tests/              # 测试
│   └── requirements.txt    # 依赖
├── frontend/               # Vue3前端
│   ├── src/
│   │   ├── api/            # API接口
│   │   ├── components/     # 组件
│   │   ├── views/          # 页面
│   │   ├── stores/         # Pinia状态
│   │   └── utils/          # 工具
│   └── package.json
├── deploy/                 # 部署配置
│   └── docker-compose.yml
└── docs/                   # 文档
```

## 技术栈
- **后端**: FastAPI + SQLAlchemy 2.0 + PostgreSQL
- **前端**: Vue3 + TypeScript + ElementPlus3
- **缓存**: Redis
- **消息队列**: RabbitMQ + Celery
- **搜索**: Elasticsearch
- **文件存储**: MinIO

## 启动方式
docker-compose up -d
