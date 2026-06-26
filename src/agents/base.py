"""Agent 基类与 LLM 调用封装"""

import os
from pathlib import Path
from typing import TypeVar, Type

from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from src.utils.cache import get_cache, set_cache

T = TypeVar("T", bound=BaseModel)

_PROMPT_DIR = Path(__file__).parent / "prompts"

# 默认 LLM 配置
_DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
_DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.3"))


def get_llm(temperature: float | None = None) -> ChatOpenAI:
    """获取 LLM 实例"""
    return ChatOpenAI(
        model=_DEFAULT_MODEL,
        temperature=temperature or _DEFAULT_TEMPERATURE,
    )


def load_prompt(name: str) -> str:
    """加载 System Prompt 文件"""
    path = _PROMPT_DIR / f"{name}.txt"
    return path.read_text(encoding="utf-8")


def run_structured_agent(
    model_class: Type[T],
    prompt_name: str,
    user_message: str,
    use_cache: bool = True,
) -> T:
    """通用的结构化输出 Agent 调用

    Args:
        model_class: Pydantic 模型类
        prompt_name: Prompt 文件名（不含 .txt）
        user_message: 用户消息
        use_cache: 是否使用缓存
    """
    if use_cache:
        cached = get_cache(prompt_name, user_message)
        if cached is not None:
            return model_class.model_validate(cached)

    llm = get_llm()
    structured_llm = llm.with_structured_output(model_class)
    system_prompt = load_prompt(prompt_name)

    result = structured_llm.invoke([
        ("system", system_prompt),
        ("human", user_message),
    ])

    if use_cache:
        try:
            set_cache(prompt_name, result.model_dump(), user_message)
        except Exception:
            pass  # 缓存写入失败不阻塞主流程

    return result