from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session) -> None:
        super().__init__(User, db)

    def get_by_session_id(self, session_id: str) -> User | None:
        return self.db.query(User).filter(User.session_id == session_id).first()

    def get_or_create_by_session(self, session_id: str) -> tuple[User, bool]:
        user = self.get_by_session_id(session_id)
        if user:
            return user, False
        user = User(session_id=session_id)
        return self.create(user), True
