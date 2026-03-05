from fastapi import APIRouter, Depends, Request
from typing import List, Dict, Any
from pydantic import ValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.task import TaskResponse
from app.services.prioritize_tasks import calculate_priority
from app.schemas.task_input import TaskPrioritizeRequest
from app.schemas.task_response import TaskPrioritizeResponse
from app.services.auth import get_current_user
from app.db.models.users import UserModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/prioritize", response_model=TaskPrioritizeResponse, status_code=200)
@limiter.limit("100/minute")
def prioritize_tasks(
    request: Request,
    body: TaskPrioritizeRequest,
    current_user: UserModel = Depends(get_current_user)
):
    prioritized = []

    for task in body.tasks:
        result = calculate_priority(task)
        prioritized.append(result)

    return {"tasks": prioritized}