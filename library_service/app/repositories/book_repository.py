from sqlalchemy.orm import Session

from ..models.book import Author, Book, Genre


class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_books(self):
        return self.db.query(Book).all()

    def create_book(self, data):
        author = (
            self.db.query(Author)
            .filter(Author.name == data.author_name)
            .first()
        )

        if not author:
            author = Author(name=data.author_name)
            self.db.add(author)
            self.db.flush()

        genre = (
            self.db.query(Genre)
            .filter(Genre.name == data.genre_name)
            .first()
        )

        if not genre:
            genre = Genre(name=data.genre_name)
            self.db.add(genre)
            self.db.flush()

        book = Book(
            title=data.title,
            description=data.description,
            cover_url=data.cover_url,
            page_count=data.page_count,
            language=data.language,
            author_id=author.id,
            genre_id=genre.id,
        )

        self.db.add(book)

        self.db.commit()
        self.db.refresh(book)

        return book

    def get_book_by_id(self, book_id):
        return (
            self.db.query(Book)
            .filter(Book.id == book_id)
            .first()
        )

    def get_book_by_id(self, book_id):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update_book(self, book: Book, data):
        update_data = data.model_dump(exclude_unset=True)

        author_name = update_data.pop("author_name", None)
        genre_name = update_data.pop("genre_name", None)

        for key, value in update_data.items():
            setattr(book, key, value)

        if author_name:
            author = self.db.query(Author).filter(Author.name == author_name).first()
            if not author:
                author = Author(name=author_name)
                self.db.add(author)
                self.db.flush()
            book.author_id = author.id

        if genre_name:
            genre = self.db.query(Genre).filter(Genre.name == genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
                self.db.add(genre)
                self.db.flush()
            book.genre_id = genre.id

        self.db.commit()
        self.db.refresh(book)
        return book

    def delete_book(self, book: Book):
        self.db.delete(book)
        self.db.commit()