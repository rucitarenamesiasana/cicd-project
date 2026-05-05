from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .storage import JsonTaskStorage

VALID_STATUSES = {"todo", "in_progress", "done"}
VALID_PRIORITIES = {"low", "medium", "high"}


class TaskValidationError(ValueError):
    """Raised when task input data is invalid."""


class TaskNotFoundError(LookupError):
    """Raised when a task cannot be found."""


class TaskService:
    """Business logic for a simple task management system."""

    def __init__(self, storage: Optional[JsonTaskStorage] = None) -> None:
        self.storage = storage or JsonTaskStorage()

    def list_tasks(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        tasks = self.storage.read_tasks()
        if status is None:
            return tasks
        self._validate_status(status)
        return [task for task in tasks if task["status"] == status]

    def create_task(self, title: str, description: str = "", priority: str = "medium") -> Dict[str, Any]:
        title = self._validate_title(title)
        description = self._validate_description(description)
        priority = self._validate_priority(priority)

        tasks = self.storage.read_tasks()
        task = {
            "id": self._next_id(tasks),
            "title": title,
            "description": description,
            "priority": priority,
            "status": "todo",
            "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        }
        tasks.append(task)
        self.storage.write_tasks(tasks)
        return task

    def get_task(self, task_id: int) -> Dict[str, Any]:
        for task in self.storage.read_tasks():
            if task["id"] == task_id:
                return task
        raise TaskNotFoundError(f"Task with id {task_id} was not found")

    def update_status(self, task_id: int, status: str) -> Dict[str, Any]:
        status = self._validate_status(status)
        tasks = self.storage.read_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                self.storage.write_tasks(tasks)
                return task
        raise TaskNotFoundError(f"Task with id {task_id} was not found")

    def delete_task(self, task_id: int) -> Dict[str, Any]:
        tasks = self.storage.read_tasks()
        for index, task in enumerate(tasks):
            if task["id"] == task_id:
                deleted_task = tasks.pop(index)
                self.storage.write_tasks(tasks)
                return deleted_task
        raise TaskNotFoundError(f"Task with id {task_id} was not found")

    def get_statistics(self) -> Dict[str, Any]:
        tasks = self.storage.read_tasks()
        total = len(tasks)
        done = len([task for task in tasks if task["status"] == "done"])
        by_status = {status: len([task for task in tasks if task["status"] == status]) for status in VALID_STATUSES}
        by_priority = {priority: len([task for task in tasks if task["priority"] == priority]) for priority in VALID_PRIORITIES}
        completion_rate = 0 if total == 0 else round((done / total) * 100, 2)
        return {
            "total": total,
            "by_status": by_status,
            "by_priority": by_priority,
            "completion_rate": completion_rate,
        }

    def _next_id(self, tasks: List[Dict[str, Any]]) -> int:
        if not tasks:
            return 1
        return max(task["id"] for task in tasks) + 1

    def _validate_title(self, title: Any) -> str:
        if not isinstance(title, str):
            raise TaskValidationError("Title must be a string")
        title = title.strip()
        if not title:
            raise TaskValidationError("Title is required")
        if len(title) > 100:
            raise TaskValidationError("Title must be 100 characters or fewer")
        return title

    def _validate_description(self, description: Any) -> str:
        if description is None:
            return ""
        if not isinstance(description, str):
            raise TaskValidationError("Description must be a string")
        if len(description) > 500:
            raise TaskValidationError("Description must be 500 characters or fewer")
        return description.strip()

    def _validate_priority(self, priority: Any) -> str:
        if not isinstance(priority, str):
            raise TaskValidationError("Priority must be a string")
        priority = priority.strip().lower()
        if priority not in VALID_PRIORITIES:
            raise TaskValidationError("Priority must be low, medium, or high")
        return priority

    def _validate_status(self, status: Any) -> str:
        if not isinstance(status, str):
            raise TaskValidationError("Status must be a string")
        status = status.strip().lower()
        if status not in VALID_STATUSES:
            raise TaskValidationError("Status must be todo, in_progress, or done")
        return status
