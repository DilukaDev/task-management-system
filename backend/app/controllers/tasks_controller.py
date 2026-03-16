from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from psycopg import AsyncConnection
from app.database.connection import get_db_connection
from app.models.task import Task, TaskCreate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

async def get_task_service(conn: AsyncConnection = Depends(get_db_connection)) -> TaskService:
    return TaskService(conn)

@router.post("/create", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, service: TaskService = Depends(get_task_service)) -> Task:
    """Create a new task."""
    return await service.create_task(task)

@router.get("/recent", response_model=List[Task])
async def get_recent_tasks(service: TaskService = Depends(get_task_service)) -> List[Task]:
    """Get the 5 most recent incomplete tasks."""
    # Returns only the most recent 5 incomplete tasks
    return await service.get_recent_tasks()

@router.patch("/{task_id}/complete", response_model=Task)
async def complete_task(task_id: int, service: TaskService = Depends(get_task_service)) -> Task:
    """Mark a task as completed."""
    task = await service.complete_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Task {task_id} not found."
        )
    return task
