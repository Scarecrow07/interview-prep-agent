"""笔试编码题生成 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.coding_problem import CodingProblemSet


def run_coding_agent(
    jd_analysis: JDAnalysis | None,
    gap_analysis: GapAnalysis | None,
) -> CodingProblemSet:
    """运行编码题生成 Agent"""
    context_parts = []

    if jd_analysis:
        tech_skills = jd_analysis.hard_skills
        tech_summary = "; ".join(
            f"{s.tech_name}({s.proficiency_level})" for s in tech_skills
        )
        context_parts.append(
            f"【JD技术要求】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"级别: {jd_analysis.role_level}\n"
            f"技术栈: {tech_summary}\n"
            f"职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
        )

    if gap_analysis:
        context_parts.append(
            f"【候选人编程能力】\n"
            f"年限: {gap_analysis.resume_summary.years_of_experience}年\n"
            f"当前角色: {gap_analysis.resume_summary.current_role}\n"
        )

    user_message = "\n".join(context_parts) + "\n\n请生成适合该岗位面试的编码题目。"

    return run_structured_agent(
        model_class=CodingProblemSet,
        prompt_name="coding_agent",
        user_message=user_message,
    )