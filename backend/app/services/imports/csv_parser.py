import csv
from io import StringIO
from typing import Any

from app.schemas.imports import CatalogImportRow


REQUIRED_COLUMNS = {
    "display_name",
    "infrastructure",
    "lighting",
    "noise",
    "insolation",
    "development",
}


def _build_reader(text: str) -> csv.DictReader:
    sample = text[:4096]

    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        return csv.DictReader(StringIO(text), dialect=dialect)
    except Exception:
        return csv.DictReader(StringIO(text), delimiter=",")


def _normalize_csv_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}

    for key, value in row.items():
        clean_key = (key or "").strip()
        clean_value = value.strip() if isinstance(value, str) else value
        normalized[clean_key] = clean_value

    return normalized


def parse_catalog_csv(
    content: bytes,
) -> tuple[list[tuple[int, CatalogImportRow]], list[dict[str, Any]]]:
    text = content.decode("utf-8-sig")
    reader = _build_reader(text)

    if not reader.fieldnames:
        return [], [
            {
                "row_number": 1,
                "row_data": {},
                "error": "CSV header is missing",
            }
        ]

    fieldnames = [f.strip() for f in reader.fieldnames if f]
    missing_columns = sorted(REQUIRED_COLUMNS - set(fieldnames))
    if missing_columns:
        return [], [
            {
                "row_number": 1,
                "row_data": {"headers": fieldnames},
                "error": f"Missing required columns: {', '.join(missing_columns)}",
            }
        ]

    valid_rows: list[tuple[int, CatalogImportRow]] = []
    errors: list[dict[str, Any]] = []

    for index, raw_row in enumerate(reader, start=2):
        row = _normalize_csv_row(raw_row)

        if not any(value not in (None, "") for value in row.values()):
            continue

        try:
            item = CatalogImportRow(**row)
            valid_rows.append((index, item))
        except Exception as exc:
            errors.append(
                {
                    "row_number": index,
                    "row_data": row,
                    "error": str(exc),
                }
            )

    return valid_rows, errors