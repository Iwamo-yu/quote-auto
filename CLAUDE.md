# quote-auto

> **このファイルはCLAUDE.mdです。**
> Claude Codeはプロジェクトを開くたびにこのファイルを自動で読みます。
> ここに書いたことがClaudeの「プロジェクトの記憶」になります。
> → Exercise 1で「このファイルを削除するとどうなるか」を試してみてください。

---

## プロジェクト概要

見積書（vendor quote）のPDFを自動で読み取り、品目・金額・取引先などを
JSON/CSVデータベースに変換するツール。

## フォルダ構成

```
quote/      ← 処理するPDFをここに入れる
saved/      ← 処理結果のJSON・CSVが出力される
src/quote_auto/
  extractor.py  — pdfplumberでPDFからテキスト抽出
  parser.py     — Claude APIで構造化データに変換
  storage.py    — JSON/CSV保存
  cli.py        — CLIエントリポイント
tests/      ← pytestテスト群
```

## コマンド

```bash
# 依存インストール
uv sync --extra dev

# フォルダ内の全PDFを処理
uv run quote-auto process quote/

# 1ファイルだけ処理
uv run quote-auto process quote/foo.pdf

# 処理済みファイル一覧
uv run quote-auto list

# テスト実行
uv run pytest
```

## 環境変数

`.env` ファイルに記載（`.env.example` を参照）:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## 出力フォーマット

### JSON (saved/{filename}_{timestamp}.json)
```json
{
  "source_file": "quote_sample.pdf",
  "extracted_at": "20260401T120000Z",
  "vendor": "株式会社サンプル",
  "date": "2026-04-01",
  "items": [
    {"name": "Webサイト制作", "qty": 1, "unit_price": 500000}
  ],
  "total": 500000,
  "currency": "JPY"
}
```

### CSV (saved/items.csv)
`source_file, vendor, date, currency, name, qty, unit_price, total` の列構成。

## 規約

- 出力はJSON（saved/*.json）とCSV（saved/items.csv）の両方を生成する
- 通貨コードはJPYまたはUSDのみ対応
- 日付フォーマットはYYYY-MM-DD
- テストはモックを使い、実際のAPI呼び出しは行わない
