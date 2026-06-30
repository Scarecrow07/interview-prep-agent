"""简历-JD 匹配分析 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from typing import Optional


def run_gap_analyzer(
    jd_text: str,
    resume_text: str,
    jd_analysis: Optional[JDAnalysis],
    resume_analysis: Optional[ResumeAnalysis],
) -> GapAnalysis:
    """运行差距分析 Agent

    Args:
        jd_text: JD 原文
        resume_text: 简历原文
        jd_analysis: JD 分析结果（可选）
        resume_analysis: 简历分析结果（可选）
    Returns:
        GapAnalysis 差距分析结果
    """
    jd_summary = ""
    if jd_analysis:
        jd_summary = (
            f"【JD分析摘要】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"核心职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
            f"硬技能要求: {'; '.join(f'{s.tech_name}({s.proficiency_level},{"必须" if s.is_required else "加分"})' for s in jd_analysis.hard_skills)}\n"
            f"软技能要求: {'; '.join(s.skill_name for s in jd_analysis.soft_skills)}\n"
            f"经验要求: {jd_analysis.experience_requirement.min_years}年+\n"
            f"级别: {jd_analysis.role_level}\n"
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
            f"项目数量: {len(resume_analysis.projects)}\n"
        )

    user_message = (
        f"{jd_summary}\n"
        f"{resume_summary}\n"
        f"【JD原文】\n{jd_text}\n\n"
        f"【简历原文】\n{resume_text}\n\n"
        "请进行详细的匹配分析。重要约束：匹配评分必须基于简历原文证据，不得夸大匹配度。"
    )

    return run_structured_agent(
        model_class=GapAnalysis,
        prompt_name="gap_analyzer",
        user_message=user_message,
    )