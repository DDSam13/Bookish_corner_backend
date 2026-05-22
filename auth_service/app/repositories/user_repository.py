from sqlalchemy.orm import Session

from ..models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email, User.is_deleted == False)
            .first()
        )

    def get_by_id(self, user_id: str) -> User | None:
        return (
            self.db.query(User)
            .filter(User.id == user_id, User.is_deleted == False)
            .first()
        )

    def create(self, email: str, password_hash: str) -> User:
        user = User(email=email, password_hash=password_hash)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_active(self):
        return (
            self.db.query(User)
            .filter(User.is_deleted == False)
            .all()
        )