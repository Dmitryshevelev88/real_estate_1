from typing import Any

from app.models.import_batch import ImportBatch


def start_batch(db, filename: str, source_type: str = "csv") -> ImportBatch:
    batch = ImportBatch(
        filename=filename,
        source_type=source_type,
        status="pending",
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def mark_batch_processing(db, batch: ImportBatch, rows_total: int) -> ImportBatch:
    batch.status = "processing"
    batch.rows_total = rows_total
    batch.error_message = None
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def mark_batch_done(
    db,
    batch: ImportBatch,
    rows_created: int,
    rows_updated: int,
    rows_failed: int,
    result_payload: dict[str, Any] | None = None,
) -> ImportBatch:
    batch.status = "done"
    batch.rows_created = rows_created
    batch.rows_updated = rows_updated
    batch.rows_failed = rows_failed
    batch.result_payload = result_payload
    batch.error_message = (
        f"{rows_failed} row(s) failed during import" if rows_failed else None
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def mark_batch_failed(
    db,
    batch: ImportBatch,
    error_message: str,
    result_payload: dict[str, Any] | None = None,
) -> ImportBatch:
    batch.status = "failed"
    batch.error_message = error_message[:1000]
    batch.result_payload = result_payload

    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch