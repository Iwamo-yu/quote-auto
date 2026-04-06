# /extract-quote

> **これはSkillsのサンプルです（学習②）。**
> `.claude/commands/` フォルダにこのようなMarkdownファイルを置くと、
> Claude Codeで `/extract-quote` と打つだけでこの指示が実行されます。
> 毎回長い文章を書かなくて済みます。

---

`quote/` フォルダにある未処理のPDFを全て処理して `saved/` に保存する。

以下の手順で実行すること：

1. `uv run quote-auto process quote/` を実行する
2. 処理件数・保存ファイル名・エラーがあればエラー内容を報告する
3. 完了後、`uv run quote-auto list` で処理済み一覧を表示する
