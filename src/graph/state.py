"""全局状态定义"""

from __future__ import annotations
from typing import Optional
from typing_extensions import TypedDict

from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.self_intro import SelfIntroScript
from src.models.project_intro import ProjectIntroSet
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
    additional_info: Optional[str]  # 用户补充信息

    # 各模块输出（按流程顺序）
    # Step 1: JD分析
    jd_analysis: Optional[JDAnalysis]
    
    # Step 2: 简历分析
    resume_analysis: Optional[ResumeAnalysis]
    
    # Step 3: 匹配度分析
    gap_analysis: Optional[GapAnalysis]
    
    # Step 4: 自我介绍
    self_intro: Optional[SelfIntroScript]
    
    # Step 5: 项目介绍
    project_intro: Optional[ProjectIntroSet]
    
    # Step 6: 面试问答（20-30道）
    question_bank: Optional[QuestionBank]
    
    # Step 7: 笔试题目（10-15道，技术岗位）
    coding_problems: Optional[CodingProblemSet]
    
    # Step 8: 学习资源推荐
    learning_resources: Optional[LearningResources]

    # 报告输出
    report_path: Optional[str]

    # 执行追踪
    errors: list[str]
    skipped_modules: list[str]
    generated_at: str