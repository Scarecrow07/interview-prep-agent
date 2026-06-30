"""面试问答模型 - Step 6 输出（20-30道题目，含来源追溯）"""

from pydantic import BaseModel, Field
from typing import Optional


class QuestionSourceReference(BaseModel):
    """问题来源追溯"""
    jd_requirement: Optional[str] = Field(
        description="来源JD的具体要求",
        default=None,
    )
    resume_section: Optional[str] = Field(
        description="来源简历的具体章节/项目",
        default=None,
    )
    gap_source: Optional[str] = Field(
        description="来自匹配度评估报告的短板项",
        default=None,
    )


class AnswerFramework(BaseModel):
    """回答框架"""
    intent: str = Field(description="考察意图：面试官想了解什么")
    structure: str = Field(description="回答结构：STAR-L / 对比分析 / 原理阐述")
    key_points: list[str] = Field(
        description="高分要点（必须体现的关键词、态度）",
        min_length=2, max_length=5,
    )
    pitfalls: list[str] = Field(
        description="需避开的雷区（减分回答）",
        default_factory=list,
    )
    sample_response: str = Field(description="可直接开口讲的示例语句")


class InterviewQuestion(BaseModel):
    """单个面试问题"""
    question_id: str = Field(description="问题ID，如tech_001, project_001")
    category: str = Field(
        description="问题分类: "
        "tech / project_deep_dive / system_design / behavioral / motivation / gap_response",
    )
    difficulty: str = Field(description="难度: easy / medium / hard")
    question_text: str = Field(description="问题内容")
    
    # 来源追溯
    source_reference: QuestionSourceReference = Field(
        description="问题来源追溯（防止编造）",
    )
    
    # 回答框架
    answer_framework: AnswerFramework = Field(
        description="回答框架与高分要点",
    )
    
    # 追问方向
    follow_up_hints: Optional[list[str]] = Field(
        description="可能的追问方向",
        default=None,
    )


class QuestionCategory(BaseModel):
    """问题分类"""
    name: str = Field(description="分类名称")
    description: str = Field(description="分类描述")
    questions: list[InterviewQuestion] = Field(
        description="该分类下的题目列表",
    )


class QuestionBank(BaseModel):
    """面试题库 - Step 6 输出（20-30道题目）"""
    total_questions: int = Field(
        description="题目总数（20-30道）",
        ge=20, le=30,
    )
    categories: list[QuestionCategory] = Field(
        description="题目分类列表",
        min_length=5, max_length=7,
    )
    
    # 核心优势植入
    highlight_injection: list[str] = Field(
        description="在回答中植入的核心优势（来自匹配度分析）",
    )
    
    # 准备重点
    focus_areas_advice: str = Field(
        description="面试准备重点领域建议",
    )
    
    # 约束说明
    constraint_note: str = Field(
        description="约束说明：所有项目相关问题必须来自简历",
        default="所有项目相关问题基于简历原文项目，技术问题覆盖JD核心技术栈，短板问题来自匹配度评估报告。",
    )