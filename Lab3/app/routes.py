from flask import Blueprint, jsonify, request
from .models import db, Book
from .schemas import book_schema, books_schema
from marshmallow import ValidationError

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('', methods=['GET'])
def get_books():
    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    if limit < 1 or offset < 0:
        return jsonify({"error": "Invalid pagination parameters"}), 400

    books = Book.query.offset(offset).limit(limit).all()
    return jsonify(books_schema.dump(books)), 200

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
