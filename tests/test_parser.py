"""parser.pyのテスト。Claude APIはモックで代替する。"""

import json
from unittest.mock import MagicMock, patch

import pytest

from quote_auto.parser import parse_quote


def _make_mock_response(payload: dict) -> MagicMock:
    """anthropic.Anthropicのレスポンスをモックする。"""
    content_block = MagicMock()
    content_block.text = json.dumps(payload)

    message = MagicMock()
    message.content = [content_block]

    client = MagicMock()
    client.messages.create.return_value = message
    return client


SAMPLE_RESPONSE = {
    "vendor": "株式会社サンプル商事",
    "date": "2026-04-01",
    "items": [
        {"name": "Webサイト制作", "qty": 1, "unit_price": 500000},
        {"name": "サーバー設定", "qty": 1, "unit_price": 80000},
    ],
    "total": 580000,
    "currency": "JPY",
}


def test_parse_quote_returns_dict():
    mock_client = _make_mock_response(SAMPLE_RESPONSE)

    with patch("quote_auto.parser.anthropic.Anthropic", return_value=mock_client):
        result = parse_quote("見積書テキスト")

    assert isinstance(result, dict)


def test_parse_quote_has_required_keys():
    mock_client = _make_mock_response(SAMPLE_RESPONSE)

    with patch("quote_auto.parser.anthropic.Anthropic", return_value=mock_client):
        result = parse_quote("見積書テキスト")

    for key in ("vendor", "date", "items", "total", "currency"):
        assert key in result, f"キー '{key}' が結果に含まれていない"


def test_parse_quote_items_is_list():
    mock_client = _make_mock_response(SAMPLE_RESPONSE)

    with patch("quote_auto.parser.anthropic.Anthropic", return_value=mock_client):
        result = parse_quote("見積書テキスト")

    assert isinstance(result["items"], list)
    assert len(result["items"]) > 0


def test_parse_quote_strips_code_block():
    """```json ... ``` で囲まれた応答でもパースできることを確認。"""
    wrapped = "```json\n" + json.dumps(SAMPLE_RESPONSE) + "\n```"

    content_block = MagicMock()
    content_block.text = wrapped
    message = MagicMock()
    message.content = [content_block]
    client = MagicMock()
    client.messages.create.return_value = message

    with patch("quote_auto.parser.anthropic.Anthropic", return_value=client):
        result = parse_quote("見積書テキスト")

    assert result["vendor"] == "株式会社サンプル商事"
