from sqlalchemy.orm import Session

from ..models.reading_goal import ReadingGoal
from ..models.reading_session import ReadingSession


class TrackerRepository:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def goal_to_response(goal: ReadingGoal | None):
        if goal is None:
            return None

        return {
            "id": goal.id,
            "user_id": goal.user_id,
            "year": goal.year,
            "books_target": goal.target_books_count,
            "books_completed": goal.completed_books_count,
            "created_at": goal.created_at,
            "updated_at": goal.updated_at,
        }

    def get_user_goal_model(self, user_id):
        return (
            self.db.query(ReadingGoal)
            .filter(ReadingGoal.user_id == user_id)
            .first()
        )

    def get_user_goal(self, user_id):
        goal = self.get_user_goal_model(user_id)
        return self.goal_to_response(goal)

    def create_goal(self, data):
        goal = ReadingGoal(
            user_id=data.user_id,
            year=data.year,
            target_books_count=data.books_target,
            completed_books_count=data.books_completed,
        )

        self.db.add(goal)
        self.db.commit()
        self.db.refresh(goal)

        return self.goal_to_response(goal)

    def update_goal(self, goal, data):
        # goal может прийти как dict после get_user_goal(),
        # поэтому достаём настоящую SQLAlchemy-модель из БД
        if isinstance(goal, dict):
            goal = self.get_user_goal_model(goal["user_id"])

        update_data = data.model_dump(exclude_unset=True)

        if "year" in update_data:
            goal.year = update_data["year"]

        if "books_target" in update_data:
            goal.target_books_count = update_data["books_target"]

        if "books_completed" in update_data:
            goal.completed_books_count = update_data["books_completed"]

        self.db.commit()
        self.db.refresh(goal)

        return self.goal_to_response(goal)

    def add_reading_session(self, data):
        session = ReadingSession(**data.model_dump())

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_user_sessions(self, user_id):
        return (
            self.db.query(ReadingSession)
            .filter(ReadingSession.user_id == user_id)
            .all()
        )