"""笔试题目生成 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.coding_problem import CodingProblemSet
from typing import Optional


def run_coding_agent(
    jd_analysis: Optional[JDAnalysis],
    gap_analysis: Optional[GapAnalysis],
) -> CodingProblemSet:
    """运行笔试题目生成 Agent

    Args:
        jd_analysis: JD分析结果
        gap_analysis: 匹配度分析结果
    Returns:
        CodingProblemSet 笔试题目集（10-15道）
    """
    jd_summary = ""
    if jd_analysis:
        jd_summary = (
            f"【JD分析摘要】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"级别: {jd_analysis.role_level}\n"
            f"核心职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
            f"硬技能: {'; '.join(f'{s.tech_name}({s.proficiency_level})' for s in jd_analysis.hard_skills)}\n"
            f"评价维度: {'; '.join(jd_analysis.key_evaluation_criteria)}\n"
        )

    gap_summary = ""
    if gap_analysis:
        gap_summary = (
            f"【匹配度分析摘要】\n"
            f"整体匹配度: {gap_analysis.overall_match_score}%\n"
            f"短板: {'; '.join(gap_analysis.top_gaps)}\n"
        )

    user_message = (
        f"{jd_summary}\n"
        f"{gap_summary}\n\n"
        "请生成10-15道笔试题目。重要约束：算法题必须标注LeetCode参考，题目必须与JD技术栈强相关。"
    )

    return run_structured_agent(
        model_class=CodingProblemSet,
        prompt_name="coding_agent",
        user_message=user_message,
    )