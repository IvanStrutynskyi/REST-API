from flask import Blueprint, jsonify, request
from .models import db, Book
from .schemas import book_schema, books_schema
from marshmallow import ValidationError

bp = Blueprint('books', __name__, url_prefix='/books')


@bp.route('', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    cursor = request.args.get('cursor', type=int)

    if limit < 1:
        return jsonify({"error": "Limit must be positive"}), 400

    query = Book.query.order_by(Book.id.asc())

    if cursor:
        query = query.filter(Book.id > cursor)

    books = query.limit(limit).all()
    serialized_books = books_schema.dump(books)
    next_cursor = books[-1].id if books else None

    return jsonify({
        "books": serialized_books,
        "next_cursor": next_cursor
    }), 200


@bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found")
    return book_schema.jsonify(book), 200


@bp.route('', methods=['POST'])
def add_book():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        book = book_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    db.session.add(book)
    db.session.commit()
    return book_schema.jsonify(book), 201


@bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id, description=f"Book with id {book_id} not found")
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": f"Book with id {book_id} deleted"}), 200
