"""简历分析模型 - Step 2 输出"""

from pydantic import BaseModel, Field
from typing import Optional


class WorkExperience(BaseModel):
    """工作经历"""
    company: str = Field(description="公司名称")
    position: str = Field(description="职位")
    duration: str = Field(description="时长，如'2020-2023'")
    key_responsibilities: list[str] = Field(description="主要职责（2-5条）")
    achievements: list[str] = Field(description="主要成就（量化优先）")
    technologies_used: list[str] = Field(description="使用的技术栈")


class ProjectExperience(BaseModel):
    """项目经历"""
    name: str = Field(description="项目名称")
    role: str = Field(description="项目角色")
    duration: Optional[str] = Field(description="项目时长", default=None)
    description: str = Field(description="项目描述")
    tech_stack: list[str] = Field(description="技术栈")
    key_contributions: list[str] = Field(description="主要贡献（2-4条）")
    outcomes: Optional[str] = Field(description="项目成果/影响", default=None)
    source_text: str = Field(description="简历原文引用，用于溯源")


class Education(BaseModel):
    """教育背景"""
    school: str = Field(description="学校名称")
    degree: str = Field(description="学位，如'本科'、'硕士'")
    major: Optional[str] = Field(description="专业", default=None)
    graduation_year: Optional[str] = Field(description="毕业年份", default=None)


class ResumeAnalysis(BaseModel):
    """简历分析结果 - Step 2 输出"""
    # 基础信息
    candidate_name: Optional[str] = Field(description="候选人姓名", default=None)
    years_of_experience: int = Field(description="工作年限", ge=0)
    current_role: Optional[str] = Field(description="当前职位", default=None)
    
    # 教育背景
    education: list[Education] = Field(description="教育经历", default_factory=list)
    
    # 工作经历
    work_experiences: list[WorkExperience] = Field(
        description="工作经历列表",
        default_factory=list,
    )
    
    # 项目经历（重点）
    projects: list[ProjectExperience] = Field(
        description="项目经历列表（用于项目介绍和面试问答）",
        default_factory=list,
    )
    
    # 技术栈汇总
    tech_skills: list[str] = Field(
        description="技术技能汇总",
        default_factory=list,
    )
    
    # 软技能/能力
    soft_skills: list[str] = Field(
        description="软技能或能力标签",
        default_factory=list,
    )
    
    # 核心优势（用于自我介绍）
    core_strengths: list[str] = Field(
        description="核心优势/亮点（3-5条）",
        default_factory=list,
    )
    
    # 潜在风险点
    potential_risks: list[str] = Field(
        description="简历中可能的风险点（如跳槽频繁、空白期等）",
        default_factory=list,
    )
    
    # 分析摘要
    summary: str = Field(description="简历分析摘要（100-150字）")