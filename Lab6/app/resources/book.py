from flask_restful import Resource, reqparse
from flasgger import swag_from
import asyncio
from app.database import book_collection

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Title of the book is required")
parser.add_argument("author", type=str, required=True, help="Author of the book is required")

class BookResource(Resource):

    @swag_from({
        'responses': {
            200: {
                'description': 'List of books',
                'examples': {
                    'application/json': [
                        {'_id': '1', 'title': 'Book 1', 'author': 'Author 1'},
                        {'_id': '2', 'title': 'Book 2', 'author': 'Author 2'}
                    ]
                }
            }
        }
    })
    def get(self, book_id=None):
        # синхронний виклик асинхронної функції через asyncio.run
        if book_id:
            book = asyncio.run(self.get_book(book_id))
            if book:
                return book, 200
            return {"message": "Book not found"}, 404
        else:
            books = asyncio.run(self.get_books())
            return books, 200

    @swag_from({
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'title': {'type': 'string'},
                        'author': {'type': 'string'}
                    },
                    'required': ['title', 'author']
                }
            }
        ],
        'responses': {
            201: {'description': 'Book created successfully'}
        }
    })
    def post(self):
        args = parser.parse_args()
        new_book = {
            "title": args["title"],
            "author": args["author"]
        }
        result = asyncio.run(book_collection.insert_one(new_book))
        return {"message": "Book created", "id": str(result.inserted_id)}, 201

    async def get_books(self):
        books = []
        cursor = book_collection.find()
        async for document in cursor:
            document["_id"] = str(document["_id"])
            books.append(document)
        return books

    async def get_book(self, book_id):
        from bson import ObjectId
        document = await book_collection.find_one({"_id": ObjectId(book_id)})
        if document:
            document["_id"] = str(document["_id"])
        return document
