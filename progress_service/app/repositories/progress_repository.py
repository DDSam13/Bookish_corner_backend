from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from ..models.reading_progress import ReadingProgress


class ProgressRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_progress(self, user_id: UUID):
        return (
            self.db.query(ReadingProgress)
            .filter(ReadingProgress.user_id == user_id)
            .all()
        )

    def get_book_progress(self, user_id: UUID, book_id: UUID):
        return (
            self.db.query(ReadingProgress)
            .filter(
                ReadingProgress.user_id == user_id,
                ReadingProgress.book_id == book_id,
            )
            .first()
        )

    def create_progress(self, data):
        progress = ReadingProgress(**data.model_dump())

        self.db.add(progress)
        self.db.commit()
        self.db.refresh(progress)

        return progress

    def update_progress(self, progress: ReadingProgress, data):
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(progress, key, value)

        progress.updated_at = datetime.utcnow()
        progress.last_opened_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(progress)

        return progress