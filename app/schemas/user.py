import uuid
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    native_language: str | None = None
    target_language: str | None = None
    proficiency_level: str | None = None
    learning_goals: str | None = None


class UserCreate(UserBase):
    session_id: str


class UserUpdate(UserBase):
    onboarding_complete: bool | None = None


class UserRead(UserBase):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    session_id: str
    onboarding_complete: bool
    created_at: datetime
