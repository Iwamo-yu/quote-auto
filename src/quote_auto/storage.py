"""構造化データをJSON/CSVに保存するモジュール。"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


def save_json(data: dict, source_file: str, saved_dir: Path) -> Path:
    """見積書データをJSONファイルに保存する。"""
    saved_dir.mkdir(parents=True, exist_ok=True)

    stem = Path(source_file).stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = saved_dir / f"{stem}_{timestamp}.json"

    payload = {
        "source_file": source_file,
        "extracted_at": timestamp,
        **data,
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return out_path


def append_csv(data: dict, source_file: str, saved_dir: Path) -> Path:
    """品目データをCSVに追記する（ヘッダーはなければ自動追加）。"""
    saved_dir.mkdir(parents=True, exist_ok=True)
    csv_path = saved_dir / "items.csv"

    fieldnames = ["source_file", "vendor", "date", "currency", "name", "qty", "unit_price", "total"]
    write_header = not csv_path.exists()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()

        for item in data.get("items", []):
            writer.writerow({
                "source_file": source_file,
                "vendor": data.get("vendor", ""),
                "date": data.get("date", ""),
                "currency": data.get("currency", ""),
                "name": item.get("name", ""),
                "qty": item.get("qty", ""),
                "unit_price": item.get("unit_price", ""),
                "total": data.get("total", ""),
            })

    return csv_path
