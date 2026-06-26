"""JD 分析 Agent"""

from src.agents.base import run_structured_agent
from src.models.jd_analysis import JDAnalysis


def run_jd_analyzer(jd_text: str) -> JDAnalysis:
    """运行 JD 分析 Agent

    Args:
        jd_text: JD 原文文本
    Returns:
        JDAnalysis 结构化分析结果
    """
    return run_structured_agent(
        model_class=JDAnalysis,
        prompt_name="jd_analyzer",
        user_message=f"请分析以下职位描述（JD）：\n\n{jd_text}",
    )