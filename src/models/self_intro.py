from pydantic import BaseModel, Field


class SelfIntroductionVersion(BaseModel):
    """单个自我介绍版本"""
    duration: str = Field(description="时长: 1min / 2min / 3min")
    target_scenario: str = Field(
        description="适用场景: 群面 / 一面 / 技术面 / 总监面",
    )
    script: str = Field(description="完整自我介绍脚本")
    key_highlights: list[str] = Field(description="脚本中强调的核心亮点")


class SelfIntroScript(BaseModel):
    """自我介绍方案"""
    versions: list[SelfIntroductionVersion] = Field(
        min_length=2, max_length=4,
        description="不同时长的自我介绍版本",
    )
    usage_tips: list[str] = Field(
        description="表达技巧与注意事项",
    )
    common_mistakes_to_avoid: list[str] = Field(
        description="针对该JD/简历组合, 自我介绍中应避免的常见错误",
    )