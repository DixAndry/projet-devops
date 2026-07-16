from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: TaskCreate) -> Task:
        task = Task(title=payload.title, description=payload.description, completed=payload.completed)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list(self) -> list[Task]:
        return self.db.query(Task).order_by(Task.id).all()

    def get(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update(self, task: Task, payload: TaskUpdate) -> Task:
        if payload.title is not None:
            task.title = payload.title
        if payload.description is not None:
            task.description = payload.description
        if payload.completed is not None:
            task.completed = payload.completed
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
