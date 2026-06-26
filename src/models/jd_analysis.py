from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class TechnologyRequirement(BaseModel):
    """单个技术需求"""
    tech_name: str = Field(description="技术名称，如 Python, Kubernetes, React")
    proficiency_level: str = Field(description="要求熟练度: 了解/熟悉/精通/专家")
    is_required: bool = Field(description="是否为必须项(true=硬性要求, false=加分项)")
    reason_from_jd: str = Field(description="从JD原文中引用的依据")


class ExperienceRequirement(BaseModel):
    """经验要求"""
    min_years: int = Field(description="最低工作年限要求,0表示无要求", ge=0)
    preferred_industry: list[str] = Field(
        description="偏好的行业背景,如['互联网','金融']",
        default_factory=list,
    )
    preferred_role: Optional[str] = Field(
        description="偏好岗位类型,如'架构师'、'高级开发'",
        default=None,
    )


class SoftSkillRequirement(BaseModel):
    """软技能要求"""
    skill_name: str = Field(description="软技能名称，如沟通能力、团队协作")
    context: str = Field(description="在JD中的上下文说明")


class JDAnalysis(BaseModel):
    """JD分析结果"""
    position_title: str = Field(description="岗位名称")
    company_industry: Optional[str] = Field(description="公司行业", default=None)
    summary: str = Field(description="JD核心摘要(100字以内)")
    core_responsibilities: list[str] = Field(
        description="核心岗位职责列表(3-8条)",
    )
    hard_skills: list[TechnologyRequirement] = Field(
        description="硬性技术技能要求",
    )
    soft_skills: list[SoftSkillRequirement] = Field(
        description="软技能要求",
    )
    experience_requirement: ExperienceRequirement
    education_requirement: Optional[str] = Field(
        description="学历要求",
        default=None,
    )
    role_level: str = Field(
        description="岗位级别: 校招/初中级/高级/资深/专家/管理",
    )
    key_evaluation_criteria: list[str] = Field(
        description="面试评价的关键维度(3-5条)",
    )