"""条件路由逻辑"""

from src.graph.state import AgentState


def is_tech_position(state: AgentState) -> str:
    """判断是否为技术岗位，决定是否执行 Coding Agent"""
    job_type = state.get("job_type_hint", "unknown")
    jd = state.get("jd_analysis")

    if job_type == "tech":
        return "coding_agent"

    if jd is not None:
        # 根据 JD 分析结果中的角色级别和硬技能判断
        role_level = jd.role_level
        has_tech_skills = len(jd.hard_skills) > 0
        tech_keywords = [
            "开发", "工程师", "算法", "后端", "前端", "全栈",
            "数据", "架构", "测试", "运维", "DevOps", "AI", "ML",
            "机器学习", "深度学习", "NLP",
        ]
        title_lower = jd.position_title.lower()
        title_matches = any(kw.lower() in title_lower for kw in tech_keywords)

        if has_tech_skills and (title_matches or role_level != "管理"):
            return "coding_agent"

    return "skip_coding"