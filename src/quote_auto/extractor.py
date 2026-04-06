"""PDF見積書からテキストを抽出するモジュール。"""

import re
from pathlib import Path

import pdfplumber


def extract_text(pdf_path: Path) -> str:
    """PDFファイルからテキストを抽出して返す。"""
    with pdfplumber.open(pdf_path) as pdf:
        pages = [page.extract_text() or "" for page in pdf.pages]
    raw = "\n".join(pages)
    return _normalize(raw)


def _normalize(text: str) -> str:
    """余分な空白・改行を整理する。"""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
