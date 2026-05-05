import pytest

from src.app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "tasks.json"))
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_create_task_endpoint_success(client):
    response = client.post("/tasks", json={"title": "API task", "priority": "high"})
    assert response.status_code == 201
    body = response.get_json()
    assert body["id"] == 1
    assert body["title"] == "API task"
    assert body["priority"] == "high"


def test_create_task_endpoint_validation_error(client):
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
    assert "Title is required" in response.get_json()["error"]


def test_get_task_endpoint_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert "not found" in response.get_json()["error"]


def test_full_task_flow_create_update_filter_stats_delete(client):
    created = client.post("/tasks", json={"title": "Flow task", "priority": "medium"})
    task_id = created.get_json()["id"]

    fetched = client.get(f"/tasks/{task_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["title"] == "Flow task"

    updated = client.patch(f"/tasks/{task_id}/status", json={"status": "done"})
    assert updated.status_code == 200
    assert updated.get_json()["status"] == "done"

    filtered = client.get("/tasks?status=done")
    assert filtered.status_code == 200
    assert len(filtered.get_json()) == 1

    stats = client.get("/stats")
    assert stats.status_code == 200
    assert stats.get_json()["completion_rate"] == 100.0

    deleted = client.delete(f"/tasks/{task_id}")
    assert deleted.status_code == 200
    assert deleted.get_json()["message"] == "Task deleted"


def test_update_status_endpoint_validation_error(client):
    created = client.post("/tasks", json={"title": "Bad status"})
    task_id = created.get_json()["id"]
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "invalid"})
    assert response.status_code == 400


def test_list_tasks_endpoint_returns_all_tasks(client):
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 2
