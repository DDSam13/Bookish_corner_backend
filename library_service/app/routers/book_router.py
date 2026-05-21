from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.book import BookCreate, BookResponse
from ..services.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.get("/", response_model=list[BookResponse])
def get_books(
    db: Session = Depends(get_db),
):
    return BookService(db).get_books()


@router.post("/", response_model=BookResponse)
def create_book(
    data: BookCreate,
    db: Session = Depends(get_db),
):
    return BookService(db).create_book(data)