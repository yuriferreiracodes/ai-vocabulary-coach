import uuid
from datetime import datetime
from pydantic import BaseModel


class DeckBase(BaseModel):
    title: str
    description: str | None = None
    topic: str | None = None
    language: str | None = None


class DeckCreate(DeckBase):
    pass


class DeckRead(DeckBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    flashcard_count: int = 0
