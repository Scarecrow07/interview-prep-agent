"""学习资料推荐 Agent"""

from src.agents.base import run_structured_agent
from src.models.gap_analysis import GapAnalysis
from src.models.coding_problem import CodingProblemSet
from src.models.learning_resource import LearningResources
from typing import Optional


def run_resource_agent(
    gap_analysis: GapAnalysis | None,
    coding_problems: Optional[CodingProblemSet] = None,
) -> LearningResources:
    """运行学习资料推荐 Agent"""
    context_parts = []

    if gap_analysis:
        context_parts.append(
            f"【差距分析】\n"
            f"主要差距: {'; '.join(gap_analysis.top_gaps)}\n"
            f"高风险领域: {'; '.join(gap_analysis.risk_areas)}\n"
            f"准备策略: {gap_analysis.preparation_strategy}\n"
        )

    if coding_problems:
        tags = set()
        for p in coding_problems.problems:
            tags.update(p.topic_tags)
        context_parts.append(
            f"【编码题涉及知识点】\n{'; '.join(sorted(tags))}\n"
        )

    user_message = "\n".join(context_parts) + "\n\n请推荐针对性的学习资料和资源。"

    return run_structured_agent(
        model_class=LearningResources,
        prompt_name="resource_agent",
        user_message=user_message,
    )