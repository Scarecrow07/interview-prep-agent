"""Streamlit Web 界面"""

import os
import tempfile
from pathlib import Path

import streamlit as st

from src.graph.graph_builder import build_graph
from src.utils.logger import setup_logger

logger = setup_logger()

st.set_page_config(
    page_title="AI 面试准备方案生成器",
    page_icon="📋",
    layout="centered",
)

st.title("AI 面试准备方案生成器")
st.markdown(
    "上传 **职位描述（JD）** 和 **简历**，自动生成完整的面试准备方案报告。"
)

# 检查 API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        help="输入你的 OpenAI API Key，不会持久化保存",
    )
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

st.sidebar.header("配置")
job_type = st.sidebar.selectbox(
    "岗位类型",
    options=["unknown", "tech", "non_tech"],
    format_func=lambda x: {"unknown": "自动识别", "tech": "技术岗位", "non_tech": "非技术岗位"}[x],
    help="选择 '技术岗位' 会生成编码题，'非技术岗位' 跳过编码题",
)
candidate_name = st.sidebar.text_input("候选人姓名（可选）", placeholder="如：张三")

col1, col2 = st.columns(2)

with col1:
    jd_file = st.file_uploader(
        "上传 JD 文件",
        type=["txt", "pdf", "docx"],
        help="支持 .txt / .pdf / .docx 格式",
    )

with col2:
    resume_file = st.file_uploader(
        "上传简历文件",
        type=["txt", "pdf", "docx"],
        help="支持 .txt / .pdf / .docx 格式",
    )

if jd_file and resume_file:
    if st.button("🚀 生成面试准备方案", type="primary", use_container_width=True):
        if not os.getenv("OPENAI_API_KEY"):
            st.error("请先在侧边栏输入 OpenAI API Key")
            st.stop()

        # 将上传的文件保存到临时目录
        with tempfile.TemporaryDirectory() as tmpdir:
            jd_path = Path(tmpdir) / jd_file.name
            jd_path.write_bytes(jd_file.getvalue())

            resume_path = Path(tmpdir) / resume_file.name
            resume_path.write_bytes(resume_file.getvalue())

            # 文字输入回退
            jd_text = jd_file.getvalue().decode("utf-8", errors="replace")
            resume_text = resume_file.getvalue().decode("utf-8", errors="replace")

        progress_bar = st.progress(0, text="初始化...")

        try:
            # 构建图
            progress_bar.progress(10, text="构建工作流图...")
            graph = build_graph()
            progress_bar.progress(20, text="正在分析 JD...")

            # 执行
            initial_state = {
                "jd_text": jd_text,
                "resume_text": resume_text,
                "candidate_name": candidate_name or None,
                "job_type_hint": job_type,
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

            final_state = graph.invoke(initial_state)

            progress_bar.progress(90, text="生成报告...")

            report_path = final_state.get("report_path")

            if report_path and Path(report_path).exists():
                progress_bar.progress(100, text="完成！")
                st.success("✅ 面试准备方案已生成！")

                with open(report_path, "rb") as f:
                    st.download_button(
                        label="📥 下载 HTML 报告",
                        data=f,
                        file_name=Path(report_path).name,
                        mime="text/html",
                        use_container_width=True,
                    )

                # 预览
                with st.expander("预览报告", expanded=True):
                    html_content = Path(report_path).read_text(encoding="utf-8")
                    st.components.v1.html(html_content, height=800, scrolling=True)
            else:
                st.error("报告生成失败，请检查日志")

            # 显示错误
            errors = final_state.get("errors", [])
            if errors:
                with st.expander("执行警告"):
                    for err in errors:
                        st.warning(err)

        except Exception as e:
            st.error(f"生成过程出错: {e}")
            logger.exception("Execution error")
        finally:
            progress_bar.empty()
else:
    st.info("请上传 JD 文件和简历文件后开始生成")

st.divider()
st.caption(
    "AI 面试准备方案生成器 v0.1.0 | "
    "基于 LLM 自动分析，仅供参考，不构成面试承诺。"
)