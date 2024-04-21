from uuid import uuid4
from fastapi import FastAPI
import random
from fastapi import HTTPException
import os
import json
from mangum import Mangum
from pydantic import BaseModel
from typing import Literal, Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI()
handler = Mangum(app)

# Book Model


class Book(BaseModel):
    title: str
    price: float
    book_id: Optional[str] = uuid4().hex
    genre: Literal["fiction", "non-fiction"]


BOOKS_FILE = "books.json"
BOOK_DATABASE = []

if os.path.exists(BOOKS_FILE):
    with open(BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)

# /


@app.get("/")
async def root():
    return {"message": "Welcome to my bookstore!"}

# /list-books


@app.get("/list-books")
async def list_books():
    return {"books": BOOK_DATABASE}


# /book-by-index/{index}
@app.get("/book-by-index/{index}")
async def get_book_by_index(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(status_code=404,
                            detail=f"Index {index} is out of range {len(BOOK_DATABASE)}")

    return {"book": BOOK_DATABASE[index]}

# /get-random-book


@app.get("/get-random-book")
async def get_random_book():
    return {"book": random.choice(BOOK_DATABASE)}

# /add-book


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
    return {"message": f"Book {book} added successfully", "book_id": book.book_id}


# /get-book?id={id}
@app.get("/get-book")
async def get_book(book_id: str):
    for book in BOOK_DATABASE:
        if book["book_id"] == book_id:
            return {"book": book}
    raise HTTPException(status_code=404, detail=f"Book {book_id} not found")
