from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.book_repository import BookRepository


class BookService:
    def __init__(self, db: Session):
        self.repository = BookRepository(db)

    def get_books(self):
        return self.repository.get_all_books()

    def create_book(self, data):
        return self.repository.create_book(data)

    def get_book_by_id(self, book_id):
        book = self.repository.get_book_by_id(book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена",
            )

        return book

    def get_book_by_id(self, book_id):
        book = self.repository.get_book_by_id(book_id)

        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена",
            )

        return book

    def update_book(self, book_id, data):
        book = self.get_book_by_id(book_id)
        return self.repository.update_book(book, data)

    def delete_book(self, book_id):
        book = self.get_book_by_id(book_id)
        self.repository.delete_book(book)

        return {
            "message": "Книга удалена",
            "book_id": str(book_id),
        }