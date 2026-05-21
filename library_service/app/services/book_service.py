from sqlalchemy.orm import Session

from ..repositories.book_repository import BookRepository


class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    def get_books(self):
        return self.repository.get_all_books()

    def create_book(self, data):
        return self.repository.create_book(data)