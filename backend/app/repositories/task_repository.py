from typing import List, Optional
from psycopg import AsyncConnection
from app.models.task import Task, TaskCreate

class TaskRepository:
    def __init__(self, conn: AsyncConnection):
        self.conn = conn

    async def create(self, task: TaskCreate) -> Task:
        """Insert a new task into the database."""
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO task (title, description)
                VALUES (%s, %s)
                RETURNING id, title, description, is_completed, created_at
                """,
                (task.title, task.description)
            )
            row = await cur.fetchone()
            await self.conn.commit()
            return Task(**row)

    async def get_recent_active_tasks(self, limit: int = 5) -> List[Task]:
        """Fetch the most recent incomplete tasks."""
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, title, description, is_completed, created_at
                FROM task
                WHERE is_completed = FALSE
                ORDER BY created_at DESC
                LIMIT %s
                """,
                (limit,)
            )
            rows = await cur.fetchall()
            return [Task(**row) for row in rows]

    async def mark_completed(self, task_id: int) -> Optional[Task]:
        """Update a task's status to completed."""
        async with self.conn.cursor() as cur:
            await cur.execute(
                """
                UPDATE task
                SET is_completed = TRUE
                WHERE id = %s
                RETURNING id, title, description, is_completed, created_at
                """,
                (task_id,)
            )
            row = await cur.fetchone()
            await self.conn.commit()
            if row:
                return Task(**row)
            return None
