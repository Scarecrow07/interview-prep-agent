"""构建 LangGraph StateGraph"""

from langgraph.graph import StateGraph, START, END

from src.graph.state import AgentState
from src.graph.nodes import (
    validate_input,
    analyze_jd,
    analyze_gap,
    generate_self_intro,
    generate_qa,
    generate_coding_problems,
    generate_learning_resources,
    skip_coding,
    generate_report,
)
from src.graph.router import is_tech_position


def build_graph() -> StateGraph:
    """构建完整的 Agent 工作流图"""
    builder = StateGraph(AgentState)

    # 注册节点
    builder.add_node("validate_input", validate_input)
    builder.add_node("jd_analyzer", analyze_jd)
    builder.add_node("gap_analyzer", analyze_gap)
    builder.add_node("self_intro", generate_self_intro)
    builder.add_node("qa_generator", generate_qa)
    builder.add_node("coding_agent", generate_coding_problems)
    builder.add_node("skip_coding", skip_coding)
    builder.add_node("learning_resource", generate_learning_resources)
    builder.add_node("report_generator", generate_report)

    # 连线
    builder.add_edge(START, "validate_input")
    builder.add_edge("validate_input", "jd_analyzer")
    builder.add_edge("jd_analyzer", "gap_analyzer")

    # 条件路由: 技术岗位 → Coding, 否则跳过
    builder.add_conditional_edges(
        "gap_analyzer",
        is_tech_position,
        {
            "coding_agent": "coding_agent",
            "skip_coding": "skip_coding",
        },
    )

    # Coding 完成或跳过之后
    builder.add_edge("coding_agent", "self_intro")
    builder.add_edge("skip_coding", "self_intro")
    builder.add_edge("self_intro", "qa_generator")
    builder.add_edge("qa_generator", "learning_resource")
    builder.add_edge("learning_resource", "report_generator")
    builder.add_edge("report_generator", END)

    return builder.compile()