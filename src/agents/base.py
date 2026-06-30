"""Agent 基类与 LLM 调用封装"""

import os
from pathlib import Path
from typing import TypeVar, Type, Optional

from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from src.utils.cache import get_cache, set_cache
from src.utils.llm_config import LLMProvider, get_llm_config, setup_environment

T = TypeVar("T", bound=BaseModel)

_PROMPT_DIR = Path(__file__).parent / "prompts"

# 全局 LLM 配置（可通过 set_llm_provider 更新）
_current_provider: LLMProvider = LLMProvider.DEEPSEEK
_current_api_key: Optional[str] = None
_current_base_url: Optional[str] = None
_current_model: Optional[str] = None
_default_temperature: float = 0.3


def set_llm_provider(
    provider: LLMProvider,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
) -> dict:
    """设置全局 LLM 配置
    
    Args:
        provider: LLM 厂商
        api_key: API Key（DeepSeek 可不提供）
        base_url: 自定义 base URL
        model: 模型名称
        temperature: 温度参数
        
    Returns:
        当前配置字典
    """
    global _current_provider, _current_api_key, _current_base_url, _current_model, _default_temperature
    
    _current_provider = provider
    _current_api_key = api_key
    _current_base_url = base_url
    _current_model = model
    if temperature is not None:
        _default_temperature = temperature
    
    config = get_llm_config(provider, api_key, base_url, model)
    setup_environment(config)
    
    return config


def get_llm(temperature: Optional[float] = None) -> ChatOpenAI:
    """获取 LLM 实例（使用当前配置）"""
    config = get_llm_config(
        provider=_current_provider,
        api_key=_current_api_key,
        base_url=_current_base_url,
        model=_current_model,
    )
    
    return ChatOpenAI(
        model=config["model"],
        temperature=temperature or _default_temperature,
        api_key=config["api_key"],
        base_url=config["base_url"],
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


def get_current_provider_info() -> dict:
    """获取当前 LLM 配置信息（用于界面显示）"""
    config = get_llm_config(
        provider=_current_provider,
        api_key=_current_api_key,
        base_url=_current_base_url,
        model=_current_model,
    )
    return {
        "provider": config["provider_name"],
        "model": config["model"],
        "has_builtin_key": _current_provider == LLMProvider.DEEPSEEK and _current_api_key is None,
    }