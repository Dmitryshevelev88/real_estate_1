import json
import uuid
from pathlib import Path
from urllib import error, parse, request

import pytest


BASE_URL = "http://localhost:8000/api/v1"
CSV_PATH = Path(__file__).parent / "fixtures" / "test_analytics.csv"


def _json_request(method: str, url: str, body: bytes | None = None, headers: dict | None = None):
    req = request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with request.urlopen(req) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8")
        payload = json.loads(raw) if raw else None
        return exc.code, payload


def _get_json(path: str, query: dict | None = None):
    url = f"{BASE_URL}{path}"
    if query:
        url = f"{url}?{parse.urlencode(query)}"
    status, payload = _json_request("GET", url)
    assert status == 200, f"GET {url} failed: {status} {payload}"
    return payload


def _patch_json(path: str, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    status, response = _json_request(
        "PATCH",
        f"{BASE_URL}{path}",
        body=body,
        headers={"Content-Type": "application/json"},
    )
    assert status == 200, f"PATCH {path} failed: {status} {response}"
    return response


def _encode_multipart(file_path: Path, field_name: str = "file") -> tuple[bytes, str]:
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    filename = file_path.name
    content = file_path.read_bytes()

    parts = []
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        (
            f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        ).encode()
    )
    parts.append(b"Content-Type: text/csv\r\n\r\n")
    parts.append(content)
    parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(parts)
    content_type = f"multipart/form-data; boundary={boundary}"
    return body, content_type


def _upload_csv(file_path: Path):
    assert file_path.exists(), f"CSV file not found: {file_path}"

    body, content_type = _encode_multipart(file_path)
    status, payload = _json_request(
        "POST",
        f"{BASE_URL}/admin/import-batches/upload",
        body=body,
        headers={"Content-Type": content_type},
    )
    assert status == 200, f"CSV upload failed: {status} {payload}"
    return payload


def _find_property_by_query(query: str):
    items = _get_json("/catalog-properties/search", {"q": query})
    assert items, f"No catalog properties found for query={query!r}"
    return items[0]


def test_import_csv_success():
    result = _upload_csv(CSV_PATH)

    assert result["status"] == "done"
    assert result["rows_failed"] == 0
    assert result["rows_total"] >= 1
    assert result["rows_created"] + result["rows_updated"] >= 1
    assert result["errors"] == []


def test_repeat_import_updates_without_duplicates():
    first = _upload_csv(CSV_PATH)
    second = _upload_csv(CSV_PATH)

    assert first["status"] == "done"
    assert second["status"] == "done"
    assert second["rows_failed"] == 0
    assert second["rows_updated"] >= 1

    items = _get_json("/catalog-properties/search", {"q": "Солнечный"})
    ids = [item["id"] for item in items]

    assert ids, "Search returned no properties after import"
    assert len(ids) == len(set(ids)), f"Duplicate property ids in search response: {ids}"


def test_evaluation_uses_latest_published_analytics():
    prop = _find_property_by_query("Солнечный")
    property_id = prop["id"]

    analytics = _get_json(f"/catalog-properties/{property_id}/analytics")
    evaluation = _get_json(f"/catalog-properties/{property_id}/evaluation")

    assert analytics["catalog_property_id"] == property_id
    assert analytics["is_published"] is True

    eval_analytics = evaluation["analytics"]
    assert eval_analytics["id"] == analytics["id"]
    assert eval_analytics["version"] == analytics["version"]
    assert eval_analytics["is_published"] is True


def test_admin_history_has_single_published_latest_version():
    prop = _find_property_by_query("Солнечный")
    property_id = prop["id"]

    history = _get_json(f"/admin/catalog-properties/{property_id}/analytics")
    assert history, "Admin analytics history is empty"

    versions = [item["version"] for item in history]
    published = [item for item in history if item["is_published"]]

    assert versions == sorted(versions, reverse=True), f"Versions are not sorted desc: {versions}"
    assert len(published) == 1, f"Expected exactly one published analytics, got {len(published)}"
    assert published[0]["version"] == max(versions)


def test_admin_patch_catalog_property_idempotent():
    prop = _find_property_by_query("Солнечный")
    property_id = prop["id"]

    current = _get_json(f"/admin/catalog-properties/{property_id}")
    patched = _patch_json(
        f"/admin/catalog-properties/{property_id}",
        {
            "project_name": current["project_name"],
            "status": current["status"],
        },
    )

    assert patched["id"] == property_id
    assert patched["project_name"] == current["project_name"]
    assert patched["status"] == current["status"]


def test_admin_patch_property_analytics_idempotent():
    prop = _find_property_by_query("Солнечный")
    property_id = prop["id"]

    history = _get_json(f"/admin/catalog-properties/{property_id}/analytics")
    current = history[0]

    patched = _patch_json(
        f"/admin/property-analytics/{current['id']}",
        {
            "source_label": current["source_label"],
            "is_published": current["is_published"],
        },
    )

    assert patched["id"] == current["id"]
    assert patched["catalog_property_id"] == property_id
    assert patched["is_published"] == current["is_published"]