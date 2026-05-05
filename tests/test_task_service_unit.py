import pytest

from src.storage import JsonTaskStorage
from src.task_service import TaskNotFoundError, TaskService, TaskValidationError


@pytest.fixture
def service(tmp_path):
    storage = JsonTaskStorage(str(tmp_path / "tasks.json"))
    return TaskService(storage)


def test_create_task_success(service):
    task = service.create_task("Belajar testing", "Unit test", "high")
    assert task["id"] == 1
    assert task["title"] == "Belajar testing"
    assert task["description"] == "Unit test"
    assert task["priority"] == "high"
    assert task["status"] == "todo"


def test_create_task_assigns_incremental_id(service):
    first = service.create_task("Task 1")
    second = service.create_task("Task 2")
    assert first["id"] == 1
    assert second["id"] == 2


def test_create_task_trims_title_and_description(service):
    task = service.create_task("  Task rapi  ", "  Desc  ")
    assert task["title"] == "Task rapi"
    assert task["description"] == "Desc"


def test_create_task_default_priority_medium(service):
    task = service.create_task("Default priority")
    assert task["priority"] == "medium"


def test_create_task_title_required(service):
    with pytest.raises(TaskValidationError, match="Title is required"):
        service.create_task("   ")


def test_create_task_title_must_be_string(service):
    with pytest.raises(TaskValidationError, match="Title must be a string"):
        service.create_task(123)


def test_create_task_title_max_length(service):
    with pytest.raises(TaskValidationError, match="100 characters"):
        service.create_task("a" * 101)


def test_create_task_invalid_priority(service):
    with pytest.raises(TaskValidationError, match="Priority must be"):
        service.create_task("Task", priority="urgent")


def test_create_task_priority_case_insensitive(service):
    task = service.create_task("Task", priority="HIGH")
    assert task["priority"] == "high"


def test_create_task_description_none_becomes_empty(service):
    task = service.create_task("Task", description=None)
    assert task["description"] == ""


def test_create_task_description_must_be_string(service):
    with pytest.raises(TaskValidationError, match="Description must be a string"):
        service.create_task("Task", description=123)


def test_create_task_description_max_length(service):
    with pytest.raises(TaskValidationError, match="500 characters"):
        service.create_task("Task", description="a" * 501)


def test_get_task_success(service):
    task = service.create_task("Find me")
    assert service.get_task(task["id"])["title"] == "Find me"


def test_get_task_not_found(service):
    with pytest.raises(TaskNotFoundError):
        service.get_task(99)


def test_update_status_success(service):
    task = service.create_task("Update me")
    updated = service.update_status(task["id"], "done")
    assert updated["status"] == "done"


def test_update_status_invalid(service):
    task = service.create_task("Update invalid")
    with pytest.raises(TaskValidationError, match="Status must be"):
        service.update_status(task["id"], "closed")


def test_update_status_not_found(service):
    with pytest.raises(TaskNotFoundError):
        service.update_status(999, "done")


def test_delete_task_success(service):
    task = service.create_task("Delete me")
    deleted = service.delete_task(task["id"])
    assert deleted["title"] == "Delete me"
    assert service.list_tasks() == []


def test_delete_task_not_found(service):
    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)


def test_list_tasks_filter_by_status(service):
    first = service.create_task("Todo")
    second = service.create_task("Done")
    service.update_status(second["id"], "done")
    done_tasks = service.list_tasks(status="done")
    assert len(done_tasks) == 1
    assert done_tasks[0]["id"] == second["id"]
    assert service.get_task(first["id"])["status"] == "todo"


def test_list_tasks_invalid_status_filter(service):
    with pytest.raises(TaskValidationError):
        service.list_tasks(status="invalid")


def test_statistics_empty(service):
    stats = service.get_statistics()
    assert stats["total"] == 0
    assert stats["completion_rate"] == 0


def test_statistics_with_tasks(service):
    service.create_task("A", priority="high")
    task_b = service.create_task("B", priority="low")
    service.update_status(task_b["id"], "done")
    stats = service.get_statistics()
    assert stats["total"] == 2
    assert stats["by_status"]["done"] == 1
    assert stats["by_priority"]["high"] == 1
    assert stats["completion_rate"] == 50.0
