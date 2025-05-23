from flask import Flask, request, jsonify
from .schemas import BookSchema
from .storage import get_all_books, get_book_by_id, add_book, delete_book

app = Flask(__name__)
book_schema = BookSchema()

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(get_all_books()), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(book), 200

@app.route('/books', methods=['POST'])
def create_book():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    # Валідація
    try:
        validated_data = book_schema.load(json_data)
    except Exception as err:
        return jsonify({"error": err.messages}), 400

    # Додаємо книгу
    add_book(validated_data)
    return jsonify(validated_data), 201

@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    book = get_book_by_id(book_id)
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    delete_book(book_id)
    return jsonify({"message": "Book deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
