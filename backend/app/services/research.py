"""
研究方案服务
"""
from typing import List, Dict
import httpx
from app.core.config import settings

class ResearchService:
    """科研辅助服务"""
    
    async def generate_protocol(
        self,
        title: str,
        study_type: str,
        disease: str,
        objectives: str
    ) -> Dict:
        """生成研究方案"""
        prompt = f"""请为以下医学研究生成详细的研究方案：

题目：{title}
研究类型：{study_type}
疾病/领域：{disease}
研究目的：{objectives}

请包含以下内容：
1. 研究背景与意义
2. 研究目标（主要终点、次要终点）
3. 研究设计（类型、分组、盲法）
4. 纳入/排除标准
5. 样本量计算依据
6. 干预措施/观察指标
7. 统计分析方法
8. 伦理考虑
9. 预期结果与局限性
10. 研究时间计划表
"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.KIMI_API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {settings.KIMI_API_KEY}"},
                json={
                    "model": settings.KIMI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=120.0
            )
            result = response.json()
            
        return {
            "protocol": result["choices"][0]["message"]["content"],
            "title": title,
            "study_type": study_type
        }
    
    async def design_experiment(
        self,
        research_question: str,
        available_resources: List[str]
    ) -> Dict:
        """设计实验"""
        prompt = f"""请为以下研究问题设计实验方案：

研究问题：{research_question}
可用资源：{', '.join(available_resources)}

请提供：
1. 实验设计类型（随机对照、队列研究等）
2. 实验组和对照组设置
3. 主要观察指标
4. 实验流程图
5. 数据收集方法
6. 质量控制措施
7. 可能的风险与应对
"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.KIMI_API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {settings.KIMI_API_KEY}"},
                json={
                    "model": settings.KIMI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                },
                timeout=120.0
            )
            result = response.json()
            
        return {
            "design": result["choices"][0]["message"]["content"]
        }
    
    async def statistical_analysis_plan(
        self,
        data_type: str,
        groups: int,
        primary_endpoint: str
    ) -> Dict:
        """统计分析方案"""
        prompt = f"""请为以下数据设计统计分析方案：

数据类型：{data_type}
分组数量：{groups}
主要终点：{primary_endpoint}

请提供：
1. 数据描述统计方法
2. 组间比较方法选择（t检验/方差分析/非参数检验等）
3. 多因素分析方法
4. 缺失值处理策略
5. 统计软件建议
6. 结果报告格式
"""
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.KIMI_API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {settings.KIMI_API_KEY}"},
                json={
                    "model": settings.KIMI_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.5
                },
                timeout=60.0
            )
            result = response.json()
            
        return {
            "analysis_plan": result["choices"][0]["message"]["content"]
        }

research_service = ResearchService()
