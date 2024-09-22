import sqlite3
import os
import logging
from datetime import datetime

LIBRARY = os.getcwd() + "/sqlite/library.db"
logger = logging.getLogger(__name__)


def add_book(book):
    time = datetime.now()
    try:
        con = sqlite3.connect(LIBRARY)
        sql = "insert into books (title, author, date_created, available) \
               values (?, ?, ?, ?);"
        data = (book.title, book.author, time.strftime(
                "%d/%m/%Y %H:%M:%S"), book.available)
        con.execute(sql, data)
        con.commit()
        con.close()
        return True
    except Exception as e:
        con.rollback()
        con.close()
        print("BOOK ADDED UNSUCCESSFULLY")
        logger.error(f"Issue adding book to database: {repr(e)}")
        return False


def edit_book(book):
    pass


def delete_book(book):
    pass


def check_out_book(title):
    time = datetime.now()
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"update books set available = 'N', check_out_date = \
        '{time.strftime("%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
            upper('{title}') and available = 'Y';"
        update_count = con.execute(sql).rowcount
        if update_count > 0:
            print("BOOK CHECKED OUT")
        elif update_count == 0:
            print("BOOK NOT FOUND")
        con.commit()
        con.close()
        return True
    except Exception as e:
        con.rollback()
        con.close()
        logger.error(f"Issue checking out book {title}: {repr(e)}")
        print("ERROR WHILE CHECKING OUT BOOK")
        return False


def check_in_book(title):
    time = datetime.now()
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"update books set available = 'N', check_in_date = \
        '{time.strftime("%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
            upper('{title}');"
        update_count = con.execute(sql).rowcount
        if update_count > 0:
            print("BOOK CHECKED IN")
        elif update_count == 0:
            print("BOOK NOT FOUND")
        con.commit()
        con.close()
        return True
    except Exception as e:
        con.rollback()
        con.close()
        logger.error(f"Issue checking in book {title}: {repr(e)}")
        print("ERROR CHECKING IN BOOK")
        return False


def get_book_by_title_for_checkout(title):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title from books where upper(title) \
            like upper('%{title}%') and available = 'Y'"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by title {
                     title}: {repr(e)}")


def get_book_by_title_for_check_in(title):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title from books where upper(title) \
            like upper('%{title}%') and available = 'N'"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by title {
                     title}: {repr(e)}")


def get_book_by_title(title):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title, author, available from books where upper(title) \
            like upper('%{title}%')"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by title {
                     title}: {repr(e)}")


def get_books_for_checkout(title):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title, author, available from books where upper(title) \
            like upper('%{title}%') and available = 'Y'"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by title {
                     title}: {repr(e)}")


def get_book_by_author(author):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title, author, available from books where \
        upper(author) like upper('%{author}%')"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by author {
                     author}: {repr(e)}")


def get_book_by_availability(availability):
    try:
        con = sqlite3.connect(LIBRARY)
        sql = f"select title, author, available from books where \
        upper(available) like upper('%{availability}%')"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books

    except Exception as e:
        con.close()
        logger.error(f"Issue while searching for book by availability {
                     availability}: {repr(e)}")


def get_all_books():
    try:
        con = sqlite3.connect(LIBRARY)
        sql = "select title, author, available from books;"
        cur = con.execute(sql)
        books = cur.fetchall()
        con.close()
        return books
    except Exception as e:
        con.close()
        logger.error(f"Issue getting all books from database: {repr(e)}")
