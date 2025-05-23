books = []

def get_all_books():
    return books

def get_book_by_id(book_id: int):
    return next((book for book in books if book['id'] == book_id), None)

def add_book(book: dict):
    books.append(book)

def delete_book(book_id: int):
    global books
    books = [book for book in books if book['id'] != book_id]
