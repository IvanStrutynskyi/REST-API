from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None
