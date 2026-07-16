from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.base import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/", response_model=dict[str, str])
async def read_root() -> dict[str, str]:
    return {"message": "API prête"}


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskRead:
    service = TaskService(db)
    task = service.create(payload)
    return TaskRead.model_validate(task)


@router.get("/tasks", response_model=list[TaskRead])
async def list_tasks(db: Session = Depends(get_db)) -> list[TaskRead]:
    service = TaskService(db)
    tasks = service.list()
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskRead:
    service = TaskService(db)
    task = service.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche introuvable")
    return TaskRead.model_validate(task)


@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)) -> TaskRead:
    service = TaskService(db)
    task = service.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche introuvable")
    updated_task = service.update(task, payload)
    return TaskRead.model_validate(updated_task)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: Session = Depends(get_db)) -> None:
    service = TaskService(db)
    task = service.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tâche introuvable")
    service.delete(task)
