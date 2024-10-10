from fastapi import FastAPI
from model.book import Book
from db.book_db import BookDB
import logging

logging.basicConfig(
    filename="logs/library.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {funcName} - {lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG)

app: FastAPI = FastAPI()
book_db: BookDB = BookDB()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Please see /docs"}


@app.get("/books")
async def get_all_books() -> list[Book] | None:
    return(book_db.get_all_books())


@app.get("/books/available/{available}")
async def get_books_by_availability(available: str) -> list[Book] | None:
    return book_db.get_book_by_availability(available)


@app.get("/books/author/{author}")
async def get_books_by_author(author: str) -> list[Book] | None:
    return book_db.get_book_by_author(author)


@app.get("/books/title/{title}")
async def get_books_by_title(title: str) -> list[Book] | None:
    return book_db.get_book_by_title(title)


@app.put("/books/add")
async def add_book(book: Book) -> dict[str, str]:
    if book_db.add_book(book):
        return {"message": "Book added."}
    return {"message": "Book not added."}


@app.patch("/books/checkout")
async def checkout_books(ids: list[int]) -> dict[str, str]:
    if ids:
        for id in ids:
            _ = book_db.checkout_book(id)
        return {"message": "Book(s) checked out."}
    return {"message": "Book(s) not checked out."}


@app.patch("/books/checkin")
async def checkin_books(ids: list[int]) -> dict[str, str]:
    if ids:
        for id in ids:
            _ = book_db.checkin_book(id)
        return {"message": "Book(s) checked in."}
    return {"message": "Book(s) not checked in."}
