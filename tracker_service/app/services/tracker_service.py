from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repositories.tracker_repository import TrackerRepository


class TrackerService:
    def __init__(self, db: Session):
        self.repository = TrackerRepository(db)

    def get_goal(self, user_id):
        goal = self.repository.get_user_goal(user_id)

        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Цель пользователя не найдена",
            )

        return goal

    def create_goal(self, data):
        existing_goal = self.repository.get_user_goal(data.user_id)

        if existing_goal:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Цель уже существует",
            )

        return self.repository.create_goal(data)

    def update_goal(self, user_id, data):
        goal = self.repository.get_user_goal(user_id)

        if not goal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Цель пользователя не найдена",
            )

        return self.repository.update_goal(goal, data)

    def create_session(self, data):
        return self.repository.add_reading_session(data)

    def get_sessions(self, user_id):
        return self.repository.get_user_sessions(user_id)