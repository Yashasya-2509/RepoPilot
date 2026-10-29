import pytest

from backend.repository.loader import inspect_repository, safe_read_text


def test_inspects_source_files(workspace_repo, test_settings):
    result = inspect_repository(workspace_repo, test_settings)
    assert result["file_count"] == 2
    assert result["languages"]["Python"] == 1


def test_skips_sensitive_files(workspace_repo, test_settings):
    (workspace_repo / ".env").write_text("API_KEY=not-for-logs", encoding="utf-8")
    result = inspect_repository(workspace_repo, test_settings)
    assert ".env" not in [item["path"] for item in result["files"]]
    assert result["skipped"]["sensitive_name"] == 1


def test_safe_read_rejects_parent_traversal(workspace_repo, test_settings):
    with pytest.raises(ValueError):
        safe_read_text(workspace_repo, "../outside.txt", test_settings)


def test_safe_read_returns_text(workspace_repo, test_settings):
    content = safe_read_text(workspace_repo, "cart.py", test_settings)
    assert "calculate_total" in content
