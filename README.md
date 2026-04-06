# quote-auto

見積書（PDF）からデータを自動抽出し、構造化データ（JSON/CSV）に変換するツールです。

## 特徴

- **PDF抽出**: `pdfplumber` を使用して、PDFから正確にテキストを抽出します。
- **インテリジェントなパース**: Claude API (`claude-3-5-sonnet` 等) を使用して、非定型な見積書から発行元、日付、品目リスト、金額、通貨などを高精度に抽出します。
- **マルチ出力**: 処理結果を各ファイルごとの JSON と、集計用の `items.csv` の両方に出力します。
- **CLIインターフェース**: シンプルなコマンドでフォルダ単位またはファイル単位の処理が可能です。

## 必要条件

- Python 3.11以上
- [uv](https://github.com/astral-sh/uv) (高速なPythonパッケージマネージャー)
- Anthropic API Key

## セットアップ

1.  レポジトリをクローンまたはダウンロードします。
2.  依存関係をインストールします。

    ```bash
    uv sync
    ```

3.  環境変数を設定します。`.env.example` を `.env` にコピーし、APIキーを記入してください。

    ```bash
    cp .env.example .env
    # .env を編集して ANTHROPIC_API_KEY=sk-ant-... を設定
    ```

## 使い方

### 1. 見積書の配置
`quote/` フォルダの中に、解析したいPDFファイルを配置します。

### 2. 実行

**フォルダ内の全PDFを処理する:**
```bash
uv run quote-auto process quote/
```

**特定のファイルを1つだけ処理する:**
```bash
uv run quote-auto process quote/sample.pdf
```

**処理済みデータの一覧を確認する:**
```bash
uv run quote-auto list
```

## 出力フォーマット

### JSON
`saved/{ファイル名}_{タイムスタンプ}.json` に詳細な抽出結果が保存されます。

### CSV
`saved/items.csv` に、すべての見積書の品目データが1行ずつ追記されます。

## 開発・テスト

テストを実行するには以下のコマンドを使用します：

```bash
uv run pytest
```

## ライセンス

MIT (または任意のライセンスを指定してください)
