from fastapi import APIRouter, Depends, Request
from app.schemas.task import TaskCreate
from typing import List, Dict, Any
from pydantic import ValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.schemas.task_response import TaskValidationResponse
from app.schemas.task_input import TaskValidationRequest
from app.services.auth import get_current_user
from app.db.models.users import UserModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])
limiter = Limiter(key_func=get_remote_address)

@router.post("/validate", response_model=TaskValidationResponse)
@limiter.limit("100/minute")
def validate_tasks(
    request: Request,
    body: TaskValidationRequest,
    current_user: UserModel = Depends(get_current_user)
):
    valid_tasks = []
    invalid_tasks = []

    for raw_task in body.tasks:
        try:
            task = TaskCreate(**raw_task.model_dump())
            valid_tasks.append(task)

        except ValidationError as e:
            invalid_tasks.append({
                "task": raw_task,
                "errors": e.errors()
            })

    return {"valid_tasks": valid_tasks, "invalid_tasks": invalid_tasks}
