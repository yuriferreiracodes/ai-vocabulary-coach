import uuid
from sqlalchemy.orm import Session, joinedload

from app.models.conversation import Conversation, ConversationMessage
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: Session) -> None:
        super().__init__(Conversation, db)

    def get_active_onboarding(self, user_id: uuid.UUID) -> Conversation | None:
        return (
            self.db.query(Conversation)
            .options(joinedload(Conversation.messages))
            .filter(
                Conversation.user_id == user_id,
                Conversation.conversation_type == "onboarding",
            )
            .order_by(Conversation.created_at.desc())
            .first()
        )

    def add_message(
        self, conversation_id: uuid.UUID, role: str, content: str
    ) -> ConversationMessage:
        msg = ConversationMessage(
            conversation_id=conversation_id, role=role, content=content
        )
        self.db.add(msg)
        self.db.commit()
        self.db.refresh(msg)
        return msg
