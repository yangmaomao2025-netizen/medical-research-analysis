"""
AI服务 - 集成Kimi API
"""
import httpx
from app.core.config import settings

class AIService:
    def __init__(self):
        self.api_key = settings.KIMI_API_KEY
        self.base_url = settings.KIMI_API_BASE
        self.model = settings.KIMI_MODEL
    
    async def chat(self, messages: list, temperature: float = 0.7) -> str:
        """通用对话"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature
                },
                timeout=60.0
            )
            result = response.json()
            return result["choices"][0]["message"]["content"]
    
    async def summarize_paper(self, title: str, abstract: str) -> dict:
        """总结论文"""
        prompt = f"""请对以下医学论文进行结构化总结：

标题：{title}
摘要：{abstract}

请按以下格式输出：
1. 研究背景
2. 研究目的
3. 方法学
4. 核心结果
5. 讨论要点
6. 结论与局限
7. 创新点（技术创新、样本量优势、新机制发现、临床意义等）
"""
        
        messages = [{"role": "user", "content": prompt}]
        content = await self.chat(messages)
        
        return {
            "summary": content,
            "sections": self._parse_summary(content)
        }
    
    async def translate_text(self, text: str, target_lang: str = "zh") -> str:
        """翻译文本"""
        direction = "英译中" if target_lang == "zh" else "中译英"
        prompt = f"请将以下医学文本{direction}，保持专业术语准确：\n\n{text}"
        
        messages = [{"role": "user", "content": prompt}]
        return await self.chat(messages)
    
    async def suggest_research_topic(self, research_area: str) -> list:
        """智能选题建议"""
        prompt = f"""作为医学研究专家，请针对"{research_area}"领域，推荐5个有创新性和临床价值的研究选题。

每个选题请包含：
1. 题目
2. 研究意义
3. 创新点
4. 可行性评估
"""
        
        messages = [{"role": "user", "content": prompt}]
        content = await self.chat(messages)
        
        return self._parse_topics(content)
    
    def _parse_summary(self, content: str) -> dict:
        """解析总结内容"""
        # TODO: 解析结构化输出
        return {"raw": content}
    
    def _parse_topics(self, content: str) -> list:
        """解析选题建议"""
        # TODO: 解析选题列表
        return [{"title": content, "description": ""}]

ai_service = AIService()
