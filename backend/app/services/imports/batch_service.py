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
) -> ImportBatch:
    batch.status = "done"
    batch.rows_created = rows_created
    batch.rows_updated = rows_updated
    batch.rows_failed = rows_failed
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def mark_batch_failed(db, batch: ImportBatch, error_message: str) -> ImportBatch:
    batch.status = "failed"
    batch.error_message = error_message[:1000]
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch