from datetime import datetime, timedelta, timezone
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.controllers.tasks_controller import get_task_service, router
from app.models.task import Task


class FakeTaskService:
    def __init__(self) -> None:
        self._tasks: list[Task] = []
        self._next_id = 1

    async def create_task(self, task) -> Task:
        created = Task(
            id=self._next_id,
            title=task.title,
            description=task.description,
            is_completed=False,
            created_at=datetime.now(timezone.utc),
        )
        self._next_id += 1
        self._tasks.append(created)
        return created

    async def get_recent_tasks(self) -> list[Task]:
        incomplete = [t for t in self._tasks if not t.is_completed]
        incomplete.sort(key=lambda t: t.created_at, reverse=True)
        return incomplete[:5]

    async def complete_task(self, task_id: int) -> Task | None:
        for idx, task in enumerate(self._tasks):
            if task.id == task_id:
                updated = task.model_copy(update={"is_completed": True})
                self._tasks[idx] = updated
                return updated
        return None


def _build_client(fake_service: FakeTaskService) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/api/v1")
    app.dependency_overrides[get_task_service] = lambda: fake_service
    return TestClient(app)


def test_create_task_endpoint_returns_created_task() -> None:
    client = _build_client(FakeTaskService())

    response = client.post(
        "/api/v1/tasks/create",
        json={"title": "Integrate API", "description": "happy path"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Integrate API"
    assert body["description"] == "happy path"
    assert body["is_completed"] is False
    assert "created_at" in body


def test_recent_tasks_endpoint_returns_only_five_incomplete() -> None:
    fake_service = FakeTaskService()
    base_time = datetime.now(timezone.utc)

    for i in range(7):
        fake_service._tasks.append(
            Task(
                id=i + 1,
                title=f"Task {i + 1}",
                description=None,
                is_completed=False,
                created_at=base_time - timedelta(minutes=i),
            )
        )
    fake_service._tasks[1] = fake_service._tasks[1].model_copy(update={"is_completed": True})

    client = _build_client(fake_service)
    response = client.get("/api/v1/tasks/recent")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 5
    assert all(not item["is_completed"] for item in body)


def test_complete_task_endpoint_marks_task_completed() -> None:
    fake_service = FakeTaskService()
    fake_service._tasks.append(
        Task(
            id=1,
            title="Close ticket",
            description=None,
            is_completed=False,
            created_at=datetime.now(timezone.utc),
        )
    )

    client = _build_client(fake_service)
    response = client.patch("/api/v1/tasks/1/complete")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == 1
    assert body["is_completed"] is True


def test_complete_task_endpoint_returns_404_when_missing() -> None:
    client = _build_client(FakeTaskService())

    response = client.patch("/api/v1/tasks/999/complete")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task 999 not found."}
