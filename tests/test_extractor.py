"""extractor.pyのテスト。"""

from pathlib import Path
from unittest.mock import MagicMock, patch

from quote_auto.extractor import _normalize, extract_text


def test_normalize_removes_extra_spaces():
    assert _normalize("foo   bar") == "foo bar"


def test_normalize_collapses_blank_lines():
    text = "line1\n\n\n\nline2"
    result = _normalize(text)
    assert "\n\n\n" not in result
    assert "line1" in result
    assert "line2" in result


def test_normalize_strips():
    assert _normalize("  hello  ") == "hello"


def test_extract_text_returns_string(tmp_path):
    """extract_textがPDFから文字列を返すことを確認（pdfplumberをモック）。"""
    dummy_pdf = tmp_path / "test.pdf"
    dummy_pdf.write_bytes(b"%PDF-1.4 fake")  # pdfplumberが開くだけ

    mock_page = MagicMock()
    mock_page.extract_text.return_value = "サンプル 見積書"

    mock_pdf = MagicMock()
    mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
    mock_pdf.__exit__ = MagicMock(return_value=False)
    mock_pdf.pages = [mock_page]

    with patch("quote_auto.extractor.pdfplumber.open", return_value=mock_pdf):
        result = extract_text(dummy_pdf)

    assert "サンプル" in result
    assert "見積書" in result
