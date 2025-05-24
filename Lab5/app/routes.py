from fastapi import APIRouter, HTTPException
from typing import List
from .database import book_collection
from .models import BookModel
from .schemas import BookCreate, BookUpdate
from pydantic_mongo import PydanticObjectId

router = APIRouter()

@router.post("/books/", response_model=BookModel)
async def create_book(book: BookCreate):
    book_dict = book.dict()
    result = await book_collection.insert_one(book_dict)
    created_book = await book_collection.find_one({"_id": result.inserted_id})
    return BookModel(**created_book)

@router.get("/books/", response_model=List[BookModel])
async def get_books():
    books_cursor = book_collection.find({})
    books = []
    async for book in books_cursor:
        books.append(BookModel(**book))
    return books

@router.get("/books/{book_id}", response_model=BookModel)
async def get_book(book_id: str):
    try:
        obj_id = PydanticObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book id format")

    book = await book_collection.find_one({"_id": obj_id})
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookModel(**book)

@router.put("/books/{book_id}", response_model=BookModel)
async def update_book(book_id: str, book_update: BookUpdate):
    try:
        obj_id = PydanticObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book id format")

    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")

    result = await book_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book = await book_collection.find_one({"_id": obj_id})
    return BookModel(**updated_book)

@router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    try:
        obj_id = PydanticObjectId(book_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid book id format")

    result = await book_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"detail": "Book deleted"}
