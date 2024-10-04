import shutil
import os
import logging
import sys
from typing import override
from model.book import Book
from db.book_db import Book_DB
from tui.tui import Tui


class Book_Tui(Tui):
    def __init__(self) -> None:
        self.book_db: Book_DB = Book_DB()
        self.logger: logging.Logger = logging.getLogger(name=__name__)
        self.dir_name: str = "BOOK DIRECTORY"
        self.dir_list: list[str] = ["CHECKOUT BOOK", "CHECK-IN BOOK", "FIND BOOK", "LIST BOOKS",
                    "ADD BOOK", "MAIN DIRECTORY", "EXIT"]
        self.dir_dict = self.create_dir_dict()

    @override
    def create_dir_dict(self) -> dict[str, str]:
        dir_dict: dict[str, str] = {}
        for i in range(0, len(self.dir_list)):
            dir_dict.update({str(i + 1): self.dir_list[i]})
        return dir_dict


    @override
    def print_header(self, content: str) -> None:
        _ = os.system(command = "clear")
        term_size: os.terminal_size = shutil.get_terminal_size(fallback=(80, 20))
        print("".center(term_size.columns, '-'))
        print(content.center(term_size.columns))
        print("".center(term_size.columns, '-'))
        print()
        print()


    @override
    def print_dir(self) -> None:
        dir_dict: dict[str, str] = {}
        for i in range(0, len(self.dir_list)):
            dir_dict.update({str(i + 1): self.dir_list[i]})
        self.print_header(content = self.dir_name)
        for i in range(1, len(dir_dict) + 1):
            print(f"{i}. {dir_dict.get(str(i))}")
        try:
            dir: str = input()
            self.logger.debug(msg=f"User input in book dir: {dir}")
            self.dir_resolver(user_input=dir)
        except ValueError as e:
            self.logger.error(msg=repr(e))
            print("INVALID INPUT. PRESS ENTER TO CONTINUE.")
            _ = input()
            return


    @override
    def dir_resolver(self, user_input: str) -> None:
        if self.dir_dict.get(user_input) == "FIND BOOK":
            self.logger.debug(msg="User searching books.")
            self.print_find_book_dir()
        elif self.dir_dict.get(user_input) == "CHECKOUT BOOK":
            self.logger.debug(msg="User checking out a book.")
            self.print_check_out_book()
        elif self.dir_dict.get(user_input) == "CHECK-IN BOOK":
            self.logger.debug(msg="User checking in a book.")
            self.print_check_in_book()
        elif self.dir_dict.get(user_input) == "LIST BOOKS":
            self.logger.debug(msg="User listing all books.")
            self.print_all_books()
        elif self.dir_dict.get(user_input) == "MAIN DIRECTORY":
            self.logger.debug(msg="User returning to main directory.")
            return
        elif self.dir_dict.get(user_input) == "ADD BOOK":
            self.logger.debug(msg="User adding book.")
            try:
                self.print_add_book_dir()
            except Exception as e:
                self.logger.error(msg=repr(e))
        elif self.dir_dict.get(user_input) == "SEARCH BY TITLE":
            self.logger.debug(msg="User is searching for book by title.")
            self.print_find_book_by_title()
        elif self.dir_dict.get(user_input) == "SEARCH BY AUTHOR":
            self.logger.debug(msg="User is searching for book by author.")
            self.print_find_book_by_author()
        elif self.dir_dict.get(user_input) == "SEARCH BY AVAILABILITY":
            self.logger.debug(msg="User is searching for book by availability.")
            self.print_find_book_by_availability()
        elif self.dir_dict.get(user_input) == "EXIT":
            self.logger.info(msg="User exiting system.")
            _ = os.system(command="clear")
            sys.exit()
        else:
            raise ValueError(f"Invalid Input Detected: {dir}")


    def print_all_books(self) -> None:
        self.print_header(content="ALL BOOKS")
        books: list[Book] | None = self.book_db.get_all_books()
        print(self.format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
        if books:
            for book in books:
                print(book.tui_format())
        _ = input("PRESS ENTER TO CONTINUE")


    def format_output(self, content: tuple[str, str, str] | list[str]) -> str:
        term_size: os.terminal_size = shutil.get_terminal_size(fallback = (80, 20))
        output: str = content[0]

        while (term_size.columns // 2) > len(output) + 3:
            output += " "
        output += content[1]

        while term_size.columns > len(output + content[2]):
            output += " "
        output += content[2]

        return output


    def print_add_book_dir(self) -> None:
        self.print_header(content="ADD BOOK")
        title: str = input("BOOK TITLE: ")
        author: str = input("AUTHOR: ")
        available: str = input("AVAILABILITY (Y/N): ")
        new_book: Book = Book(title=title, author=author, available=available)
        if self.book_db.add_book(book=new_book):
            print("BOOK ADDED SUCCESSFULLY")
            self.logger.info(msg=f"Book added by user: {title}")
        else:
            self.logger.error(msg=f"Book not able to be added: {title};{author};{available}")
            print("BOOK ADDED UNSUCESSFULLY")
        _ = input()


    def print_check_out_book(self)-> None:
        self.print_header(content="CHECKOUT BOOK")
        title: str = input("BOOK TITLE: ")
        books: list[str] | None = self.book_db.get_book_by_title_for_checkout(title)
        print()
        if books:
            book_dict: dict[str,str] = {}
            for i in range(0, len(books)):
                book_dict.update({str(i + 1): books[i][0]})
                print(f"{i + 1}. {book_dict.get(str(i + 1))}")
            book: str = input("BOOK TO CHECKOUT: ")
            if self.book_db.checkout_book_by_title(title=book_dict.get(book)):
                print("BOOK CHECKED IN")
            else:
                print("BOOK CHECKED OUT")
        else:
            print("NO BOOKS FOUND")
        _ = input()


    def print_check_in_book(self) -> None:
        self.print_header(content="CHECK-IN BOOK")
        title: str = input("BOOK TITLE: ")
        books: list[str] | None = self.book_db.get_book_by_title_for_check_in(title)
        print()
        if books:
            book_dict: dict[str, str] = {}
            for i in range(0, len(books)):
                book_dict.update({str(i + 1): books[i][0]})
                print(f"{i + 1}. {book_dict.get(str(i + 1))}")
            book: str = input("BOOK TO CHECK-IN: ")
            if self.book_db.checkin_book_by_title(title=book_dict.get(book)):
                print("BOOK CHECKED IN")
            else:
                print("BOOK NOT CHECKED IN")
        else:
            print("NO BOOKS FOUND")
        _ = input()


    def print_find_book_dir(self) -> None:
        self.print_header(content="FIND BOOK")

        dir_list: list[str] = ["SEARCH BY TITLE", "SEARCH BY AUTHOR",
                    "SEARCH BY AVAILABILITY"]
        dir_dict:dict[str, str] = {}
        for i in range(0, len(dir_list)):
            dir_dict.update({str(i + 1): dir_list[i]})

        for i in range(1, len(dir_dict) + 1):
            print(f"{i}. {dir_dict.get(str(i))}")
        self.dir_resolver(user_input=input())


    def print_find_book_by_title(self) -> None:
        _ = os.system(command="clear")
        self.print_header(content="SEARCH BOOKS BY TITLE")
        title:str = input("BOOK TITLE: ")
        books:list [Book] | None = self.book_db.get_book_by_title(title)
        print()
        if books:
            print(self.format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
            for book in books:
                print(book.tui_format())
        else:
            print("NO BOOKS FOUND")
        _ = input()


    def print_find_book_by_author(self) -> None:
        _ = os.system(command="clear")
        self.print_header(content="SEARCH BOOKS BY AUTHOR")
        author:str = input("BOOK AUTHOR: ")
        books:list[Book] | None = self.book_db.get_book_by_author(author)
        print()
        if books:
            print(self.format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
            for book in books:
                print(book.tui_format())
        else:
            print("NO BOOKS FOUND")
        _ = input()


    def print_find_book_by_availability(self) -> None:
        _ = os.system(command="clear")
        self.print_header(content="SEARCH BOOKS BY AVAILABILITY")
        availability:str = input("BOOK AVAILABILITY (Y/N): ")
        books:list[Book] | None = self.book_db.get_book_by_availability(availability)
        print()
        if books:
            print(self.format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
            for book in books:
                print(book.tui_format())
        else:
            print("NO BOOKS FOUND")
        _= input()
