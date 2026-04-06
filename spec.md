# Spec: quote-auto 見積書抽出仕様

> **このファイルはspec.mdです（Spec-driven開発の仕様書）。**
> 実装前にここに「何を作るか」を書き、Claudeに「spec.mdに従って実装して」と指示する。
> specがあると、Claudeは毎回同じ解釈で実装する。
> → Exercise 3で「specあり/なし」の違いを体験してください。

---

## 機能要件

### 1. PDF読み取り

- `quote/` フォルダ内の `.pdf` ファイルを対象とする
- 1ファイル指定での処理もサポートする
- テキストが抽出できないページ（画像PDF等）は空文字として扱い、処理を続行する

### 2. データ抽出

Claude API（claude-haiku-4-5-20251001）を使い、以下のフィールドを抽出する：

| フィールド | 型 | 説明 |
|---|---|---|
| `vendor` | string | 発行会社名（必須） |
| `date` | string \| null | 見積日（YYYY-MM-DD形式、不明はnull） |
| `items` | array | 品目リスト（必須、最低1件） |
| `items[].name` | string | 品目名 |
| `items[].qty` | number | 数量 |
| `items[].unit_price` | number | 単価（税別） |
| `total` | number | 合計金額（税別） |
| `currency` | string | 通貨コード |

### 3. 通貨対応

- 対応通貨: `JPY` / `USD` のみ
- それ以外の通貨が検出された場合: `ValueError` を送出し、該当ファイルをスキップする
- CLIは他のファイルの処理を続行する

### 4. 保存形式

**JSON** (`saved/{stem}_{timestamp}.json`)
- `extracted_at` フィールドをUTC ISO形式（`20260401T120000Z`）で付与する
- `source_file` フィールドにPDFファイル名を記録する

**CSV** (`saved/items.csv`)
- 品目単位で1行ずつ追記する（追記モード）
- ヘッダーが存在しない場合のみヘッダーを書き込む
- 列: `source_file, vendor, date, currency, name, qty, unit_price, total`

### 5. CLI

```
quote-auto process <path>   # フォルダ or 1ファイルを処理
quote-auto list             # saved/の処理済み一覧を表示
```

## 非機能要件

- `ANTHROPIC_API_KEY` は `.env` から読み込む（環境変数直打ちも可）
- テストはClaude API・pdfplumberをモックし、実際のAPI呼び出しは行わない
- Python 3.11以上

## エラー処理

| ケース | 挙動 |
|---|---|
| PDFにテキストなし | 空文字で処理継続 |
| 未対応通貨 | スキップ + エラーメッセージ出力 |
| JSONパース失敗 | スキップ + エラーメッセージ出力 |
| ANTHROPIC_API_KEY未設定 | KeyError で即時終了 |
