from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from .models import Book

class BookSchema(SQLAlchemySchema):
    class Meta:
        model = Book
        load_instance = True

    id = auto_field(dump_only=True)
    title = auto_field(required=True)
    author = auto_field(required=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
