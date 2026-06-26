from pydantic import BaseModel, Field
from typing import Optional


class SkillMatchItem(BaseModel):
    """单项技能匹配结果"""
    skill_name: str
    skill_type: str = Field(description="类型: tech / soft / domain")
    requirement_level: str = Field(description="JD 要求等级")
    candidate_level: Optional[str] = Field(
        description="候选人当前水平(从简历推断), None=未提及",
        default=None,
    )
    match_status: str = Field(
        description="匹配状态: matched / partial / gap / not_mentioned",
    )
    evidence_from_resume: Optional[str] = Field(
        description="简历中的证据原文",
        default=None,
    )
    gap_description: Optional[str] = Field(
        description="差距描述(如果存在差距)",
        default=None,
    )
    priority: int = Field(
        description="弥补优先级: 1=高优先, 2=中, 3=低",
        ge=1, le=3,
    )


class ResumeSummary(BaseModel):
    """简历摘要"""
    years_of_experience: int = Field(ge=0)
    current_role: Optional[str] = None
    education_background: Optional[str] = None
    notable_projects: list[str] = Field(
        description="突出项目经历(最多5个)",
        max_length=5,
    )


class GapAnalysis(BaseModel):
    """差距分析结果"""
    resume_summary: ResumeSummary
    overall_match_score: int = Field(
        description="总体匹配度(0-100)", ge=0, le=100,
    )
    skill_match_details: list[SkillMatchItem]
    strengths: list[str] = Field(
        description="候选人的核心优势(3-5条)",
    )
    top_gaps: list[str] = Field(
        description="最需要弥补的Top差距(3-5条)",
    )
    risk_areas: list[str] = Field(
        description="面试中可能被问倒的高风险领域",
    )
    preparation_strategy: str = Field(
        description=(
            "面试准备策略建议(基于差距分析的个性化建议, 150-200字)"
        ),
    )