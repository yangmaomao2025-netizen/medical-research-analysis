"""
Elasticsearch服务
"""
from elasticsearch import Elasticsearch
from app.core.config import settings

class ElasticService:
    def __init__(self):
        self.client = Elasticsearch([settings.ELASTICSEARCH_URL])
    
    def create_index(self):
        """创建文献索引"""
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "ik_max_word"},
                    "abstract": {"type": "text", "analyzer": "ik_max_word"},
                    "keywords": {"type": "keyword"},
                    "diseases": {"type": "keyword"},
                    "authors": {"type": "keyword"},
                    "journal": {"type": "keyword"},
                    "year": {"type": "integer"},
                    "impact_factor": {"type": "float"},
                    "content": {"type": "text", "analyzer": "ik_max_word"}
                }
            }
        }
        
        if not self.client.indices.exists(index="literatures"):
            self.client.indices.create(index="literatures", body=mapping)
    
    def index_literature(self, literature_id: str, data: dict):
        """索引文献"""
        self.client.index(index="literatures", id=literature_id, body=data)
    
    def search(
        self,
        query: str = None,
        filters: dict = None,
        page: int = 1,
        page_size: int = 20
    ):
        """全文搜索"""
        must = []
        
        if query:
            must.append({
                "multi_match": {
                    "query": query,
                    "fields": ["title^3", "abstract^2", "keywords", "content"]
                }
            })
        
        # 过滤器
        filter_list = []
        if filters:
            if "year_from" in filters:
                filter_list.append({"range": {"year": {"gte": filters["year_from"]}}})
            if "year_to" in filters:
                filter_list.append({"range": {"year": {"lte": filters["year_to"]}}})
            if "is_sci" in filters:
                filter_list.append({"term": {"is_sci": filters["is_sci"]}})
        
        body = {
            "query": {
                "bool": {
                    "must": must,
                    "filter": filter_list
                }
            },
            "from": (page - 1) * page_size,
            "size": page_size,
            "highlight": {
                "fields": {
                    "title": {},
                    "abstract": {}
                }
            }
        }
        
        result = self.client.search(index="literatures", body=body)
        return result["hits"]["hits"], result["hits"]["total"]["value"]

es_service = ElasticService()
