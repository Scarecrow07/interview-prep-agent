"""PDF 简历解析"""

import fitz  # PyMuPDF
from pathlib import Path


def parse_pdf(file_path: str | Path) -> str:
    """从 PDF 文件中提取文本"""
    doc = fitz.open(str(file_path))
    text_parts = []
    for page in doc:
        text_parts.append(page.get_text())
    doc.close()
    return "\n".join(text_parts).strip()