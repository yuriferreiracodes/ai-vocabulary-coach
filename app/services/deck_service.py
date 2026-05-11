import uuid
from sqlalchemy.orm import Session

from app.models.deck import Deck
from app.models.flashcard import Flashcard
from app.repositories.deck_repository import DeckRepository
from app.repositories.flashcard_repository import FlashcardRepository
from app.repositories.user_repository import UserRepository
from app.services import ai_service


class DeckService:
    def __init__(self, db: Session) -> None:
        self.deck_repo = DeckRepository(db)
        self.flashcard_repo = FlashcardRepository(db)
        self.user_repo = UserRepository(db)

    def list_decks(self, session_id: str) -> list[Deck]:
        user = self.user_repo.get_by_session_id(session_id)
        if not user:
            return []
        return self.deck_repo.list_by_user(user.id)

    def get_deck(self, session_id: str, deck_id: uuid.UUID) -> Deck | None:
        user = self.user_repo.get_by_session_id(session_id)
        if not user:
            return None
        return self.deck_repo.get_by_user_and_id(user.id, deck_id)

    def generate_deck(self, session_id: str, topic: str, count: int = 10) -> Deck:
        user = self.user_repo.get_by_session_id(session_id)
        if not user:
            raise ValueError("User not found")
        if not user.onboarding_complete:
            raise ValueError("User must complete onboarding first")

        raw_cards = ai_service.generate_flashcards(
            native_language=user.native_language or "English",
            target_language=user.target_language or "Spanish",
            proficiency_level=user.proficiency_level or "beginner",
            topic=topic,
            count=count,
        )

        deck = Deck(
            user_id=user.id,
            title=f"{user.target_language} — {topic.title()}",
            description=f"AI-generated deck for {topic}",
            topic=topic,
            language=user.target_language,
        )
        deck = self.deck_repo.create(deck)

        flashcards = [
            Flashcard(
                deck_id=deck.id,
                front=card["front"],
                back=card["back"],
                example_sentence=card.get("example_sentence"),
                pronunciation=card.get("pronunciation"),
            )
            for card in raw_cards
        ]
        self.flashcard_repo.bulk_create(flashcards)

        return deck

    def delete_deck(self, session_id: str, deck_id: uuid.UUID) -> bool:
        deck = self.get_deck(session_id, deck_id)
        if not deck:
            return False
        self.deck_repo.delete(deck)
        return True
