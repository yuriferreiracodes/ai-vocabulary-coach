import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.models.flashcard import Flashcard
from app.repositories.flashcard_repository import FlashcardRepository


class FlashcardService:
    def __init__(self, db: Session) -> None:
        self.flashcard_repo = FlashcardRepository(db)

    def get_due_cards(self, deck_id: uuid.UUID) -> list[Flashcard]:
        return self.flashcard_repo.get_due_for_review(deck_id)

    def record_review(self, flashcard_id: uuid.UUID, quality: int) -> Flashcard:
        """Apply SM-2 spaced repetition algorithm."""
        card = self.flashcard_repo.get(flashcard_id)
        if not card:
            raise ValueError(f"Flashcard {flashcard_id} not found")

        if quality < 3:
            card.repetitions = 0
            card.interval_days = 1
        else:
            if card.repetitions == 0:
                card.interval_days = 1
            elif card.repetitions == 1:
                card.interval_days = 6
            else:
                card.interval_days = round(card.interval_days * card.ease_factor)

            card.ease_factor = max(
                1.3,
                card.ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02),
            )
            card.repetitions += 1

        card.next_review_at = datetime.now(timezone.utc) + timedelta(days=card.interval_days)
        return self.flashcard_repo.update(card)
