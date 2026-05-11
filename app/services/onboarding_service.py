from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.user import User
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.user_repository import UserRepository
from app.services import ai_service


class OnboardingService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repo = UserRepository(db)
        self.conv_repo = ConversationRepository(db)

    def get_or_create_session(self, session_id: str) -> User:
        user, _ = self.user_repo.get_or_create_by_session(session_id)
        return user

    def get_conversation_history(self, user: User) -> Conversation | None:
        return self.conv_repo.get_active_onboarding(user.id)

    def send_message(self, session_id: str, user_message: str) -> dict:
        user = self.get_or_create_session(session_id)

        conversation = self.get_conversation_history(user)
        if not conversation:
            conversation = Conversation(user_id=user.id, conversation_type="onboarding")
            self.conv_repo.create(conversation)

        self.conv_repo.add_message(conversation.id, "user", user_message)

        history = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]

        ai_reply, profile = ai_service.chat_onboarding(history)

        self.conv_repo.add_message(conversation.id, "assistant", ai_reply)

        onboarding_complete = False
        if profile and profile.get("onboarding_complete"):
            user.native_language = profile.get("native_language")
            user.target_language = profile.get("target_language")
            user.proficiency_level = profile.get("proficiency_level")
            user.learning_goals = profile.get("learning_goals")
            user.onboarding_complete = True
            self.user_repo.update(user)
            onboarding_complete = True

        return {
            "reply": ai_reply,
            "onboarding_complete": onboarding_complete,
        }
