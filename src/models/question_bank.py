from pydantic import BaseModel, Field
from typing import Optional


class InterviewQuestion(BaseModel):
    """单个面试问题"""
    question_number: int
    category: str = Field(
        description=(
            "问题分类: "
            "tech_deep_dive / experience_probe / behavioral / scenario / hr / motivation"
        ),
    )
    difficulty: str = Field(description="难度: easy / medium / hard")
    question_text: str
    evaluation_dimension: str = Field(
        description="考察维度, 对应JDAnalysis.key_evaluation_criteria中的维度",
    )
    answer_framework: Optional[str] = Field(
        description="回答框架建议,如'STAR法则'",
        default=None,
    )
    reference_answer_key_points: list[str] = Field(
        description="参考答案的要点(结合候选人简历给出个性化内容)",
    )
    suggested_time_limit: str = Field(
        description="建议回答时长, 如'2-3分钟'",
    )
    follow_up_hints: Optional[list[str]] = Field(
        description="可能的追问方向",
        default=None,
    )


class QuestionBank(BaseModel):
    """面试题库"""
    total_questions: int
    questions: list[InterviewQuestion] = Field(
        min_length=10, max_length=30,
        description="面试题目列表, 至少10题",
    )
    focus_areas_advice: str = Field(
        description="面试准备重点领域建议",
    )