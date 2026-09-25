"""boards.flatten_item must give the row shape gh's item-list gives, because every
tracker, pulse and assign read goes through field_value() on that shape."""
import importlib.util
import pathlib

spec = importlib.util.spec_from_file_location(
    "boards", pathlib.Path(__file__).parent.parent / "scripts" / "boards.py")
boards = importlib.util.module_from_spec(spec)
spec.loader.exec_module(boards)

ITEM = {
    "id": "PVTI_1",
    "content": {"__typename": "DraftIssue", "id": "DI_1", "title": "ada · C03", "body": ""},
    "fieldValues": {"nodes": [
        {"__typename": "ProjectV2ItemFieldTextValue", "text": "ada · C03", "field": {"name": "Title"}},
        {"__typename": "ProjectV2ItemFieldSingleSelectValue", "name": "Passed", "field": {"name": "Outcome"}},
        {"__typename": "ProjectV2ItemFieldNumberValue", "number": 2.0, "field": {"name": "Attempts"}},
        {"__typename": "ProjectV2ItemFieldDateValue", "date": "2026-09-03", "field": {"name": "First attempt"}},
        {"__typename": "ProjectV2ItemFieldUserValue"},
    ]},
}


def test_row_matches_gh_shape():
    row = boards.flatten_item(ITEM)
    assert row["id"] == "PVTI_1"
    assert row["title"] == "ada · C03"
    assert row["outcome"] == "Passed"
    assert row["attempts"] == 2 and isinstance(row["attempts"], int)
    assert row["first attempt"] == "2026-09-03"
    assert "assignees" not in row                      # unread types are absent, not None


def test_field_value_reads_it_like_a_gh_row():
    row = boards.flatten_item(ITEM)
    assert boards.field_value(row, "First attempt") == "2026-09-03"
    assert int(boards.field_value(row, "Attempts") or 0) == 2
    assert boards.field_value(row, "Outcome") == "Passed"
    assert boards.field_value(row, "Passed on") is None


def test_title_falls_back_to_content():
    bare = {"id": "PVTI_2", "content": {"title": "from content"}, "fieldValues": {"nodes": []}}
    assert boards.flatten_item(bare)["title"] == "from content"
