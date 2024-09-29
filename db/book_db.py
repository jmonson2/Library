import sqlite3
import os
import logging
from datetime import datetime
from model.book import Book
LIBRARY: str = os.getcwd() + "/sqlite/library.db"
logger: logging.Logger = logging.getLogger(name = __name__)


def add_book(book: Book) -> bool:
    time: datetime = datetime.now()
    con: sqlite3.Connection= sqlite3.connect(LIBRARY)
    try:
        sql = "insert into books (title, author, date_created, available) \
               values (?, ?, ?, ?);"
        data: tuple[str, str, str, str] = (book.title, book.author, time.strftime(
                format = "%d/%m/%Y %H:%M:%S"), book.available)
        _ = con.execute(sql, data)
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        print("BOOK ADDED UNSUCCESSFULLY")
        logger.error(msg=f"Issue adding book to database: {repr(e)}")
        return False
    finally:
        con.close()


def check_out_book(title: str | None) -> bool:
    time: datetime = datetime.now()
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"update books set available = 'N', check_out_date = \
        '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
            upper('{title}') and available = 'Y';"
        update_count: int = con.execute(sql).rowcount
        if update_count > 0:
            print("BOOK CHECKED OUT")
            logger.info(msg=f"Book checked out: {title}")
        elif update_count == 0:
            print("BOOK NOT FOUND")
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        logger.error(msg=f"Issue checking out book {title}: {repr(e)}")
        print("ERROR WHILE CHECKING OUT BOOK")
        return False
    finally:
        con.close()

def check_in_book(title: str | None) -> bool:
    time: datetime = datetime.now()
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"update books set available = 'Y', check_in_date = \
        '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
            upper('{title}');"
        update_count: int = con.execute(sql).rowcount
        if update_count > 0:
            print("BOOK CHECKED IN")
            logger.info(msg=f"Book checked in: {title}")
        elif update_count == 0:
            print("BOOK NOT FOUND")
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        logger.error(msg=f"Issue checking in book {title}: {repr(e)}")
        print("ERROR CHECKING IN BOOK")
        return False
    finally:
        con.close()

def get_book_by_title_for_checkout(title: str)  -> list[str] | None:
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"select title from books where upper(title) \
            like upper('%{title}%') and available = 'Y'"
        cur: sqlite3.Cursor = con.execute(sql)
        books: list[str] = cur.fetchall()
        return books

    except Exception as e:
        logger.error(msg=f"Issue while searching for book by title {
                     title}: {repr(e)}")
    finally:
        con.close()

def get_book_by_title_for_check_in(title: str) -> list[str] | None:
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"select title from books where upper(title) \
            like upper('%{title}%') and available = 'N'"
        cur: sqlite3.Cursor = con.execute(sql)
        books: list[str] = cur.fetchall()
        return books

    except Exception as e:
        logger.error(msg=f"Issue while searching for book by title {
                     title}: {repr(e)}")
    finally:
        con.close()

def get_book_by_title(title : str) -> list[Book] | None:
    books: list[Book] = []
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"select title, author, available from books where upper(title) \
            like upper('%{title}%')"
        cur: sqlite3.Cursor = con.execute(sql)
        results: list[str] = cur.fetchall()
        for result in results:
            books.append(Book(title=result[0], author=result[1], available=result[2]))        
        return books
    except Exception as e:
        logger.error(msg=f"Issue while searching for book by title {
                     title}: {repr(e)}")
    finally:
        con.close()

def get_books_for_checkout(title: str) -> list[str] | None:
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    logger.debug(f"Getting books for checkout: {title}")
    try:
        sql: str = f"select title, author, available from books where upper(title) \
            like upper('%{title}%') and available = 'Y'"
        cur: sqlite3.Cursor = con.execute(sql)
        books: list[str] = cur.fetchall()
        return books
    except Exception as e:
        logger.error(msg=f"Issue while searching for book by title {
                     title}: {repr(e)}")
    finally:
        con.close()


def get_book_by_author(author: str) -> list[Book] | None:
    books: list[Book] = []
    logger.debug(f"Getting books by author: {author}")
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"select title, author, available from books where \
        upper(author) like upper('%{author}%')"
        cur: sqlite3.Cursor = con.execute(sql)
        results: list[str] = cur.fetchall()
        for result in results:
            books.append(Book(title=result[0], author=result[1], available=result[2]))
        return books
    except Exception as e:
        logger.error(msg=f"Issue while searching for book by author {
                     author}: {repr(e)}")
    finally:
        con.close()


def get_book_by_availability(availability: str) -> list[Book] | None:
    books: list[Book] = []
    logger.debug(f"Getting books by availability: {availability}")
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql: str = f"select title, author, available from books where \
        upper(available) like upper('%{availability}%')"
        cur: sqlite3.Cursor = con.execute(sql)
        results: list[str] = cur.fetchall()
        for result in results:
            books.append(Book(title=result[0], author=result[1], available=result[2]))        
        return books
    except Exception as e:
        logger.error(msg=f"Issue while searching for book by availability {
                     availability}: {repr(e)}")
    finally:
        con.close()


def get_all_books() -> list[Book] | None:
    books: list[Book] = []
    logger.debug("Getting all books")
    con: sqlite3.Connection = sqlite3.connect(LIBRARY)
    try:
        sql = "select title, author, available from books;"
        cur: sqlite3.Cursor = con.execute(sql)
        results: list[str] = cur.fetchall()
        for result in results:
            books.append(Book(title=result[0], author=result[1], available=result[2]))
        return books
    except Exception as e:
        logger.error(msg=f"Issue getting all books from database: {repr(e)}")
    finally:
        con.close()
