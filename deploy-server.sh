#!/bin/bash
# 医学科研平台 - 一键部署脚本
# 在服务器上执行: curl -fsSL [脚本URL] | bash

set -e

SERVER_IP=$(curl -s ifconfig.me 2>/dev/null || echo "your-server-ip")
INSTALL_DIR="/opt/medical-platform"

echo "========================================"
echo "  医学科研平台部署脚本"
echo "========================================"
echo ""

# 检查root权限
if [ "$EUID" -ne 0 ]; then 
    echo "请使用root权限运行: sudo bash deploy.sh"
    exit 1
fi

# 安装Docker
install_docker() {
    echo "[1/8] 检查并安装Docker..."
    if ! command -v docker &> /dev/null; then
        echo "正在安装Docker..."
        curl -fsSL https://get.docker.com | bash -s -- --mirror Aliyun
        systemctl enable docker
        systemctl start docker
        echo "Docker安装完成"
    else
        echo "Docker已安装: $(docker --version)"
    fi
}

# 安装Docker Compose
install_compose() {
    echo "[2/8] 检查并安装Docker Compose..."
    if ! command -v docker-compose &> /dev/null; then
        echo "正在安装Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.24.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        echo "Docker Compose安装完成"
    else
        echo "Docker Compose已安装: $(docker-compose --version)"
    fi
}

# 创建项目目录
setup_directory() {
    echo "[3/8] 创建项目目录..."
    mkdir -p $INSTALL_DIR
    cd $INSTALL_DIR
    echo "工作目录: $INSTALL_DIR"
}

# 下载项目代码
download_code() {
    echo "[4/8] 下载项目代码..."
    
    # 如果存在git，直接clone
    if command -v git &> /dev/null; then
        if [ -d ".git" ]; then
            git pull origin master
        else
            git clone https://github.com/yangmaomao2025-netizen/medical-research-analysis.git .
        fi
    else
        echo "未安装git，尝试安装..."
        apt-get update -qq && apt-get install -y -qq git
        git clone https://github.com/yangmaomao2025-netizen/medical-research-analysis.git .
    fi
}

# 配置环境变量
setup_env() {
    echo "[5/8] 配置环境变量..."
    
    cat > $INSTALL_DIR/medical-research-platform/backend/.env <> EOF
APP_NAME=Medical Research Platform
APP_VERSION=0.1.0
DEBUG=false

DATABASE_URL=postgresql://postgres:postgres@postgres:5432/medical_research
REDIS_URL=redis://redis:6379/0
RABBITMQ_URL=amqp://admin:admin@rabbitmq:5672/
ELASTICSEARCH_URL=http://elasticsearch:9200
MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_NAME=medical-research

SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

KIMI_API_KEY=sk-kimi-4cIO9Ps487BvzCHEyCAF7Ohc9wYmRduoPe6lKNkeTrNRXhnw2pxY4dgHqIIEjOT8
KIMI_API_BASE=https://api.kimi.com/coding/v1
KIMI_MODEL=kimi-for-coding

MAX_UPLOAD_SIZE=104857600
UPLOAD_CHUNK_SIZE=5242880
EOF

    echo "环境配置完成"
}

# 启动服务
start_services() {
    echo "[6/8] 启动Docker服务..."
    cd $INSTALL_DIR/medical-research-platform/deploy
    
    # 停止旧服务
    docker-compose down 2>/dev/null || true
    
    # 启动新服务
    docker-compose up -d
    
    echo "服务启动中，请等待..."
    sleep 15
}

# 初始化数据库
init_database() {
    echo "[7/8] 初始化数据库..."
    cd $INSTALL_DIR/medical-research-platform/deploy
    
    # 创建表
    docker-compose exec -T backend python -c "
from app.db.database import engine
from app.db.models import Base
Base.metadata.create_all(bind=engine)
print('数据库表创建完成')
" 2>/dev/null || echo "等待数据库就绪，稍后请手动执行初始化"
    
    # 创建管理员
    docker-compose exec -T backend python -c "
from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.services.auth import get_password_hash
import uuid

db = SessionLocal()
try:
    if not db.query(User).filter(User.username == 'admin').first():
        admin = User(
            id=uuid.uuid4(),
            username='admin',
            email='admin@medical-platform.com',
            hashed_password=get_password_hash('admin123'),
            real_name='系统管理员',
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        db.add(admin)
        db.commit()
        print('✓ 管理员账号创建成功')
    else:
        print('✓ 管理员账号已存在')
except Exception as e:
    print(f'创建管理员失败: {e}')
finally:
    db.close()
" 2>/dev/null || echo "稍后请手动创建管理员"
}

# 显示信息
show_info() {
    echo ""
    echo "========================================"
    echo "  🎉 部署完成！"
    echo "========================================"
    echo ""
    echo "📱 访问地址："
    echo "  • 前端界面:    http://${SERVER_IP}:3000"
    echo "  • API文档:     http://${SERVER_IP}:8000/docs"
    echo "  • 后端API:     http://${SERVER_IP}:8000"
    echo ""
    echo "🔧 管理工具："
    echo "  • RabbitMQ:    http://${SERVER_IP}:15672 (admin/admin)"
    echo "  • MinIO控制台: http://${SERVER_IP}:9001 (minioadmin/minioadmin)"
    echo ""
    echo "👤 默认账号："
    echo "  • 管理员: admin / admin123"
    echo ""
    echo "📋 常用命令："
    echo "  查看日志: cd $INSTALL_DIR/medical-research-platform/deploy && docker-compose logs -f"
    echo "  停止服务: cd $INSTALL_DIR/medical-research-platform/deploy && docker-compose down"
    echo "  重启服务: cd $INSTALL_DIR/medical-research-platform/deploy && docker-compose restart"
    echo ""
    echo "💡 提示："
    echo "  - 首次启动可能需要1-2分钟初始化"
    echo "  - 如果端口冲突，请修改 deploy/docker-compose.yml 中的端口映射"
    echo ""
    echo "========================================"
}

# 主流程
main() {
    install_docker
    install_compose
    setup_directory
    download_code
    setup_env
    start_services
    init_database
    show_info
}

main "$@"
