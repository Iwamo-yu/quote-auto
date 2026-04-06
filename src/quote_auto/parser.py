"""Claude APIを使って見積書テキストを構造化データに変換するモジュール。"""

import json
import os
import re

import anthropic
from dotenv import load_dotenv

load_dotenv()

# 抽出するJSONのスキーマ定義
_SCHEMA = {
    "vendor": "str — 発行会社名",
    "date": "str — 見積日 (YYYY-MM-DD形式、不明な場合はnull)",
    "items": [
        {
            "name": "str — 品目名",
            "qty": "number — 数量",
            "unit_price": "number — 単価",
        }
    ],
    "total": "number — 合計金額",
    "currency": "str — 通貨コード (JPY / USD)",
}

_PROMPT_TEMPLATE = """\
以下は見積書のテキストです。
内容を解析し、指定のJSONスキーマに従って構造化データを返してください。
JSONのみを返し、説明文は不要です。

## スキーマ
{schema}

## 見積書テキスト
{text}
"""


def parse_quote(text: str) -> dict:
    """見積書テキストをClaude APIで解析し、構造化dictを返す。"""
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    prompt = _PROMPT_TEMPLATE.format(
        schema=json.dumps(_SCHEMA, ensure_ascii=False, indent=2),
        text=text,
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = message.content[0].text.strip()
    # コードブロックで囲まれていた場合に除去
    if raw.startswith("```"):
        raw = re.sub(r"^```[a-z]*\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw)

    return json.loads(raw)
