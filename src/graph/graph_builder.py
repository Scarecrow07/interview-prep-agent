"""构建 LangGraph StateGraph - 完整面试准备流程"""

from langgraph.graph import StateGraph, START, END

from src.graph.state import AgentState
from src.graph.nodes import (
    validate_input,
    analyze_jd,
    analyze_resume,
    analyze_gap,
    generate_self_intro,
    generate_project_intro,
    generate_qa,
    generate_coding_problems,
    generate_learning_resources,
    skip_coding,
    generate_report,
)
from src.graph.router import is_tech_position


def build_graph() -> StateGraph:
    """构建完整的 Agent 工作流图
    
    流程顺序（7步面试作战手册）：
    1. 输入校验
    2. JD分析 (Step 1)
    3. 简历分析 (Step 2)
    4. 匹配度分析 (Step 3)
    5. 自我介绍生成 (Step 4)
    6. 项目介绍生成 (Step 5)
    7. 面试问答生成 (Step 6, 20-30道)
    8. 笔试题目生成 (Step 7, 10-15道, 仅技术岗位)
    9. 学习资源推荐 (Step 8)
    10. HTML报告生成
    """
    builder = StateGraph(AgentState)

    # 注册节点（按流程顺序）
    builder.add_node("validate_input", validate_input)
    builder.add_node("jd_analyzer", analyze_jd)              # Step 1
    builder.add_node("resume_analyzer", analyze_resume)      # Step 2
    builder.add_node("gap_analyzer", analyze_gap)            # Step 3
    builder.add_node("self_intro", generate_self_intro)      # Step 4
    builder.add_node("project_intro", generate_project_intro) # Step 5
    builder.add_node("qa_generator", generate_qa)            # Step 6
    builder.add_node("coding_agent", generate_coding_problems) # Step 7 (技术岗位)
    builder.add_node("skip_coding", skip_coding)             # Step 7 (非技术岗位)
    builder.add_node("learning_resource", generate_learning_resources) # Step 8
    builder.add_node("report_generator", generate_report)

    # 连线（按流程顺序）
    builder.add_edge(START, "validate_input")
    builder.add_edge("validate_input", "jd_analyzer")
    builder.add_edge("jd_analyzer", "resume_analyzer")
    builder.add_edge("resume_analyzer", "gap_analyzer")
    builder.add_edge("gap_analyzer", "self_intro")
    builder.add_edge("self_intro", "project_intro")
    builder.add_edge("project_intro", "qa_generator")

    # 条件路由: 技术岗位 → Coding, 否则跳过
    builder.add_conditional_edges(
        "qa_generator",
        is_tech_position,
        {
            "coding_agent": "coding_agent",
            "skip_coding": "skip_coding",
        },
    )

    # Coding 完成或跳过之后 → 学习资源 → 报告
    builder.add_edge("coding_agent", "learning_resource")
    builder.add_edge("skip_coding", "learning_resource")
    builder.add_edge("learning_resource", "report_generator")
    builder.add_edge("report_generator", END)

    return builder.compile()