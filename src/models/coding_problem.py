from pydantic import BaseModel, Field
from typing import Optional


class CodingProblem(BaseModel):
    """单道编码题"""
    problem_number: int
    title: str
    difficulty: str = Field(description="难度: easy / medium / hard")
    estimated_time: str = Field(description="预估完成时间, 如'20分钟'")
    topic_tags: list[str] = Field(
        description="知识点标签,如['数组','动态规划','二分查找']",
    )
    problem_description: str = Field(description="题目描述")
    examples: list[dict] = Field(description="输入输出示例")
    constraints: list[str] = Field(description="约束条件")
    hints: list[str] = Field(description="解题提示(2-3条)")
    solution_approach: str = Field(description="解题思路概述")
    reference_code_language: str = Field(
        description="参考答案使用的编程语言",
    )
    reference_code_snippet: str = Field(
        description="核心代码片段(含注释)",
    )
    complexity_analysis: str = Field(
        description="时间/空间复杂度分析",
    )
    related_leetcode_problems: Optional[list[str]] = Field(
        description="相关 LeetCode 题目编号",
        default=None,
    )


class CodingProblemSet(BaseModel):
    """编码题集"""
    total_problems: int = Field(ge=3, le=10)
    language_recommendation: str = Field(
        description="推荐使用的编程语言(基于简历和JD)",
    )
    problems: list[CodingProblem]
    preparation_tips: str = Field(description="笔试/面试准备贴士")