import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.flashcard import Flashcard
from app.repositories.base import BaseRepository


class FlashcardRepository(BaseRepository[Flashcard]):
    def __init__(self, db: Session) -> None:
        super().__init__(Flashcard, db)

    def list_by_deck(self, deck_id: uuid.UUID) -> list[Flashcard]:
        return self.db.query(Flashcard).filter(Flashcard.deck_id == deck_id).all()

    def get_due_for_review(self, deck_id: uuid.UUID) -> list[Flashcard]:
        now = datetime.now(timezone.utc)
        return (
            self.db.query(Flashcard)
            .filter(
                Flashcard.deck_id == deck_id,
                (Flashcard.next_review_at == None) | (Flashcard.next_review_at <= now),  # noqa: E711
            )
            .all()
        )

    def bulk_create(self, flashcards: list[Flashcard]) -> list[Flashcard]:
        self.db.add_all(flashcards)
        self.db.commit()
        for fc in flashcards:
            self.db.refresh(fc)
        return flashcards
