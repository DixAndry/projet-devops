from sqlalchemy.orm import Session

from app.models.example import ExampleModel
from app.schemas.example import ExampleCreate


class ExampleService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: ExampleCreate) -> ExampleModel:
        example = ExampleModel(name=payload.name, description=payload.description)
        self.db.add(example)
        self.db.commit()
        self.db.refresh(example)
        return example

    def list(self) -> list[ExampleModel]:
        return self.db.query(ExampleModel).all()
