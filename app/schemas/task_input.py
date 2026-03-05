from pydantic import BaseModel
from typing import Any, List, Dict, Optional, Union
from app.schemas.task import TaskCreate
from uuid import UUID

class TaskInput(BaseModel):
    task_id: Optional[Union[str, UUID]] = None
    title: Any = None
    deadline_days: Any = None
    estimated_hours: Any = None
    importance: Any = None

'''
    Request models for task validation and prioritization endpoints.
    These models allow for flexible input while ensuring that the validation endpoint can identify and report errors effectively.
'''
class TaskValidationRequest(BaseModel):
    tasks: List[TaskInput]

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "task_id": '123e4567-e89b-12d3-a456-426614174000',
                        "title": "Complete project report",
                        "deadline_days": 5,
                        "estimated_hours": 10.5,
                        "importance": 8
                    },
                    {
                        "task_id": None,
                        "title": "",
                        "deadline_days": -1,
                        "estimated_hours": 0,
                        "importance": 15
                    }
                ]
            }
        }


class TaskPrioritizeRequest(BaseModel):
    tasks: List[TaskCreate]

    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "task_id": '123e4567-e89b-12d3-a456-426614174000',
                        "title": "Complete project report",
                        "deadline_days": 5,
                        "estimated_hours": 10.5,
                        "importance": 8
                    },
                    {
                        "task_id": '123e4567-e89b-12d3-a456-426614174001',
                        "title": "Prepare presentation",
                        "deadline_days": 2,
                        "estimated_hours": 6,
                        "importance": 9
                    }
                ]
            }
        }