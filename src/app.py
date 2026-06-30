"""Streamlit Web 界面"""

import os
import tempfile
from pathlib import Path

import streamlit as st

from src.graph.graph_builder import build_graph
from src.utils.logger import setup_logger
from src.utils.llm_config import LLMProvider, PROVIDER_CONFIG
from src.agents.base import set_llm_provider, get_current_provider_info

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

# ============ LLM 配置区域 ============
st.sidebar.header("🤖 LLM 配置")

# 厂商选择
provider_options = {
    "DeepSeek（内置API Key，可直接使用）": LLMProvider.DEEPSEEK,
    "OpenAI": LLMProvider.OPENAI,
    "智谱 GLM": LLMProvider.ZHIPU,
    "阿里云通义": LLMProvider.QWEN,
    "自定义 OpenAI 兼容": LLMProvider.CUSTOM,
}

selected_provider_display = st.sidebar.selectbox(
    "LLM 厂商",
    options=list(provider_options.keys()),
    index=0,  # 默认选择 DeepSeek
    help="DeepSeek 内置API Key，可直接使用；其他厂商需提供API Key",
)

selected_provider = provider_options[selected_provider_display]
provider_config = PROVIDER_CONFIG[selected_provider]

# 显示当前配置信息
if selected_provider == LLMProvider.DEEPSEEK:
    st.sidebar.success(f"✅ {provider_config['name']} - 内置API Key，可直接使用")
    st.sidebar.caption(f"默认模型: {provider_config['default_model']}")
else:
    st.sidebar.info(f"🔑 {provider_config['name']} - 需要提供API Key")
    st.sidebar.caption(f"默认模型: {provider_config['default_model']}")

# API Key 输入（非 DeepSeek 时显示）
api_key = None
base_url = None
model_override = None

if provider_config["needs_user_key"]:
    api_key = st.sidebar.text_input(
        f"{provider_config['name']} API Key",
        type="password",
        help=f"输入你的 {provider_config['name']} API Key",
    )
    
    if selected_provider == LLMProvider.CUSTOM:
        base_url = st.sidebar.text_input(
            "自定义 Base URL",
            placeholder="https://your-api-endpoint.com/v1",
            help="自定义 LLM 服务的 API 地址",
        )

# 模型选择（可选）
available_models = {
    LLMProvider.DEEPSEEK: ["deepseek-chat", "deepseek-coder"],
    LLMProvider.OPENAI: ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
    LLMProvider.ZHIPU: ["glm-4", "glm-4-flash", "glm-3-turbo"],
    LLMProvider.QWEN: ["qwen-plus", "qwen-turbo", "qwen-max"],
    LLMProvider.CUSTOM: [],  # 用户自定义
}

model_options = available_models.get(selected_provider, [])
if model_options:
    model_override = st.sidebar.selectbox(
        "模型选择",
        options=model_options,
        index=0,
        help="可选择不同的模型",
    )
elif selected_provider == LLMProvider.CUSTOM:
    model_override = st.sidebar.text_input(
        "模型名称",
        placeholder="your-model-name",
        help="自定义模型名称",
    )

# 温度参数
temperature = st.sidebar.slider(
    "温度参数",
    min_value=0.0,
    max_value=1.0,
    value=0.3,
    step=0.1,
    help="较低的值生成更确定性的输出，较高的值生成更有创意的输出",
)

# 应用 LLM 配置按钮
if st.sidebar.button("应用 LLM 配置", type="primary"):
    if provider_config["needs_user_key"] and not api_key:
        st.sidebar.error(f"请先输入 {provider_config['name']} API Key")
    elif selected_provider == LLMProvider.CUSTOM and not base_url:
        st.sidebar.error("请输入自定义 Base URL")
    else:
        try:
            config = set_llm_provider(
                provider=selected_provider,
                api_key=api_key,
                base_url=base_url,
                model=model_override,
                temperature=temperature,
            )
            st.sidebar.success(f"✅ 已配置: {config['provider_name']} - {config['model']}")
        except ValueError as e:
            st.sidebar.error(str(e))

# 显示当前配置状态
current_info = get_current_provider_info()
st.sidebar.caption(f"当前: {current_info['provider']} | 模型: {current_info['model']}")
if current_info["has_builtin_key"]:
    st.sidebar.caption("💡 使用内置API Key")

# ============ 面试配置区域 ============
st.sidebar.header("📋 面试配置")

job_type = st.sidebar.selectbox(
    "岗位类型",
    options=["unknown", "tech", "non_tech"],
    format_func=lambda x: {"unknown": "自动识别", "tech": "技术岗位", "non_tech": "非技术岗位"}[x],
    help="选择 '技术岗位' 会生成编码题，'非技术岗位' 跳过编码题",
)

candidate_name = st.sidebar.text_input("候选人姓名（可选）", placeholder="如：张三")

# 用户补充信息（可选）
additional_info = st.sidebar.text_area(
    "补充信息（可选）",
    placeholder="如：面试岗位画像、重点关注的技能方向、已知的面试官偏好等...",
    help="可提供额外的面试背景信息，帮助生成更精准的方案",
)

# ============ 文件上传区域 ============
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

# ============ 生成区域 ============
if jd_file and resume_file:
    if st.button("🚀 生成面试准备方案", type="primary", use_container_width=True):
        # 验证 LLM 配置
        current_info = get_current_provider_info()
        if current_info["provider"] != provider_config["name"]:
            st.error("请先点击 '应用 LLM 配置' 按钮确认配置")
            st.stop()
        
        # 验证 API Key（非 DeepSeek）
        if provider_config["needs_user_key"] and not api_key:
            st.error(f"请先在侧边栏输入 {provider_config['name']} API Key")
            st.stop()
        
        if selected_provider == LLMProvider.CUSTOM and not base_url:
            st.error("请输入自定义 Base URL")
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
                "additional_info": additional_info or None,
                # 各模块输出初始化
                "jd_analysis": None,
                "resume_analysis": None,
                "gap_analysis": None,
                "self_intro": None,
                "project_intro": None,
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
    "AI 面试准备方案生成器 v0.2.0 | "
    "DeepSeek API Key 内置，可直接使用 | "
    "基于 LLM 自动分析，仅供参考，不构成面试承诺。"
)