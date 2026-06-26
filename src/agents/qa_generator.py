"""面试问答生成 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.question_bank import QuestionBank


def run_qa_generator(
    jd_analysis: JDAnalysis | None,
    gap_analysis: GapAnalysis | None,
    resume_text: str,
) -> QuestionBank:
    """运行面试问答生成 Agent"""
    context_parts = [f"【简历原文】\n{resume_text}\n"]

    if jd_analysis:
        context_parts.append(
            f"【JD信息】\n"
            f"岗位: {jd_analysis.position_title}\n"
            f"职责: {'; '.join(jd_analysis.core_responsibilities)}\n"
            f"关键评价维度: {'; '.join(jd_analysis.key_evaluation_criteria)}\n"
            f"硬技能要求: {'; '.join(f'{s.tech_name}({s.proficiency_level})' for s in jd_analysis.hard_skills)}\n"
        )

    if gap_analysis:
        context_parts.append(
            f"【差距分析】\n"
            f"匹配度: {gap_analysis.overall_match_score}/100\n"
            f"高风险领域: {'; '.join(gap_analysis.risk_areas)}\n"
            f"核心优势: {'; '.join(gap_analysis.strengths)}\n"
            f"主要差距: {'; '.join(gap_analysis.top_gaps)}\n"
        )

    user_message = "\n".join(context_parts) + "\n\n请生成全面的面试问答题库。"

    return run_structured_agent(
        model_class=QuestionBank,
        prompt_name="qa_generator",
        user_message=user_message,
    )