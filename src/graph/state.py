from __future__ import annotations
from typing import Optional
from typing_extensions import TypedDict

from src.models.jd_analysis import JDAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.self_intro import SelfIntroScript
from src.models.question_bank import QuestionBank
from src.models.coding_problem import CodingProblemSet
from src.models.learning_resource import LearningResources


class AgentState(TypedDict):
    """全局状态，在每个 Agent 节点间传递"""
    # 输入
    jd_text: str
    resume_text: str
    candidate_name: Optional[str]
    job_type_hint: str

    # 各模块输出
    jd_analysis: Optional[JDAnalysis]
    gap_analysis: Optional[GapAnalysis]
    self_intro: Optional[SelfIntroScript]
    question_bank: Optional[QuestionBank]
    coding_problems: Optional[CodingProblemSet]
    learning_resources: Optional[LearningResources]

    # 执行追踪
    errors: list[str]
    skipped_modules: list[str]
    generated_at: str