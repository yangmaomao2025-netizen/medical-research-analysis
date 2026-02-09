"""
论文写作服务
"""
from typing import List, Dict
import httpx
from app.core.config import settings

class WritingService:
    """论文写作辅助服务"""
    
    async def generate_outline(
        self,
        title: str,
        paper_type: str,  # research_article, review, case_report
        sections: List[str]
    ) -> Dict:
        """生成论文大纲"""
        prompt = f"""请为以下论文生成详细大纲：

标题：{title}
论文类型：{paper_type}
需要包含的章节：{', '.join(sections)}

请按照标准的医学论文结构，为每个章节生成：
1. 该章节的主题句
2. 3-5个要点（每个要点的关键内容提示）
3. 建议的字数分配
4. 需要引用的文献类型

输出格式：
# 论文大纲：{title}

## 1. 章节名
- **主题**：...
- **要点**：
  1. ...
  2. ...
- **建议字数**：XXX字
- **文献需求**：...
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
            "outline": result["choices"][0]["message"]["content"],
            "title": title,
            "paper_type": paper_type
        }
    
    async def polish_text(
        self,
        text: str,
        polish_type: str,  # grammar, clarity, academic, concise
        target_journal: str = None
    ) -> Dict:
        """润色文本"""
        polish_desc = {
            "grammar": "修正语法错误，改善句式结构",
            "clarity": "提高表达清晰度，使逻辑更连贯",
            "academic": "增强学术性，使用更专业的表达",
            "concise": "精简表达，去除冗余内容"
        }
        
        journal_hint = f"目标期刊：{target_journal}" if target_journal else ""
        
        prompt = f"""请对以下医学论文文本进行润色：

润色类型：{polish_desc.get(polish_type, polish_type)}
{journal_hint}

原文：
{text}

请提供：
1. 润色后的文本
2. 修改说明（列出主要修改点）
3. 改进建议

输出格式：
## 润色后文本
...

## 修改说明
- 修改1：...
- 修改2：...

## 改进建议
...
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
                timeout=120.0
            )
            result = response.json()
            
        return {
            "polished_text": result["choices"][0]["message"]["content"],
            "original_text": text,
            "polish_type": polish_type
        }
    
    async def suggest_references(
        self,
        topic: str,
        keywords: List[str],
        num_suggestions: int = 10
    ) -> List[Dict]:
        """推荐参考文献"""
        prompt = f"""请为主题"{topic}"推荐相关的经典文献和高影响力论文。

关键词：{', '.join(keywords)}
需要推荐：{num_suggestions}篇

对每篇文献请提供：
1. 标题
2. 作者
3. 期刊
4. 年份
5. 推荐理由（为什么这篇文献重要）

输出格式：
1. **标题**：...
   **作者**：...
   **期刊**：...
   **年份**：...
   **推荐理由**：...
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
            "suggestions": result["choices"][0]["message"]["content"],
            "topic": topic,
            "keywords": keywords
        }

writing_service = WritingService()
