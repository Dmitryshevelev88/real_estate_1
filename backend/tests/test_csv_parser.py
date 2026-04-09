from app.services.imports.csv_parser import parse_catalog_csv


def test_parse_catalog_csv_valid():
    content = """external_id,display_name,infrastructure,lighting,noise,insolation,development
1001,ЖК Солнечный,8,7,6,9,7
""".encode("utf-8")

    rows, errors = parse_catalog_csv(content)

    assert len(rows) == 1
    assert len(errors) == 0
    assert rows[0].external_id == "1001"
    assert rows[0].display_name == "ЖК Солнечный"
    assert rows[0].infrastructure == 8
    assert rows[0].lighting == 7
    assert rows[0].noise == 6
    assert rows[0].insolation == 9
    assert rows[0].development == 7


def test_parse_catalog_csv_invalid_metric():
    content = """external_id,display_name,infrastructure,lighting,noise,insolation,development
1001,ЖК Солнечный,99,7,6,9,7
""".encode("utf-8")

    rows, errors = parse_catalog_csv(content)

    assert len(rows) == 0
    assert len(errors) == 1
    assert errors[0]["row_number"] == 2