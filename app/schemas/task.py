from typing import Optional, Union

from pydantic import BaseModel, Field
from uuid import UUID

class TaskCreate(BaseModel):
    task_id: Optional[Union[str, UUID]] = None
    title: str = Field(..., min_length=1)
    deadline_days: int = Field(..., ge=0)
    estimated_hours: float = Field(..., gt=0)
    importance: int = Field(..., ge=1, le=10)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1)
    deadline_days: Optional[int] = Field(None, ge=0)
    estimated_hours: Optional[float] = Field(None, gt=0)
    importance: Optional[int] = Field(None, ge=1, le=10)

class TaskResponse(BaseModel):
    task_id: Optional[UUID] = None
    title: str
    deadline_days: int
    estimated_hours: float
    importance: int
    score: Optional[float] = None
    category: Optional[str] = None

    class Config:
        from_attributes = True
