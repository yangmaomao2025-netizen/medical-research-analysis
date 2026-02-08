"""
应用配置
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "Medical Research Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # 数据库
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/medical_research"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    
    # Elasticsearch
    ELASTICSEARCH_URL: str = "http://localhost:9200"
    
    # MinIO
    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET_NAME: str = "medical-research"
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI配置
    KIMI_API_KEY: str = ""
    KIMI_API_BASE: str = "https://api.kimi.com/coding/v1"
    KIMI_MODEL: str = "kimi-for-coding"
    
    # 文件上传
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    UPLOAD_CHUNK_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        env_file = ".env"

settings = Settings()
