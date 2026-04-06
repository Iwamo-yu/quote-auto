"""quote-auto CLI — 見積書PDFを処理するコマンドラインツール。"""

import json
from pathlib import Path

import typer

from quote_auto.extractor import extract_text
from quote_auto.parser import parse_quote
from quote_auto.storage import append_csv, save_json

app = typer.Typer(help="見積書PDFを読み取ってJSON/CSVデータベースを作成するツール")

SAVED_DIR = Path("saved")


@app.command()
def process(
    target: Path = typer.Argument(..., help="PDFファイル or PDFが入ったフォルダ"),
):
    """見積書PDFを処理してsaved/に保存する。"""
    pdf_files: list[Path] = []

    if target.is_dir():
        pdf_files = sorted(target.glob("*.pdf"))
        if not pdf_files:
            typer.echo(f"[!] {target} にPDFが見つかりません")
            raise typer.Exit(1)
    elif target.is_file() and target.suffix.lower() == ".pdf":
        pdf_files = [target]
    else:
        typer.echo(f"[!] {target} はPDFファイルまたはフォルダではありません")
        raise typer.Exit(1)

    typer.echo(f"処理対象: {len(pdf_files)} 件")

    for pdf in pdf_files:
        typer.echo(f"  → {pdf.name} を処理中...")
        try:
            text = extract_text(pdf)
            data = parse_quote(text)
            json_path = save_json(data, pdf.name, SAVED_DIR)
            append_csv(data, pdf.name, SAVED_DIR)
            typer.echo(f"     保存完了: {json_path.name}")
        except Exception as e:
            typer.echo(f"     [ERROR] {e}")

    typer.echo("完了。")


@app.command()
def list():
    """saved/フォルダの処理済みファイル一覧を表示する。"""
    json_files = sorted(SAVED_DIR.glob("*.json"))
    if not json_files:
        typer.echo("saved/ に処理済みファイルがありません。")
        return

    typer.echo(f"処理済み: {len(json_files)} 件\n")
    for f in json_files:
        data = json.loads(f.read_text())
        typer.echo(
            f"  {f.name}\n"
            f"    vendor: {data.get('vendor', '?')}\n"
            f"    date:   {data.get('date', '?')}\n"
            f"    total:  {data.get('total', '?')} {data.get('currency', '')}\n"
        )
