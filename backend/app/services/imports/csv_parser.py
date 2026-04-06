import csv
from io import StringIO
from typing import Any

from app.schemas.imports import CsvImportRow


def parse_catalog_csv(content: bytes) -> tuple[list[CsvImportRow], list[dict[str, Any]]]:
    text = content.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(text))

    valid_rows: list[CsvImportRow] = []
    errors: list[dict[str, Any]] = []

    for index, row in enumerate(reader, start=2):
        try:
            item = CsvImportRow(**row)
            valid_rows.append(item)
        except Exception as exc:
            errors.append(
                {
                    "row_number": index,
                    "row_data": row,
                    "error": str(exc),
                }
            )

    return valid_rows, errors