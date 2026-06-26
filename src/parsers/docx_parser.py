"""Word (.docx) 简历解析"""

import docx
from pathlib import Path


def parse_docx(file_path: str | Path) -> str:
    """从 .docx 文件中提取文本"""
    doc = docx.Document(str(file_path))
    text_parts = []
    for paragraph in doc.paragraphs:
        text_parts.append(paragraph.text)
    return "\n".join(text_parts).strip()