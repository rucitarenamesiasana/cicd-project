from flask import Flask, jsonify, request

from .storage import JsonTaskStorage
from .task_service import TaskNotFoundError, TaskService, TaskValidationError


def create_app(storage_path: str = "data/tasks.json") -> Flask:
    app = Flask(__name__)
    service = TaskService(JsonTaskStorage(storage_path))

    @app.get("/")
    def home():
        return jsonify({"message": "Task Management API", "status": "running"})

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/tasks")
    def list_tasks():
        status = request.args.get("status")
        return jsonify(service.list_tasks(status=status))

    @app.post("/tasks")
    def create_task():
        payload = request.get_json(silent=True) or {}
        task = service.create_task(
            title=payload.get("title", ""),
            description=payload.get("description", ""),
            priority=payload.get("priority", "medium"),
        )
        return jsonify(task), 201

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id: int):
        return jsonify(service.get_task(task_id))

    @app.patch("/tasks/<int:task_id>/status")
    def update_task_status(task_id: int):
        payload = request.get_json(silent=True) or {}
        return jsonify(service.update_status(task_id, payload.get("status", "")))

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id: int):
        deleted_task = service.delete_task(task_id)
        return jsonify({"message": "Task deleted", "task": deleted_task})

    @app.get("/stats")
    def statistics():
        return jsonify(service.get_statistics())

    @app.errorhandler(TaskValidationError)
    def handle_validation_error(error):
        return jsonify({"error": str(error)}), 402

    @app.errorhandler(TaskNotFoundError)
    def handle_not_found(error):
        return jsonify({"error": str(error)}), 408

    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", port=5000, debug=False)
