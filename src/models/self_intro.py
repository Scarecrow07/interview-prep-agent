"""自我介绍模型 - Step 4 输出（含来源约束）"""

from pydantic import BaseModel, Field
from typing import Optional


class SourceReference(BaseModel):
    """内容来源追溯"""
    jd_requirement: Optional[str] = Field(
        description="来源JD的具体要求",
        default=None,
    )
    resume_section: Optional[str] = Field(
        description="来源简历的具体章节",
        default=None,
    )
    user_input: Optional[str] = Field(
        description="来源用户补充信息",
        default=None,
    )


class SelfIntroductionVersion(BaseModel):
    """单个自我介绍版本"""
    duration: str = Field(description="时长: 2min / 3min")
    target_scenario: str = Field(
        description="适用场景: 一面 / 技术面 / 总监面 / HR面",
    )
    script: str = Field(description="完整自我介绍脚本")
    key_highlights: list[str] = Field(
        description="脚本中强调的核心亮点",
        min_length=2, max_length=5,
    )
    source_references: list[SourceReference] = Field(
        description="内容来源追溯（防止编造）",
        default_factory=list,
    )


class SelfIntroScript(BaseModel):
    """自我介绍方案 - Step 4 输出"""
    versions: list[SelfIntroductionVersion] = Field(
        min_length=2, max_length=3,
        description="不同时长的自我介绍版本（2-3个）",
    )
    core_selling_points: list[str] = Field(
        description="核心卖点（必须与JD硬性要求匹配）",
        min_length=2, max_length=5,
    )
    jd_alignment: str = Field(
        description="自我介绍与JD硬性要求的匹配说明",
    )
    usage_tips: list[str] = Field(
        description="表达技巧与注意事项",
    )
    common_mistakes_to_avoid: list[str] = Field(
        description="自我介绍中应避免的常见错误",
    )
    constraint_note: str = Field(
        description="约束说明：内容必须来自简历和JD，不得编造",
        default="所有内容均来自简历原文和JD硬性要求，未添加任何虚构经历或技能。",
    )