"""LLM 配置模块 - 支持多厂商 API

DeepSeek API Key 内置（隐码编码），其他厂商需用户提供 API Key。
"""

import os
import base64
from enum import Enum
from typing import Optional


class LLMProvider(Enum):
    """支持的 LLM 厂商"""
    DEEPSEEK = "deepseek"
    OPENAI = "openai"
    ZHIPU = "zhipu"  # 智谱 GLM
    QWEN = "qwen"    # 阿里云通义千问
    CUSTOM = "custom"


# 厂商配置映射
PROVIDER_CONFIG = {
    LLMProvider.DEEPSEEK: {
        "name": "DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
        "needs_user_key": False,  # 内置 API Key
    },
    LLMProvider.OPENAI: {
        "name": "OpenAI",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o",
        "needs_user_key": True,
    },
    LLMProvider.ZHIPU: {
        "name": "智谱 GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4",
        "needs_user_key": True,
    },
    LLMProvider.QWEN: {
        "name": "阿里云通义",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "needs_user_key": True,
    },
    LLMProvider.CUSTOM: {
        "name": "自定义 OpenAI 兼容",
        "base_url": "",  # 用户自定义
        "default_model": "",
        "needs_user_key": True,
    },
}


def _decode_builtin_key(encoded: str) -> str:
    """解码内置的隐码 API Key"""
    # 使用 base64 反向编码 + 字符位移
    shifted = base64.b64decode(encoded).decode('utf-8')
    # 字符位移还原（每个字符 ASCII -1）
    return ''.join(chr(ord(c) - 1) for c in shifted)


def _encode_for_storage(key: str) -> str:
    """编码存储（仅用于开发时生成隐码）"""
    # 字符位移（每个字符 ASCII +1）
    shifted = ''.join(chr(ord(c) + 1) for c in key)
    return base64.b64encode(shifted.encode('utf-8')).decode('utf-8')


# DeepSeek 内置 API Key（隐码存储，用户可直接使用）
_DEEPSEEK_KEY_ENCODED = "dGwuZWU6N2RnOTliM2JiNTI6YzpjZTU6MmU0NmcyZjg4OjI="


def get_builtin_deepseek_key() -> str:
    """获取内置的 DeepSeek API Key"""
    return _decode_builtin_key(_DEEPSEEK_KEY_ENCODED)


def get_llm_config(
    provider: LLMProvider = LLMProvider.DEEPSEEK,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
) -> dict:
    """获取 LLM 配置
    
    Args:
        provider: LLM 厂商
        api_key: 用户提供的 API Key（DeepSeek 可不提供，使用内置）
        base_url: 自定义 base URL（仅 CUSTOM 厂商需要）
        model: 自定义模型名称
        
    Returns:
        配置字典，包含 base_url, api_key, model
    """
    config = PROVIDER_CONFIG[provider]
    
    # 处理 API Key
    if provider == LLMProvider.DEEPSEEK:
        # DeepSeek 使用内置 Key，用户提供的 key 优先
        final_key = api_key or get_builtin_deepseek_key()
    else:
        # 其他厂商必须用户提供
        final_key = api_key or os.getenv(f"{provider.value.upper()}_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not final_key:
            raise ValueError(f"{config['name']} 需要提供 API Key")
    
    # 处理 base_url
    if provider == LLMProvider.CUSTOM:
        final_base_url = base_url or os.getenv("CUSTOM_LLM_BASE_URL")
        if not final_base_url:
            raise ValueError("自定义厂商需要提供 base_url")
    else:
        final_base_url = config["base_url"]
    
    # 处理 model
    final_model = model or os.getenv("LLM_MODEL") or config["default_model"]
    
    return {
        "provider": provider.value,
        "provider_name": config["name"],
        "base_url": final_base_url,
        "api_key": final_key,
        "model": final_model,
    }


def setup_environment(config: dict) -> None:
    """设置环境变量供 langchain-openai 使用"""
    os.environ["OPENAI_API_KEY"] = config["api_key"]
    os.environ["OPENAI_API_BASE"] = config["base_url"]
    os.environ["LLM_MODEL"] = config["model"]


# 开发工具：生成新的隐码（仅开发时使用）
if __name__ == "__main__":
    # 示例：生成新的隐码
    test_key = "sk-your-new-key-here"
    encoded = _encode_for_storage(test_key)
    print(f"Encoded: {encoded}")
    print(f"Decoded: {_decode_builtin_key(encoded)}")