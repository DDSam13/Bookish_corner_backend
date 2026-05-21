from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.progress_repository import ProgressRepository
from ..schemas.progress import ProgressCreate, ProgressUpdate


class ProgressService:
    def __init__(self, db: Session):
        self.repository = ProgressRepository(db)

    def get_user_progress(self, user_id):
        return self.repository.get_user_progress(user_id)

    def create_progress(self, data: ProgressCreate):
        existing_progress = self.repository.get_book_progress(
            data.user_id,
            data.book_id,
        )

        if existing_progress:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Прогресс по этой книге уже существует",
            )

        return self.repository.create_progress(data)

    def update_progress(self, user_id, book_id, data: ProgressUpdate):
        progress = self.repository.get_book_progress(user_id, book_id)

        if not progress:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Прогресс по книге не найден",
            )

        return self.repository.update_progress(progress, data)