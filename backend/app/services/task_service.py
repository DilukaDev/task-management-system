from typing import List, Optional
from psycopg import AsyncConnection
from app.repositories.task_repository import TaskRepository
from app.models.task import Task, TaskCreate

class TaskService:
    def __init__(self, conn: AsyncConnection):
        self.repo = TaskRepository(conn)

    async def create_task(self, task: TaskCreate) -> Task:
        """Create a new task in the database."""
        return await self.repo.create(task)

    async def get_recent_tasks(self) -> List[Task]:
        """Retrieve the 5 most recent incomplete tasks."""
        return await self.repo.get_recent_active_tasks(limit=5)

    async def complete_task(self, task_id: int) -> Optional[Task]:
        """Mark a task as completed."""
        return await self.repo.mark_completed(task_id)
