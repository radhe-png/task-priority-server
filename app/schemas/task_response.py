from pydantic import BaseModel
from typing import List, Optional
from app.schemas.task import TaskCreate
from uuid import UUID, uuid4

'''
    Response models for task validation and prioritization endpoints.
'''
class InvalidTask(BaseModel):
    task: dict
    errors: list

class TaskValidationResponse(BaseModel):
    valid_tasks: List[TaskCreate]
    invalid_tasks: List[InvalidTask]

class PrioritizedTask(BaseModel):
    task_id: Optional[UUID] = None
    title: str
    score: float
    category: str
    explanation: List[str]

class TaskPrioritizeResponse(BaseModel):
    tasks: List[PrioritizedTask]