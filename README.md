# quote-auto — Claude Code ハンズオン教材

> **このリポジトリは、Claude Code の主要概念を実践的に学ぶためのハンズオン教材です。**
>
> 「見積書PDFの自動データ抽出」という実用的なテーマを題材に、Claude Code を使った開発ワークフローの5つの重要概念を体験しながら習得できます。

## 🎯 この教材で学べること

本教材には **5つの Exercise** が用意されており、それぞれ「まず困る → 解決策を使う → なぜ必要かを理解する」の3ステップで構成されています。

| Exercise | 概念 | 学べること |
|---|---|---|
| 1 | **CLAUDE.md** | プロジェクトの永続的な記憶を与える方法 |
| 2 | **Skills** | よく使う指示をスラッシュコマンドとして固定化する方法 |
| 3 | **Spec-driven** | 仕様書を先に書き、Claudeの解釈のブレを防ぐ方法 |
| 4 | **Harness** | テストを用いてClaude に自律的な検証をさせる方法 |
| 5 | **Coworks** | Claude Code と Claude.ai の使い分けの原則 |

詳しい演習内容は [`EXERCISES.md`](./EXERCISES.md) を参照してください。

## 📦 題材プロジェクトの概要

見積書（PDF）を読み取り、Claude API で構造化データ（JSON/CSV）に自動変換する CLI ツールです。

```
quote/          ← 処理する PDF を配置
saved/          ← 抽出結果の JSON・CSV が出力される
src/quote_auto/
  extractor.py  — pdfplumber で PDF からテキスト抽出
  parser.py     — Claude API で構造化データに変換
  storage.py    — JSON/CSV 保存
  cli.py        — CLI エントリポイント
tests/          ← pytest テスト群
```

## 🚀 セットアップ

### 必要条件

- Python 3.11 以上
- [uv](https://github.com/astral-sh/uv)（高速な Python パッケージマネージャー）
- [Anthropic API Key](https://console.anthropic.com/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview)（演習の実行に必要）

### インストール

```bash
# 1. リポジトリをクローン
git clone https://github.com/Iwamo-yu/quote-auto.git
cd quote-auto

# 2. 依存関係をインストール
uv sync --extra dev

# 3. 環境変数を設定
cp .env.example .env
# .env を編集して ANTHROPIC_API_KEY=sk-ant-... を設定
```

## 💻 使い方

```bash
# フォルダ内の全 PDF を処理
uv run quote-auto process quote/

# 特定のファイルを 1 つだけ処理
uv run quote-auto process quote/sample.pdf

# 処理済みデータの一覧を確認
uv run quote-auto list

# テストを実行
uv run pytest
```

## 📂 出力フォーマット

| 形式 | パス | 説明 |
|---|---|---|
| JSON | `saved/{stem}_{timestamp}.json` | ファイルごとの詳細な抽出結果 |
| CSV | `saved/items.csv` | 全見積書の品目データ（追記式） |

## 📝 関連ファイル

| ファイル | 役割 |
|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | Claude Code が自動で読むプロジェクトの説明書（Exercise 1 の題材） |
| [`EXERCISES.md`](./EXERCISES.md) | 5つの演習の詳細な手順書 |
| [`spec.md`](./spec.md) | Spec-driven 開発の仕様書（Exercise 3 の題材） |
| `.claude/commands/` | Skills のスラッシュコマンド（Exercise 2 の題材） |

## ライセンス

[MIT](./LICENSE)
