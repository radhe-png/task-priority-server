from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.auth import get_current_user
from app.db.models.users import UserModel, UserRole
from app.db.models.task import TaskModel
from app.services.prioritize_tasks import calculate_priority
import logging

router = APIRouter(prefix="/tasks", tags=["Task Management"])
limiter = Limiter(key_func=get_remote_address)

logger = logging.getLogger(__name__)

# Helper function to check if user is admin
def is_admin(user: UserModel) -> bool:
    return user.role == UserRole.ADMIN

@router.get("/", response_model=List[TaskResponse])
@limiter.limit("50/minute")
def get_tasks(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get tasks based on user role"""
    # print("Current user:::::::::::::::::::::::::;", current_user)
    tasks = db.query(TaskModel).offset(skip).limit(limit).all()
    # print("All tasks:::::::::::::::::::::::::;", tasks)

    if is_admin(current_user):
        logger.info("Admin user accessing all tasks")
        return tasks
    tasks = db.query(TaskModel).filter(TaskModel.user_id==current_user.user_id).offset(skip).limit(limit).all()
    return tasks

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
def create_task(
    request: Request,
    task: TaskCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task"""
    # Calculate priority score
    priority_result = calculate_priority(task)
    # print("Calculated priority::::::::::::::::::::::::::;", priority_result)
    score = priority_result['score']
    category = priority_result["category"]

    # Create task with current user's ID
    db_task = TaskModel(
        title=task.title,
        deadline_days=task.deadline_days,
        estimated_hours=task.estimated_hours,
        importance=task.importance,
        score=score,
        category=category,
        user_id=current_user.user_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/{task_id}", response_model=TaskResponse)
@limiter.limit("100/minute")
def update_task(
    request: Request,
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task"""
    task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()
    if task.user_id!=current_user.user_id and not is_admin(current_user):
        logger.error(f"User {current_user.user_id} attempted to update task {task_id} without permission")
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    if not task:
        logger.error(f"Task {task_id} not found")
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    if any(k in update_data for k in ['deadline_days', 'estimated_hours', 'importance']):
        priority_result = calculate_priority(task)
        task.score = priority_result['score']
        task.category = priority_result['category']

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
@limiter.limit("10/minute")
def delete_task(
    request: Request,
    task_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task"""
    task = db.query(TaskModel).filter(TaskModel.task_id == task_id).first()

    if task.user_id!=current_user.user_id and not is_admin(current_user):
        logger.error(f"User {current_user.user_id} attempted to delete task {task_id} without permission")
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    if not task:
        logger.error(f"Task {task_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}