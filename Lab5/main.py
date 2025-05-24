from fastapi import FastAPI
from app.routes import router as book_router

app = FastAPI(title="Library API with FastAPI and MongoDB")

app.include_router(book_router)
