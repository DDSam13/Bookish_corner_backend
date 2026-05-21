from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.tracker import (
    ReadingGoalCreate,
    ReadingGoalResponse,
    ReadingGoalUpdate,
    ReadingSessionCreate,
    ReadingSessionResponse,
)
from ..services.tracker_service import TrackerService

router = APIRouter(
    prefix="/tracker",
    tags=["Tracker"],
)


@router.get("/goal/{user_id}", response_model=ReadingGoalResponse)
def get_goal(user_id: UUID, db: Session = Depends(get_db)):
    return TrackerService(db).get_goal(user_id)


@router.post("/goal", response_model=ReadingGoalResponse)
def create_goal(data: ReadingGoalCreate, db: Session = Depends(get_db)):
    return TrackerService(db).create_goal(data)


@router.patch("/goal/{user_id}", response_model=ReadingGoalResponse)
def update_goal(
    user_id: UUID,
    data: ReadingGoalUpdate,
    db: Session = Depends(get_db),
):
    return TrackerService(db).update_goal(user_id, data)


@router.post("/session", response_model=ReadingSessionResponse)
def create_session(
    data: ReadingSessionCreate,
    db: Session = Depends(get_db),
):
    return TrackerService(db).create_session(data)


@router.get("/session/{user_id}", response_model=list[ReadingSessionResponse])
def get_sessions(user_id: UUID, db: Session = Depends(get_db)):
    return TrackerService(db).get_sessions(user_id)