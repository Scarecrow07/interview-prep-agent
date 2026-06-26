"""HTML 报告渲染器"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from src.graph.state import AgentState

_TEMPLATE_DIR = Path(__file__).parent / "templates"


def render_report(state: AgentState) -> str:
    """将 AgentState 渲染为 HTML 报告

    Args:
        state: 完整的 AgentState
    Returns:
        生成的 HTML 文件路径
    """
    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATE_DIR)),
        autoescape=True,
    )
    template = env.get_template("interview_prep_report.html.j2")

    # 从 state 提取各模块数据
    jd = state.get("jd_analysis")
    gap = state.get("gap_analysis")
    intro = state.get("self_intro")
    qa = state.get("question_bank")
    coding = state.get("coding_problems")
    resources = state.get("learning_resources")
    errors = state.get("errors", [])
    skipped = state.get("skipped_modules", [])

    candidate_name = state.get("candidate_name") or "候选人"
    generated_at = state.get("generated_at", "")

    html = template.render(
        jd=jd.model_dump() if jd else None,
        gap=gap.model_dump() if gap else None,
        intro=intro.model_dump() if intro else None,
        qa=qa.model_dump() if qa else None,
        coding=coding.model_dump() if coding else None,
        resources=resources.model_dump() if resources else None,
        errors=errors,
        skipped_modules=skipped,
        candidate_name=candidate_name,
        generated_at=generated_at,
    )

    # 写文件
    output_dir = Path("examples/output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "interview_prep_report.html"
    output_path.write_text(html, encoding="utf-8")

    return str(output_path.resolve())