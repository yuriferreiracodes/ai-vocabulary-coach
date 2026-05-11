import uuid
from sqlalchemy.orm import Session

from app.models.deck import Deck
from app.repositories.base import BaseRepository


class DeckRepository(BaseRepository[Deck]):
    def __init__(self, db: Session) -> None:
        super().__init__(Deck, db)

    def list_by_user(self, user_id: uuid.UUID) -> list[Deck]:
        return (
            self.db.query(Deck)
            .filter(Deck.user_id == user_id)
            .order_by(Deck.created_at.desc())
            .all()
        )

    def get_by_user_and_id(self, user_id: uuid.UUID, deck_id: uuid.UUID) -> Deck | None:
        return (
            self.db.query(Deck)
            .filter(Deck.user_id == user_id, Deck.id == deck_id)
            .first()
        )
