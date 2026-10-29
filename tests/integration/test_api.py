def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_inspect_repository(client, workspace_repo):
    response = client.post(
        "/repositories/inspect",
        json={"repository_name": "demo-repo"},
    )
    assert response.status_code == 200
    assert response.json()["file_count"] == 2


def test_search_repository(client, workspace_repo):
    response = client.post(
        "/repositories/search",
        json={"repository_name": "demo-repo", "query": "calculate total"},
    )
    assert response.status_code == 200
    assert response.json()["results"]


def test_investigation_is_explicitly_mock(client, workspace_repo):
    response = client.post(
        "/investigations",
        json={
            "repository_name": "demo-repo",
            "bug_report": "The total is incorrect for multiple items.",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["provider"] == "mock"
    assert data["task_id"]
    assert data["limitations"]


def test_workspace_path_traversal_is_rejected(client):
    response = client.post(
        "/repositories/inspect",
        json={"repository_name": "../"},
    )
    assert response.status_code == 422


def test_patch_validation_endpoint(client):
    diff = (
        "--- a/app.py\n"
        "+++ b/app.py\n"
        "@@ -1,1 +1,1 @@\n"
        "-x\n"
        "+y\n"
    )
    response = client.post(
        "/patches/validate",
        json={"repository_name": "demo-repo", "diff": diff},
    )
    assert response.status_code == 200
    assert response.json()["valid"] is True
