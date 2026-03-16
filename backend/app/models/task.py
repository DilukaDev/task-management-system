from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., max_length=255, description="Title of the task")
    description: Optional[str] = Field(None, description="Detailed description of the task")

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_completed: bool = False
    created_at: datetime
