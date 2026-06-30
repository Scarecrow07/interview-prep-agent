"""所有 Agent 节点的实现"""

from datetime import datetime
from typing import Any

from src.graph.state import AgentState
from src.models.input_schema import InterviewPrepInput
from src.models.jd_analysis import JDAnalysis
from src.models.resume_analysis import ResumeAnalysis
from src.models.gap_analysis import GapAnalysis
from src.models.self_intro import SelfIntroScript
from src.models.project_intro import ProjectIntroSet
from src.models.question_bank import QuestionBank
from src.models.coding_problem import CodingProblemSet
from src.models.learning_resource import LearningResources


def validate_input(state: AgentState) -> dict[str, Any]:
    """输入校验节点"""
    errors: list[str] = []
    try:
        InterviewPrepInput(
            jd_text=state["jd_text"],
            resume_text=state["resume_text"],
            candidate_name=state.get("candidate_name"),
            job_type_hint=state.get("job_type_hint", "unknown"),
        )
    except Exception as e:
        errors.append(f"输入校验失败: {str(e)}")

    return {
        "errors": errors,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def analyze_jd(state: AgentState) -> dict[str, Any]:
    """JD 分析 Agent 节点 - Step 1"""
    errors: list[str] = state.get("errors", [])
    jd_analysis: JDAnalysis | None = None

    try:
        from src.agents.jd_analyzer import run_jd_analyzer
        jd_analysis = run_jd_analyzer(state["jd_text"])
    except Exception as e:
        errors.append(f"JD分析失败: {str(e)}")

    return {
        "jd_analysis": jd_analysis,
        "errors": errors,
    }


def analyze_resume(state: AgentState) -> dict[str, Any]:
    """简历分析 Agent 节点 - Step 2"""
    errors: list[str] = state.get("errors", [])
    resume_analysis: ResumeAnalysis | None = None

    try:
        from src.agents.resume_analyzer import run_resume_analyzer
        resume_analysis = run_resume_analyzer(state["resume_text"])
    except Exception as e:
        errors.append(f"简历分析失败: {str(e)}")

    return {
        "resume_analysis": resume_analysis,
        "errors": errors,
    }


def analyze_gap(state: AgentState) -> dict[str, Any]:
    """简历-JD 匹配分析 Agent 节点 - Step 3"""
    errors: list[str] = state.get("errors", [])
    gap_analysis: GapAnalysis | None = None

    try:
        from src.agents.gap_analyzer import run_gap_analyzer
        gap_analysis = run_gap_analyzer(
            jd_text=state["jd_text"],
            resume_text=state["resume_text"],
            jd_analysis=state["jd_analysis"],
            resume_analysis=state["resume_analysis"],
        )
    except Exception as e:
        errors.append(f"差距分析失败: {str(e)}")

    return {
        "gap_analysis": gap_analysis,
        "errors": errors,
    }


def generate_self_intro(state: AgentState) -> dict[str, Any]:
    """自我介绍生成节点 - Step 4"""
    errors: list[str] = state.get("errors", [])
    self_intro: SelfIntroScript | None = None

    try:
        from src.agents.self_intro_agent import run_self_intro_agent
        self_intro = run_self_intro_agent(
            jd_analysis=state["jd_analysis"],
            resume_analysis=state["resume_analysis"],
            gap_analysis=state["gap_analysis"],
            additional_info=state.get("additional_info"),
        )
    except Exception as e:
        errors.append(f"自我介绍生成失败: {str(e)}")

    return {
        "self_intro": self_intro,
        "errors": errors,
    }


def generate_project_intro(state: AgentState) -> dict[str, Any]:
    """项目介绍生成节点 - Step 5"""
    errors: list[str] = state.get("errors", [])
    project_intro: ProjectIntroSet | None = None

    try:
        from src.agents.project_intro_agent import run_project_intro_agent
        project_intro = run_project_intro_agent(
            resume_analysis=state["resume_analysis"],
            jd_analysis=state["jd_analysis"],
            gap_analysis=state["gap_analysis"],
        )
    except Exception as e:
        errors.append(f"项目介绍生成失败: {str(e)}")

    return {
        "project_intro": project_intro,
        "errors": errors,
    }


def generate_qa(state: AgentState) -> dict[str, Any]:
    """面试问答生成节点 - Step 6（20-30道题目）"""
    errors: list[str] = state.get("errors", [])
    question_bank: QuestionBank | None = None

    try:
        from src.agents.qa_generator import run_qa_generator
        question_bank = run_qa_generator(
            jd_analysis=state["jd_analysis"],
            resume_analysis=state["resume_analysis"],
            gap_analysis=state["gap_analysis"],
            resume_text=state["resume_text"],
        )
    except Exception as e:
        errors.append(f"面试问答生成失败: {str(e)}")

    return {
        "question_bank": question_bank,
        "errors": errors,
    }


def generate_coding_problems(state: AgentState) -> dict[str, Any]:
    """笔试编码题生成节点 - Step 7（10-15道题目，仅技术岗位）"""
    errors: list[str] = state.get("errors", [])
    coding_problems: CodingProblemSet | None = None

    try:
        from src.agents.coding_agent import run_coding_agent
        coding_problems = run_coding_agent(
            jd_analysis=state["jd_analysis"],
            gap_analysis=state["gap_analysis"],
        )
    except Exception as e:
        errors.append(f"编码题生成失败: {str(e)}")

    return {
        "coding_problems": coding_problems,
        "errors": errors,
    }


def skip_coding(state: AgentState) -> dict[str, Any]:
    """非技术岗位时跳过编码题"""
    skipped = state.get("skipped_modules", [])
    skipped.append("coding_problems")
    return {
        "coding_problems": None,
        "skipped_modules": skipped,
    }


def generate_learning_resources(state: AgentState) -> dict[str, Any]:
    """学习资料推荐节点 - Step 8"""
    errors: list[str] = state.get("errors", [])
    learning_resources: LearningResources | None = None

    try:
        from src.agents.resource_agent import run_resource_agent
        learning_resources = run_resource_agent(
            gap_analysis=state["gap_analysis"],
            coding_problems=state.get("coding_problems"),
        )
    except Exception as e:
        errors.append(f"学习资料推荐失败: {str(e)}")

    return {
        "learning_resources": learning_resources,
        "errors": errors,
    }


def generate_report(state: AgentState) -> dict[str, Any]:
    """HTML 报告生成节点"""
    errors: list[str] = state.get("errors", [])

    try:
        from src.report.renderer import render_report
        output_path = render_report(state)
        return {"report_path": output_path, "errors": errors}
    except Exception as e:
        errors.append(f"报告生成失败: {str(e)}")
        return {"report_path": None, "errors": errors}