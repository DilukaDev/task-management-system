from datetime import datetime, timezone
from unittest.mock import AsyncMock
import pytest
from app.models.task import Task, TaskCreate
from app.services.task_service import TaskService


def _sample_task(task_id: int = 1, title: str = "Test task") -> Task:
    return Task(
        id=task_id,
        title=title,
        description="desc",
        is_completed=False,
        created_at=datetime.now(timezone.utc),
    )


@pytest.mark.asyncio
async def test_create_task_delegates_to_repository() -> None:
    service = TaskService(conn=object())
    service.repo = AsyncMock()

    payload = TaskCreate(title="Write tests", description="unit")
    expected = _sample_task()
    service.repo.create.return_value = expected

    result = await service.create_task(payload)

    service.repo.create.assert_awaited_once_with(payload)
    assert result == expected


@pytest.mark.asyncio
async def test_get_recent_tasks_uses_limit_five() -> None:
    service = TaskService(conn=object())
    service.repo = AsyncMock()

    expected = [_sample_task(task_id=i) for i in range(1, 4)]
    service.repo.get_recent_active_tasks.return_value = expected

    result = await service.get_recent_tasks()

    service.repo.get_recent_active_tasks.assert_awaited_once_with(limit=5)
    assert result == expected


@pytest.mark.asyncio
async def test_complete_task_returns_repository_result() -> None:
    service = TaskService(conn=object())
    service.repo = AsyncMock()

    expected = _sample_task(task_id=99)
    service.repo.mark_completed.return_value = expected

    result = await service.complete_task(99)

    service.repo.mark_completed.assert_awaited_once_with(99)
    assert result == expected


@pytest.mark.asyncio
async def test_complete_task_returns_none_when_missing() -> None:
    service = TaskService(conn=object())
    service.repo = AsyncMock()
    service.repo.mark_completed.return_value = None

    result = await service.complete_task(404)

    service.repo.mark_completed.assert_awaited_once_with(404)
    assert result is None
