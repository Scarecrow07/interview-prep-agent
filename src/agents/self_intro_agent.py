"""自我介绍生成 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.self_intro import SelfIntroScript


def run_self_intro_agent(
    jd_analysis: JDAnalysis | None,
    gap_analysis: GapAnalysis | None,
) -> SelfIntroScript:
    """运行自我介绍生成 Agent"""
    context_parts = []

    if jd_analysis:
        context_parts.append(
            f"【JD信息】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"核心职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
        )

    if gap_analysis:
        context_parts.append(
            f"【匹配分析】\n"
            f"总体匹配度: {gap_analysis.overall_match_score}/100\n"
            f"核心优势: {'; '.join(gap_analysis.strengths)}\n"
            f"主要差距: {'; '.join(gap_analysis.top_gaps)}\n"
            f"简历摘要: 年限={gap_analysis.resume_summary.years_of_experience}年, "
            f"角色={gap_analysis.resume_summary.current_role}, "
            f"项目={'; '.join(gap_analysis.resume_summary.notable_projects)}\n"
        )

    user_message = "\n".join(context_parts) + "\n\n请生成适合该候选人的自我介绍方案。"

    return run_structured_agent(
        model_class=SelfIntroScript,
        prompt_name="self_intro_agent",
        user_message=user_message,
    )