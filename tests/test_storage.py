"""storage.pyのテスト。"""

import csv
import json

from quote_auto.storage import append_csv, save_json

SAMPLE_DATA = {
    "vendor": "株式会社テスト",
    "date": "2026-04-01",
    "items": [
        {"name": "コンサルティング", "qty": 2, "unit_price": 100000},
    ],
    "total": 200000,
    "currency": "JPY",
}


def test_save_json_creates_file(tmp_path):
    path = save_json(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    assert path.exists()


def test_save_json_contains_source_file(tmp_path):
    path = save_json(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    data = json.loads(path.read_text())
    assert data["source_file"] == "test_quote.pdf"


def test_save_json_contains_extracted_at(tmp_path):
    path = save_json(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    data = json.loads(path.read_text())
    assert "extracted_at" in data


def test_save_json_preserves_vendor(tmp_path):
    path = save_json(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    data = json.loads(path.read_text())
    assert data["vendor"] == "株式会社テスト"


def test_append_csv_creates_file(tmp_path):
    append_csv(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    assert (tmp_path / "items.csv").exists()


def test_append_csv_has_header(tmp_path):
    append_csv(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    with (tmp_path / "items.csv").open() as f:
        reader = csv.reader(f)
        header = next(reader)
    assert "vendor" in header
    assert "name" in header
    assert "unit_price" in header


def test_append_csv_writes_item(tmp_path):
    append_csv(SAMPLE_DATA, "test_quote.pdf", tmp_path)
    with (tmp_path / "items.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["name"] == "コンサルティング"
    assert rows[0]["vendor"] == "株式会社テスト"


def test_append_csv_appends_on_second_call(tmp_path):
    append_csv(SAMPLE_DATA, "quote1.pdf", tmp_path)
    append_csv(SAMPLE_DATA, "quote2.pdf", tmp_path)
    with (tmp_path / "items.csv").open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
