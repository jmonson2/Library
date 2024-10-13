import sqlite3
import logging
from datetime import datetime

from model.book import Book
from util.paths import Paths

class BookDB:

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name = __name__)
        self.paths: Paths = Paths()


    def add_books(self, books: list[Book]) -> bool:
        conn: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        cursor: sqlite3.Cursor = conn.cursor()
        try:
            cursor.executemany(
                "insert into books (title, author, date_created, available) values (?, ?, ?, ?);",
                [(book.title, book.author, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), book.available) for book in books]
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Issue adding books to database: {repr(e)}")
            return False
        finally:
            conn.close()


    def add_book(self, book: Book) -> bool:
        time: datetime = datetime.now()
        con: sqlite3.Connection= sqlite3.connect(self.paths.db_file_path)
        try:
            sql = "insert into books (title, author, date_created, available) \
                values (?, ?, ?, ?);"
            data: tuple[str, str, str, str] = (book.title, book.author, time.strftime(
                    format = "%d/%m/%Y %H:%M:%S"), book.available)
            _ = con.execute(sql, data)
            con.commit()
            self.logger.info(f"Book added: {repr(book)}")
            return True
        except Exception as e:
            con.rollback()
            self.logger.error(msg=f"Issue adding book to database: {repr(e)}")
            return False
        finally:
            con.close()


    def checkout_book(self, id: int | None) -> bool:
        time: datetime = datetime.now()
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"update books set available = 'N', check_out_date = \
            '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where id =  \
            {id} and available = 'Y';"
            update_count: int = con.execute(sql).rowcount
            con.commit()
            if update_count > 0:
                self.logger.info(msg=f"Book checked out: {id}")
                return True
            elif update_count == 0:
                self.logger.info(msg=f"Book not checked out: {id}")
            return False
        except Exception as e:
            con.rollback()
            self.logger.error(msg=f"Issue checking out book {id}: {repr(e)}")
            return False
        finally:
            con.close()


    def checkout_book_by_title(self, title: str | None) -> bool:
        time: datetime = datetime.now()
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"update books set available = 'N', check_out_date = \
            '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
                upper('{title}') and available = 'Y';"
            update_count: int = con.execute(sql).rowcount
            con.commit()
            if update_count > 0:
                self.logger.info(msg=f"Book checked out: {title}")
                return True
            elif update_count == 0:
                self.logger.info(msg=f"Book not checked out: {title}")
            return False
        except Exception as e:
            con.rollback()
            self.logger.error(msg=f"Issue checking out book {title}: {repr(e)}")
            return False
        finally:
            con.close()


    def checkin_book_by_title(self, title: str | None) -> bool:
        time: datetime = datetime.now()
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"update books set available = 'Y', check_in_date = \
            '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where upper(title) =  \
                upper('{title}');"
            update_count: int = con.execute(sql).rowcount
            if update_count > 0:
                self.logger.info(msg=f"Book checked in: {title}")
            elif update_count == 0:
                self.logger.info(msg=f"Book not checked in: {title}")
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            self.logger.error(msg=f"Issue checking in book {title}: {repr(e)}")
            return False
        finally:
            con.close()


    def checkin_book(self, id: int | None) -> bool:
        time: datetime = datetime.now()
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"update books set available = 'Y', check_in_date = \
            '{time.strftime(format = "%d/%m/%Y %H:%M:%S")}' where id =  \
                {id};"
            update_count: int = con.execute(sql).rowcount
            if update_count > 0:
                self.logger.info(msg=f"Book checked in: {id}")
            elif update_count == 0:
                self.logger.info(msg=f"Book not checked in: {id}")
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            self.logger.error(msg=f"Issue checking in book {id}: {repr(e)}")
            return False
        finally:
            con.close()


    def get_book_by_title_for_checkout(self, title: str)  -> list[str] | None:
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"select title from books where upper(title) \
                like upper('%{title}%') and available = 'Y'"
            cur: sqlite3.Cursor = con.execute(sql)
            books: list[str] = cur.fetchall()
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by title {
                        title}: {repr(e)}")
        finally:
            con.close()


    def get_book_by_title_for_check_in(self, title: str) -> list[str] | None:
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"select title from books where upper(title) \
                like upper('%{title}%') and available = 'N'"
            cur: sqlite3.Cursor = con.execute(sql)
            books: list[str] = cur.fetchall()
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by title {
                        title}: {repr(e)}")
        finally:
            con.close()


    def get_book_by_title(self, title : str) -> list[Book] | None:
        books: list[Book] = []
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"select id, title, author, available from books where upper(title) \
                like upper('%{title}%')"
            cur: sqlite3.Cursor = con.execute(sql)
            results: list[str] = cur.fetchall()
            for result in results:
                books.append(Book(id=int(result[0]), title=result[1], author=result[2], available=result[3]))        
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by title {
                        title}: {repr(e)}")
        finally:
            con.close()


    def get_books_for_checkout(self, title: str) -> list[str] | None:
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        self.logger.debug(f"Getting books for checkout: {title}")
        try:
            sql: str = f"select title, author, available from books where upper(title) \
                like upper('%{title}%') and available = 'Y'"
            cur: sqlite3.Cursor = con.execute(sql)
            books: list[str] = cur.fetchall()
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by title {
                        title}: {repr(e)}")
        finally:
            con.close()


    def get_book_by_author(self, author: str) -> list[Book] | None:
        books: list[Book] = []
        self.logger.debug(f"Getting books by author: {author}")
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"select id, title, author, available from books where \
            upper(author) like upper('%{author}%')"
            cur: sqlite3.Cursor = con.execute(sql)
            results: list[str] = cur.fetchall()
            for result in results:
                books.append(Book(id = int(result[0]), title=result[1], author=result[2], available=result[3]))
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by author {
                        author}: {repr(e)}")
        finally:
            con.close()


    def get_book_by_availability(self, availability: str) -> list[Book] | None:
        books: list[Book] = []
        self.logger.debug(f"Getting books by availability: {availability}")
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql: str = f"select id, title, author, available from books where \
            upper(available) like upper('%{availability}%')"
            cur: sqlite3.Cursor = con.execute(sql)
            results: list[str] = cur.fetchall()
            for result in results:
                books.append(Book(id = int(result[0]), title=result[1], author=result[2], available=result[3]))
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue while searching for book by availability {
                        availability}: {repr(e)}")
        finally:
            con.close()


    def get_all_books(self) -> list[Book] | None:
        books: list[Book] = []
        self.logger.debug("Getting all books")
        con: sqlite3.Connection = sqlite3.connect(self.paths.db_file_path)
        try:
            sql = "select id, title, author, available from books;"
            cur: sqlite3.Cursor = con.execute(sql)
            results: list[str] = cur.fetchall()
            for result in results:
                books.append(Book(id=int(result[0]), title=result[1], author=result[2], available=result[3]))
            return books
        except Exception as e:
            self.logger.error(msg=f"Issue getting all books from database: {repr(e)}")
        finally:
            con.close()
