books = []
book_id_counter = 1

def get_all_books():
    return books

def get_book_by_id(book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None

def add_book(book_data):
    global book_id_counter
    book_data["id"] = book_id_counter
    books.append(book_data)
    book_id_counter += 1
    return book_data

def delete_book(book_id):
    global books
    for book in books:
        if book["id"] == book_id:
            books = [b for b in books if b["id"] != book_id]
            return True
    return False
