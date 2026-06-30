"""项目介绍模型 - Step 5 输出（含来源约束，不得编造）"""

from pydantic import BaseModel, Field
from typing import Optional


class ProjectSourceReference(BaseModel):
    """项目内容来源追溯"""
    resume_project_name: str = Field(
        description="简历中的原始项目名称",
    )
    resume_section: str = Field(
        description="简历原文引用片段",
    )
    verified: bool = Field(
        description="是否从简历原文验证",
        default=True,
    )


class ProjectIntroDetail(BaseModel):
    """单个项目介绍详情"""
    project_name: str = Field(description="项目名称（必须来自简历projects字段）")
    project_role: str = Field(description="项目角色（必须来自简历）")
    duration: Optional[str] = Field(description="项目时长", default=None)
    
    # 项目介绍核心内容
    background: str = Field(description="项目背景/业务价值")
    tech_stack: list[str] = Field(
        description="技术栈（必须来自简历，不得编造）",
    )
    core_challenges: list[str] = Field(
        description="核心技术挑战（2-3个）",
    )
    solution_approach: str = Field(description="解决方案概述")
    key_contributions: list[str] = Field(
        description="个人核心贡献（来自简历，量化优先）",
        min_length=2, max_length=4,
    )
    outcomes_and_impact: str = Field(description="项目成果/影响（量化指标）")
    
    # 面试话术
    intro_script: str = Field(
        description="项目介绍口述脚本（2-3分钟）",
    )
    key_points_to_emphasize: list[str] = Field(
        description="面试时要重点强调的点",
    )
    
    # 来源验证
    source_reference: ProjectSourceReference = Field(
        description="内容来源追溯（防止编造）",
    )
    
    # 可能的追问方向
    potential_followup_questions: list[str] = Field(
        description="面试官可能追问的方向",
        default_factory=list,
    )


class ProjectIntroSet(BaseModel):
    """项目介绍方案 - Step 5 输出"""
    projects: list[ProjectIntroDetail] = Field(
        description="项目介绍列表（每个项目必须来自简历projects字段）",
        min_length=2, max_length=4,
    )
    recommended_sequence: list[str] = Field(
        description="推荐的项目讲述顺序",
    )
    selection_criteria: str = Field(
        description="项目选择标准说明（为什么选这些项目）",
    )
    preparation_tips: list[str] = Field(
        description="项目介绍准备建议",
    )
    constraint_note: str = Field(
        description="约束说明：所有项目必须来自简历，不得编造",
        default="所有项目信息均来自简历原文，未添加任何虚构项目或技能。",
    )