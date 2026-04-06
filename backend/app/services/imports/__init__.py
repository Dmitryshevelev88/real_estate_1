import csv
import io
from dataclasses import dataclass

from pydantic import ValidationError

from app.schemas.imports import CsvImportRow


REQUIRED_COLUMNS = {
    "external_id",
    "display_name",
    "infrastructure",
    "lighting",
    "noise",
    "insolation",
    "development",
}


@dataclass
class ParsedImportRow:
    line_no: int
    row: CsvImportRow


def parse_csv_rows(content: bytes) -> tuple[list[ParsedImportRow], list[str]]:
    if not content:
        raise ValueError("CSV file is empty")

    text = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames:
        raise ValueError("CSV header is missing")

    fieldnames = [name.strip() for name in reader.fieldnames]
    missing = sorted(REQUIRED_COLUMNS - set(fieldnames))
    if missing:
        raise ValueError(f"Missing CSV columns: {', '.join(missing)}")

    parsed_rows: list[ParsedImportRow] = []
    errors: list[str] = []

    for line_no, raw in enumerate(reader, start=2):
        normalized = {
            (key.strip() if isinstance(key, str) else key): (
                value.strip() if isinstance(value, str) else value
            )
            for key, value in raw.items()
        }

        if not any(normalized.values()):
            continue

        try:
            row = CsvImportRow.model_validate(normalized)
            parsed_rows.append(ParsedImportRow(line_no=line_no, row=row))
        except ValidationError as exc:
            first_error = exc.errors()[0]
            errors.append(f"row {line_no}: {first_error['msg']}")

    return parsed_rows, errors