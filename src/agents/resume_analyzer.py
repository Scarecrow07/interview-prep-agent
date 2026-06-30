"""简历分析 Agent"""

from src.agents.base import run_structured_agent
from src.models.resume_analysis import ResumeAnalysis


def run_resume_analyzer(resume_text: str) -> ResumeAnalysis:
    """运行简历分析 Agent

    Args:
        resume_text: 简历原文文本
    Returns:
        ResumeAnalysis 结构化分析结果
    """
    return run_structured_agent(
        model_class=ResumeAnalysis,
        prompt_name="resume_analyzer",
        user_message=f"请分析以下简历：\n\n{resume_text}",
    )