from fastapi import FastAPI, HTTPException
from .schemas import Book
from . import storage

app = FastAPI()

@app.get("/books")
async def get_books():
    return storage.get_all_books()

@app.get("/books/{book_id}")
async def get_book(book_id: int):
    book = storage.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.post("/books")
async def create_book(book: Book):
    storage.add_book(book.dict())
    return {"message": "Book added successfully"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    book = storage.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    storage.delete_book(book_id)
    return {"message": "Book deleted"}
