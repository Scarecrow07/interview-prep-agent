"""面试问答生成 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.question_bank import QuestionBank
from typing import Optional


def run_qa_generator(
    jd_analysis: Optional[JDAnalysis],
    resume_analysis: Optional[ResumeAnalysis],
    gap_analysis: Optional[GapAnalysis],
    resume_text: str,
) -> QuestionBank:
    """运行面试问答生成 Agent

    Args:
        jd_analysis: JD分析结果
        resume_analysis: 简历分析结果
        gap_analysis: 匹配度分析结果
        resume_text: 简历原文（用于项目问题验证）
    Returns:
        QuestionBank 面试题库（20-30道）
    """
    jd_summary = ""
    if jd_analysis:
        jd_summary = (
            f"【JD分析摘要】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"级别: {jd_analysis.role_level}\n"
            f"核心职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
            f"硬技能: {'; '.join(f'{s.tech_name}' for s in jd_analysis.hard_skills)}\n"
            f"软技能: {'; '.join(s.skill_name for s in jd_analysis.soft_skills)}\n"
            f"评价维度: {'; '.join(jd_analysis.key_evaluation_criteria)}\n"
        )

    resume_summary = ""
    if resume_analysis:
        resume_summary = (
            f"【简历分析摘要】\n"
            f"候选人: {resume_analysis.candidate_name or '未知'}\n"
            f"项目数量: {len(resume_analysis.projects)}\n"
        )
        
        # 添加项目详情用于项目深挖类问题
        projects_detail = "\n【项目详情】\n"
        for proj in resume_analysis.projects[:4]:  # 最多4个项目
            projects_detail += (
                f"- {proj.name}\n"
                f"  角色: {proj.role}\n"
                f"  技术栈: {', '.join(proj.tech_stack)}\n"
            )
        resume_summary += projects_detail

    gap_summary = ""
    if gap_analysis:
        gap_summary = (
            f"【匹配度分析摘要】\n"
            f"整体匹配度: {gap_analysis.overall_match_score}%\n"
            f"核心优势: {'; '.join(gap_analysis.strengths)}\n"
            f"短板: {'; '.join(gap_analysis.top_gaps)}\n"
            f"风险领域: {'; '.join(gap_analysis.risk_areas)}\n"
        )

    user_message = (
        f"{jd_summary}\n"
        f"{resume_summary}\n"
        f"{gap_summary}\n"
        f"【简历原文片段】\n{resume_text[:2000]}\n\n"
        "请生成20-30道面试问答题目。重要约束：项目问题必须基于简历projects字段，技术问题覆盖JD核心技术栈，短板问题来自匹配度分析。"
    )

    return run_structured_agent(
        model_class=QuestionBank,
        prompt_name="qa_generator",
        user_message=user_message,
    )