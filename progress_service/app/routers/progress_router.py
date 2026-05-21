from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.progress import (
    ProgressCreate,
    ProgressResponse,
    ProgressUpdate,
)
from ..services.progress_service import ProgressService

router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)


@router.get("/{user_id}", response_model=list[ProgressResponse])
def get_user_progress(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    return ProgressService(db).get_user_progress(user_id)


@router.post("/", response_model=ProgressResponse)
def create_progress(
    data: ProgressCreate,
    db: Session = Depends(get_db),
):
    return ProgressService(db).create_progress(data)


@router.patch("/{user_id}/{book_id}", response_model=ProgressResponse)
def update_progress(
    user_id: UUID,
    book_id: UUID,
    data: ProgressUpdate,
    db: Session = Depends(get_db),
):
    return ProgressService(db).update_progress(user_id, book_id, data)