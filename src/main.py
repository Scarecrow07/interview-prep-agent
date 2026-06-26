"""面试准备方案自动生成系统 — 入口"""

import argparse
import sys
from pathlib import Path

from src.graph.graph_builder import build_graph
from src.parsers import parse_pdf, parse_docx
from src.utils.logger import setup_logger

logger = setup_logger()


def read_text(file_path: str) -> str:
    """读取输入文件，支持 txt/pdf/docx"""
    p = Path(file_path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(p)
    elif suffix == ".docx":
        return parse_docx(p)
    else:
        return p.read_text(encoding="utf-8")


def run(
    jd_path: str,
    resume_path: str,
    candidate_name: str | None = None,
    job_type_hint: str = "unknown",
) -> str:
    """运行完整的面试准备方案生成流程

    Args:
        jd_path: JD 文件路径 (.txt/.pdf/.docx)
        resume_path: 简历文件路径
        candidate_name: 候选人姓名
        job_type_hint: 岗位类型提示

    Returns:
        HTML 报告文件路径
    """
    logger.info("读取输入文件...")
    jd_text = read_text(jd_path)
    resume_text = read_text(resume_path)

    logger.info("构建 Agent 工作流图...")
    graph = build_graph()

    initial_state = {
        "jd_text": jd_text,
        "resume_text": resume_text,
        "candidate_name": candidate_name,
        "job_type_hint": job_type_hint,
        "jd_analysis": None,
        "gap_analysis": None,
        "self_intro": None,
        "question_bank": None,
        "coding_problems": None,
        "learning_resources": None,
        "errors": [],
        "skipped_modules": [],
        "generated_at": "",
    }

    logger.info("开始执行 Agent 链...")
    final_state = graph.invoke(initial_state)

    errors = final_state.get("errors", [])
    if errors:
        logger.warning("执行过程中出现以下错误:")
        for err in errors:
            logger.warning(f"  - {err}")

    report_path = final_state.get("report_path")
    if report_path:
        logger.info(f"✅ 面试准备方案已生成: {report_path}")
    else:
        logger.error("报告生成失败")

    return report_path or ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI 面试准备方案自动生成系统",
    )
    parser.add_argument("--jd", required=True, help="JD 文件路径 (.txt/.pdf/.docx)")
    parser.add_argument("--resume", required=True, help="简历文件路径")
    parser.add_argument("--name", default=None, help="候选人姓名")
    parser.add_argument(
        "--type",
        dest="job_type",
        default="unknown",
        choices=["tech", "non_tech", "unknown"],
        help="岗位类型",
    )

    args = parser.parse_args()
    try:
        run(args.jd, args.resume, args.name, args.job_type)
    except Exception as e:
        logger.error(f"执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()