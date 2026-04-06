# Claude Code 練習問題 — quote-auto で学ぶ5つの概念

このファイルはClaude Codeの主要概念を「このプロジェクトを使って体験する」ための練習帳です。
**各課題は「まず困る→解決策を使う→なぜ必要かを理解する」の3ステップ構成**です。

---

## Exercise 1 — なぜ CLAUDE.md が必要か？

### CLAUDE.mdとは？
Claude Codeがプロジェクトを開くたびに**自動で読む「プロジェクトの説明書」**。
Claudeは会話をまたいで記憶しないため、CLAUDE.mdだけが「毎回確実に渡される文脈」になります。

### 体験してみよう

**STEP 1（困る）:** CLAUDE.md を一時的に別名にリネームする
```bash
mv CLAUDE.md CLAUDE.md.bak
```
→ Claude Codeで「このプロジェクトの出力フォルダはどこですか？」と聞く
→ Claudeはsaved/の存在を知らずに推測で答える、または聞き返す

**STEP 2（解決）:** 元に戻して同じ質問をする
```bash
mv CLAUDE.md.bak CLAUDE.md
```
→ Claudeは即座に「saved/フォルダです」と答える

**STEP 3（理解）:** なぜ？
> CLAUDE.mdがなければClaudeは毎回ゼロから文脈を推測する。
> あれば、プロジェクトのルール・構造・コマンドを即座に知っている。

### 課題
CLAUDE.mdの「規約」セクションに以下を追記してみよう:
```
- このプロジェクトではJSONのみ使用する。CSVは禁止。
```
追記後、Claude Codeで「出力形式は何が使えますか？」と聞いて回答の変化を確認せよ。

---

## Exercise 2 — なぜ Skills が必要か？

### Skillsとは？
`.claude/commands/` フォルダにMarkdownファイルを置くと、
`/ファイル名` で呼び出せる**自作コマンド（スラッシュコマンド）**。
よく使う長い指示を1行のコマンドに圧縮できる。

### 体験してみよう

**STEP 1（困る）:** Skillsなしで毎回手で頼む
```
「quote/フォルダにある未処理のPDFを全部読み取って、
  Claude APIで構造化して、saved/にJSONで保存して、
  何件処理したか教えて」← 毎回これを書く
```
→ 表現がブレると動作も微妙にブレる

**STEP 2（解決）:** `/extract-quote` と打つだけ
→ `.claude/commands/extract-quote.md` の内容が自動実行される

**STEP 3（理解）:** なぜ？
> 同じ指示を毎回書くと①時間がかかる②表現がブレてClaudeの動作が安定しない。
> Skillsは「指示のテンプレート固定化」。チームで共有すれば全員の操作が統一される。

### 課題
`.claude/commands/check-saved.md` を自分で作り、
`/check-saved` で「saved/フォルダに何件のJSONがあるか」を報告させよ。

ヒント: `.claude/commands/extract-quote.md` を参考にしてMarkdownを書けばOK。

---

## Exercise 3 — なぜ Spec-driven が必要か？

### Spec-drivenとは？
実装前に**仕様書（spec.md）を書き、Claudeに「spec.mdに従って」と指示する**開発スタイル。
specがあると、Claudeは毎回同じ解釈で実装する。

### 体験してみよう

**STEP 1（困る）:** specなしでClaudeに頼む
```
「見積書PDFからデータを取り出す機能に複数通貨対応を追加して」
```
→ Claudeが独自に判断した形で実装される（フィールド名・エラー処理・対応通貨が毎回違う）

**STEP 2（解決）:** spec.mdを先に書いてから頼む
```
「spec.mdの通貨対応の仕様に従って実装して」
```
→ specに書いた通りの実装になる

**STEP 3（理解）:** なぜ？
> Claudeは文脈がなければ「それっぽい」実装をする。
> specは「Claudeが判断を間違えられない制約」。
> 実装前に書くことで手戻りをゼロにする。

### 課題
`spec.md` の「通貨対応」を以下に書き換えよ:
```
- 対応通貨: JPY / USD のみ
- それ以外はValueErrorを送出してスキップ
```
書き換え後、Claude Codeで「spec.mdに従って通貨バリデーションを実装して」と頼んでみよ。
specありとなしで実装がどう変わるか比べよ。

---

## Exercise 4 — なぜ Harness が必要か？

### Harnessとは？
**テスト + 実行環境**の組み合わせ。
これがあるとClaudeが「自分の実装が正しいか」を自律的に検証できる。

### 体験してみよう

**STEP 1（困る）:** テストなしでClaudeに修正を頼む
```
「parser.pyのバグを直して」
```
→ Claudeが直す → 「直りました」と言う
→ 本当に直ったか確認するのは自分 ← 毎回これ

**STEP 2（解決）:** テストがある状態で頼む
```
「テストを全部passさせて」
```
→ Claudeが `uv run pytest` を自分で実行
→ 失敗したら原因を調べて再修正 → passするまで繰り返す
→ 人間は最後の結果だけ確認すればいい

**STEP 3（理解）:** なぜ？
> Harnessとは「Claudeが自律的に正誤判定できる仕組み」。
> テストがあればClaudeは自己検証できる。
> なければClaudeは「たぶん動く」と言うしかない。

### 課題
`tests/test_parser.py` に**意図的に失敗するテスト**を1つ追加しよう:
```python
def test_parse_quote_currency_is_valid():
    # このテストは最初失敗する — Claudeに直させよ
    mock_client = _make_mock_response({**SAMPLE_RESPONSE, "currency": "EUR"})
    with patch("quote_auto.parser.anthropic.Anthropic", return_value=mock_client):
        with pytest.raises(ValueError):
            parse_quote("見積書テキスト")
```
追加後、Claude Codeで「`uv run pytest` を全部passさせて」とだけ頼む。
Claudeが自走して修正するか観察せよ。

---

## Exercise 5 — なぜ Coworks の使い分けが必要か？

### Coworksとは？
Claude Codeと Claude.ai（ブラウザチャット）を**得意不得意で使い分ける**こと。

| | Claude Code | Claude.ai |
|---|---|---|
| **得意** | ファイル編集・コマンド実行・テスト | 設計相談・ドキュメント読解・アイデア出し |
| **CLAUDE.mdを読む** | ✓ 自動で読む | ✗ 読まない |
| **ファイルを直接触れる** | ✓ | ✗（コピペが必要） |
| **向いている操作** | 実装・修正・リファクタ | 相談・レビュー・学習 |

### 体験してみよう

**STEP 1（困る）:** 間違った使い方をする
```
× Claude.aiのチャットで「parser.pyのバグを直して」と頼む
  → コードを貼り付けてくる → 自分でコピペが必要 → ミスが起きやすい

× Claude Codeに「このプロジェクトの設計をどう思う？」と相談する
  → Claudeがいきなりファイルを編集し始めることがある
```

**STEP 2（解決）:** 使い分けの原則
```
✓ ファイル操作・コマンド実行・テスト実行 → Claude Code
✓ 設計相談・ドキュメント理解・アイデア出し → Claude.ai
```

**STEP 3（理解）:** なぜ？
> Claude CodeはCLAUDE.mdを読み、ファイルを直接触れる。
> Claude.aiはブラウザ上の汎用チャット。
> 「道具の得意不得意」を知ることで作業速度が変わる。

### 課題
以下の2つをそれぞれ**適切な方**に頼み、体験を比較せよ:

A. 「parser.pyにエラーログを追加して」
   → どちらに頼むべきか？ → **Claude Code**（ファイルを直接編集できるから）

B. 「このプロジェクトのアーキテクチャで改善できる点は？」
   → どちらに頼むべきか？ → **Claude.ai**（コードを書かずに議論したいから）

---

## まとめ

| 概念 | 一言で言うと | ないと困ること |
|---|---|---|
| **CLAUDE.md** | プロジェクトの永続記憶 | 毎回文脈を説明し直す |
| **Skills** | 指示のテンプレート固定化 | 毎回長い指示を書く、表現がブレる |
| **Spec-driven** | 実装前の制約書き | Claudeが毎回違う解釈をする |
| **Harness** | 自律的な正誤判定機構 | 人間が毎回動作確認する |
| **Coworks** | 道具の使い分け | 間違った道具で非効率になる |
