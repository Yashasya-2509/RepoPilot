from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from backend.app import app
from backend.config import get_settings


@pytest.fixture
def test_settings(tmp_path, monkeypatch):
    workspace = tmp_path / "workspaces"
    workspace.mkdir()
    database = tmp_path / "artifacts" / "test.sqlite3"
    monkeypatch.setenv("WORKSPACE_ROOT", str(workspace))
    monkeypatch.setenv("DATABASE_PATH", str(database))
    get_settings.cache_clear()
    yield get_settings()
    get_settings.cache_clear()


@pytest.fixture
def workspace_repo(test_settings):
    repo = test_settings.workspace_root / "demo-repo"
    repo.mkdir()
    (repo / "cart.py").write_text(
        "def calculate_total(items):\n"
        "    total = 0\n"
        "    for item in items:\n"
        "        total += item['price']\n"
        "    return total\n",
        encoding="utf-8",
    )
    (repo / "README.md").write_text("Demo fixture repository\n", encoding="utf-8")
    return repo


@pytest.fixture
def client(test_settings):
    with TestClient(app) as test_client:
        yield test_client
