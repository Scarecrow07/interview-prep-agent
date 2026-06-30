"""自我介绍 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.self_intro import SelfIntroScript
from typing import Optional


def run_self_intro_agent(
    jd_analysis: Optional[JDAnalysis],
    resume_analysis: Optional[ResumeAnalysis],
    gap_analysis: Optional[GapAnalysis],
    additional_info: Optional[str] = None,
) -> SelfIntroScript:
    """运行自我介绍 Agent

    Args:
        jd_analysis: JD分析结果
        resume_analysis: 简历分析结果
        gap_analysis: 匹配度分析结果
        additional_info: 用户补充信息（可选）
    Returns:
        SelfIntroScript 自我介绍方案
    """
    jd_summary = ""
    if jd_analysis:
        jd_summary = (
            f"【JD分析摘要】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"核心职责: {'; '.join(jd_analysis.core_responsibilities[:3])}\n"
            f"硬性要求: {'; '.join(f'{s.tech_name}({"必须" if s.is_required else "加分"})' for s in jd_analysis.hard_skills[:5])}\n"
            f"级别: {jd_analysis.role_level}\n"
            f"评价维度: {'; '.join(jd_analysis.key_evaluation_criteria)}\n"
        )

    resume_summary = ""
    if resume_analysis:
        resume_summary = (
            f"【简历分析摘要】\n"
            f"候选人: {resume_analysis.candidate_name or '未知'}\n"
            f"工作年限: {resume_analysis.years_of_experience}年\n"
            f"当前职位: {resume_analysis.current_role or '未知'}\n"
            f"核心优势: {'; '.join(resume_analysis.core_strengths)}\n"
            f"技术栈: {'; '.join(resume_analysis.tech_skills[:10])}\n"
        )

    gap_summary = ""
    if gap_analysis:
        gap_summary = (
            f"【匹配度分析摘要】\n"
            f"整体匹配度: {gap_analysis.overall_match_score}%\n"
            f"核心优势: {'; '.join(gap_analysis.strengths)}\n"
            f"短板: {'; '.join(gap_analysis.top_gaps)}\n"
            f"准备策略: {gap_analysis.preparation_strategy}\n"
        )

    additional_info_section = ""
    if additional_info:
        additional_info_section = f"【用户补充信息】\n{additional_info}\n"

    user_message = (
        f"{jd_summary}\n"
        f"{resume_summary}\n"
        f"{gap_summary}\n"
        f"{additional_info_section}\n"
        "请生成自我介绍方案。重要约束：内容必须来自简历和JD，不得编造经历。"
    )

    return run_structured_agent(
        model_class=SelfIntroScript,
        prompt_name="self_intro_agent",
        user_message=user_message,
    )