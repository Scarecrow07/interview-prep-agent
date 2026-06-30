"""项目介绍 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.project_intro import ProjectIntroSet
from typing import Optional


def run_project_intro_agent(
    resume_analysis: ResumeAnalysis,
    jd_analysis: Optional[JDAnalysis],
    gap_analysis: Optional[GapAnalysis],
) -> ProjectIntroSet:
    """运行项目介绍 Agent

    Args:
        resume_analysis: 简历分析结果
        jd_analysis: JD分析结果（可选）
        gap_analysis: 匹配度分析结果（可选）
    Returns:
        ProjectIntroSet 项目介绍方案
    """
    resume_summary = ""
    if resume_analysis:
        resume_summary = (
            f"【简历分析摘要】\n"
            f"候选人: {resume_analysis.candidate_name or '未知'}\n"
            f"工作年限: {resume_analysis.years_of_experience}年\n"
            f"当前职位: {resume_analysis.current_role or '未知'}\n"
            f"核心优势: {'; '.join(resume_analysis.core_strengths)}\n"
            f"项目数量: {len(resume_analysis.projects)}\n"
        )
        
        # 添加项目详情
        projects_detail = "\n【项目列表】\n"
        for proj in resume_analysis.projects:
            projects_detail += (
                f"- {proj.name} ({proj.role})\n"
                f"  技术栈: {', '.join(proj.tech_stack)}\n"
                f"  贡献: {', '.join(proj.key_contributions)}\n"
            )
        resume_summary += projects_detail

    jd_summary = ""
    if jd_analysis:
        jd_summary = (
            f"【JD分析摘要】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"级别: {jd_analysis.role_level}\n"
            f"硬技能: {'; '.join(f'{s.tech_name}' for s in jd_analysis.hard_skills[:5])}\n"
        )

    gap_summary = ""
    if gap_analysis:
        gap_summary = (
            f"【匹配度分析摘要】\n"
            f"整体匹配度: {gap_analysis.overall_match_score}%\n"
            f"核心优势: {'; '.join(gap_analysis.strengths)}\n"
            f"短板: {'; '.join(gap_analysis.top_gaps)}\n"
        )

    user_message = (
        f"{resume_summary}\n"
        f"{jd_summary}\n"
        f"{gap_summary}\n\n"
        "请基于简历中的项目经历生成项目介绍方案。重要约束：所有项目必须来自简历projects字段，不得编造。"
    )

    return run_structured_agent(
        model_class=ProjectIntroSet,
        prompt_name="project_intro_agent",
        user_message=user_message,
    )