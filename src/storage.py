import json
import os
from typing import Any, Dict, List


class JsonTaskStorage:
    """Simple JSON-file storage for tasks."""

    def __init__(self, path: str = "data/tasks.json") -> None:
        self.path = path
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        if not os.path.exists(path):
            self.write_tasks([])

    def read_tasks(self) -> List[Dict[str, Any]]:
        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(tasks, file, indent=2)
