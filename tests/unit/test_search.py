from backend.repository.search import search_repository


def test_search_returns_line_references(workspace_repo, test_settings):
    results = search_repository(workspace_repo, "calculate total", 10, test_settings)
    assert results
    assert results[0]["path"] == "cart.py"
    assert results[0]["line_number"] == 1
