"""
文件上传服务
"""
import os
import uuid
from minio import Minio
from app.core.config import settings

class FileService:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=False
        )
        self.bucket = settings.MINIO_BUCKET_NAME
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """确保bucket存在"""
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)
    
    def upload_file(self, file_data: bytes, filename: str, content_type: str = "application/pdf") -> str:
        """上传文件到MinIO"""
        # 生成唯一文件名
        ext = os.path.splitext(filename)[1]
        object_name = f"literatures/{uuid.uuid4()}{ext}"
        
        # 上传
        from io import BytesIO
        self.client.put_object(
            self.bucket,
            object_name,
            BytesIO(file_data),
            length=len(file_data),
            content_type=content_type
        )
        
        return object_name
    
    def get_file_url(self, object_name: str, expires: int = 3600) -> str:
        """获取文件临时访问URL"""
        return self.client.presigned_get_object(self.bucket, object_name, expires)
    
    def delete_file(self, object_name: str):
        """删除文件"""
        self.client.remove_object(self.bucket, object_name)

file_service = FileService()
