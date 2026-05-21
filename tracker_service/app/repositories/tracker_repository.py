from sqlalchemy.orm import Session

from ..models.reading_goal import ReadingGoal
from ..models.reading_session import ReadingSession


class TrackerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_goal(self, user_id):
        return self.db.query(ReadingGoal).filter(
            ReadingGoal.user_id == user_id
        ).first()

    def create_goal(self, data):
        goal = ReadingGoal(**data.model_dump())
        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)
        return goal

    def update_goal(self, goal, data):
        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(goal, key, value)

        self.db.commit()
        self.db.refresh(goal)
        return goal

    def add_reading_session(self, data):
        session = ReadingSession(**data.model_dump())
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_user_sessions(self, user_id):
        return self.db.query(ReadingSession).filter(
            ReadingSession.user_id == user_id
        ).all()