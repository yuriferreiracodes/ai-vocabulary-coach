import uuid
from datetime import datetime
from pydantic import BaseModel


class FlashcardBase(BaseModel):
    front: str
    back: str
    example_sentence: str | None = None
    pronunciation: str | None = None


class FlashcardCreate(FlashcardBase):
    pass


class FlashcardRead(FlashcardBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    deck_id: uuid.UUID
    ease_factor: float
    interval_days: int
    repetitions: int
    next_review_at: datetime | None
    created_at: datetime


class ReviewResult(BaseModel):
    flashcard_id: uuid.UUID
    quality: int  # 0-5 scale (SM-2 algorithm)


class ChatMessage(BaseModel):
    content: str
