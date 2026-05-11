from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from app.database import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], db: Session) -> None:
        self.model = model
        self.db = db

    def get(self, id: object) -> ModelT | None:
        return self.db.get(self.model, id)

    def list(self, *, offset: int = 0, limit: int = 100) -> list[ModelT]:
        return self.db.query(self.model).offset(offset).limit(limit).all()

    def create(self, obj: ModelT) -> ModelT:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, obj: ModelT) -> ModelT:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelT) -> None:
        self.db.delete(obj)
        self.db.commit()
