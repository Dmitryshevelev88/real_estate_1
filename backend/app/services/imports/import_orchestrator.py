from typing import Any

from sqlalchemy.orm import Session

from app.models.import_batch import ImportBatch
from app.services.imports.analytics_versioning import create_analytics_version
from app.services.imports.batch_service import (
    mark_batch_done,
    mark_batch_failed,
    mark_batch_processing,
)
from app.services.imports.catalog_upsert import upsert_catalog_property
from app.services.imports.csv_parser import parse_catalog_csv


def run_catalog_csv_import(
    db: Session,
    batch: ImportBatch,
    content: bytes,
) -> dict[str, Any]:
    try:
        rows, parse_errors = parse_catalog_csv(content)

        mark_batch_processing(db, batch, rows_total=len(rows) + len(parse_errors))

        rows_created = 0
        rows_updated = 0
        row_errors: list[dict[str, Any]] = list(parse_errors)

        for row_number, row in rows:
            try:
                item, created = upsert_catalog_property(db, row)
                create_analytics_version(db, item.id, row)

                if created:
                    rows_created += 1
                else:
                    rows_updated += 1

                db.commit()
            except Exception as exc:
                db.rollback()
                row_errors.append(
                    {
                        "row_number": row_number,
                        "row_data": row.model_dump(),
                        "error": str(exc),
                    }
                )

        mark_batch_done(
            db,
            batch,
            rows_created=rows_created,
            rows_updated=rows_updated,
            rows_failed=len(row_errors),
        )

        return {
            "batch_id": batch.id,
            "status": batch.status,
            "rows_total": batch.rows_total,
            "rows_created": batch.rows_created,
            "rows_updated": batch.rows_updated,
            "rows_failed": batch.rows_failed,
            "errors": row_errors,
        }
    except Exception as exc:
        db.rollback()
        mark_batch_failed(db, batch, str(exc))
        raise