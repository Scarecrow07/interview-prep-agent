from pydantic import BaseModel, Field
from typing import Optional


class LearningResource(BaseModel):
    """单个学习资源"""
    resource_type: str = Field(
        description=(
            "类型: book / online_course / documentation / video"
            " / practice_platform / article"
        ),
    )
    title: str
    target_skill: str = Field(description="针对的技能名称")
    reason: str = Field(
        description="为什么推荐这个资源(结合差距分析)",
    )
    url_or_reference: Optional[str] = Field(
        description="链接或引用信息",
        default=None,
    )
    estimated_time_required: Optional[str] = Field(
        description="预估学习时长, 如'2周'",
        default=None,
    )
    priority: str = Field(description="学习优先级: high / medium / low")
    difficulty_level: str = Field(
        description="学习难度: beginner / intermediate / advanced",
    )


class LearningResources(BaseModel):
    """学习资源方案"""
    resources: list[LearningResource] = Field(
        min_length=5,
        description="推荐的学习资源列表",
    )
    study_plan_summary: str = Field(
        description=(
            "学习计划摘要"
            "(如果有3-5天准备时间, 建议的学习路径)"
        ),
    )
    key_knowledge_points: list[str] = Field(
        description="需要重点掌握的知识要点清单",
    )