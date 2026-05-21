from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.book import BookCreate, BookResponse
from ..services.book_service import BookService
from uuid import UUID

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

@router.get("/{book_id}", response_model=BookResponse)
def get_book_by_id(
    book_id: UUID,
    db: Session = Depends(get_db),
):
    book = BookService(db).get_book_by_id(book_id)

    return BookResponse(
        id=book.id,
        title=book.title,
        description=book.description,
        cover_url=book.cover_url,
        page_count=book.page_count,
        language=book.language,
        author_name=book.author.name if book.author else None,
        genre_name=book.genre.name if book.genre else None,
    )