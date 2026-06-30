"""笔试题目模型 - Step 7 输出（10-15道题目，含LeetCode参考）"""

from pydantic import BaseModel, Field
from typing import Optional


class LeetCodeReference(BaseModel):
    """LeetCode题库参考"""
    problem_id: str = Field(description="LeetCode题号，如'#146'")
    problem_name: str = Field(description="LeetCode题目名称")
    practice_link: str = Field(description="LeetCode练习链接")
    relevance: Optional[str] = Field(
        description="本题与LeetCode原题的差异/适配说明",
        default=None,
    )


class ScoringDimension(BaseModel):
    """评分维度"""
    dimension: str = Field(description="维度名称：正确性/代码质量/边界处理等")
    weight: int = Field(description="权重百分比", ge=0, le=100)
    description: str = Field(description="评分描述")


class ScoringCriteria(BaseModel):
    """评分标准"""
    total_points: int = Field(description="总分", ge=10, le=100)
    dimensions: list[ScoringDimension] = Field(
        description="评分维度列表",
        min_length=3, max_length=6,
    )


class InterviewFollowup(BaseModel):
    """面试追问建议"""
    suggested_questions: list[str] = Field(
        description="可作为面试追问的方向",
        default_factory=list,
    )
    extension_points: list[str] = Field(
        description="题目变体或延伸场景",
        default_factory=list,
    )


class CodingProblem(BaseModel):
    """单道编码题"""
    problem_id: str = Field(description="题目ID，如algo_001, design_001")
    problem_type: str = Field(
        description="题目类型: algorithm / system_design / case_analysis / practical",
    )
    difficulty: str = Field(description="难度: easy / medium / hard")
    title: str = Field(description="题目名称")
    
    # 题目详情
    problem_description: str = Field(description="场景化题目描述")
    input_output_example: Optional[dict] = Field(
        description="输入输出示例",
        default=None,
    )
    
    # LeetCode参考（算法题必须）
    leetcode_reference: Optional[LeetCodeReference] = Field(
        description="LeetCode题库参考（算法题必须，其他类型可为None）",
        default=None,
    )
    
    # 考察点
    skills_assessed: list[str] = Field(
        description="考察点列表",
        min_length=1, max_length=5,
    )
    
    # 来源追溯
    jd_reference: Optional[str] = Field(
        description="关联的JD硬性要求",
        default=None,
    )
    gap_reference: Optional[str] = Field(
        description="本题验证的匹配度短板项",
        default=None,
    )
    
    # 评分标准
    scoring_criteria: ScoringCriteria = Field(description="评分标准")
    
    # 时间预估
    expected_time_minutes: int = Field(description="预期完成时间（分钟）", ge=5, le=60)
    
    # 面试追问
    interview_followup: Optional[InterviewFollowup] = Field(
        description="面试追问建议",
        default=None,
    )


class LeetCodePracticeSummary(BaseModel):
    """LeetCode练习建议"""
    recommended_problems: list[LeetCodeReference] = Field(
        description="推荐练习的LeetCode题目",
        min_length=3, max_length=10,
    )
    practice_strategy: str = Field(description="练习策略建议")


class CodingProblemSet(BaseModel):
    """编码题集 - Step 7 输出（10-15道题目）"""
    total_problems: int = Field(
        description="题目总数（10-15道）",
        ge=10, le=15,
    )
    test_format: str = Field(
        description="笔试形式：在线编程/系统设计/案例分析等",
        default="在线编程",
    )
    time_estimate_minutes: int = Field(
        description="总预估时间（分钟）",
        ge=60, le=180,
    )
    
    # 题目列表
    problems: list[CodingProblem] = Field(
        description="题目列表",
    )
    
    # LeetCode练习建议
    leetcode_practice_summary: LeetCodePracticeSummary = Field(
        description="LeetCode练习建议汇总",
    )
    
    # 语言推荐
    language_recommendation: str = Field(
        description="推荐使用的编程语言（基于简历和JD）",
    )
    
    # 面试衔接建议
    interview衔接建议: dict = Field(
        description="面试衔接建议",
        default_factory=dict,
    )
    
    # 约束说明
    constraint_note: str = Field(
        description="约束说明：题目必须与JD强相关",
        default="所有题目必须与岗位技术栈和核心职责强相关，LeetCode参考便于候选人针对性练习。",
    )