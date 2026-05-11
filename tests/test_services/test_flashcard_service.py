import uuid
from app.models.deck import Deck
from app.models.flashcard import Flashcard
from app.models.user import User
from app.services.flashcard_service import FlashcardService


def test_sm2_good_review(db):
    user = User(session_id=str(uuid.uuid4()))
    db.add(user)
    db.commit()

    deck = Deck(user_id=user.id, title="Test Deck")
    db.add(deck)
    db.commit()

    card = Flashcard(deck_id=deck.id, front="hola", back="hello")
    db.add(card)
    db.commit()

    svc = FlashcardService(db)
    updated = svc.record_review(card.id, quality=4)

    assert updated.repetitions == 1
    assert updated.interval_days == 6
    assert updated.next_review_at is not None


def test_sm2_again_resets(db):
    user = User(session_id=str(uuid.uuid4()))
    db.add(user)
    db.commit()

    deck = Deck(user_id=user.id, title="Test Deck")
    db.add(deck)
    db.commit()

    card = Flashcard(deck_id=deck.id, front="gracias", back="thank you", repetitions=3, interval_days=10)
    db.add(card)
    db.commit()

    svc = FlashcardService(db)
    updated = svc.record_review(card.id, quality=0)

    assert updated.repetitions == 0
    assert updated.interval_days == 1
