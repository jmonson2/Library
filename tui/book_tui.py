import shutil
import os
import logging
import sys
from model.book import Book
from db import book_db

logger: logging.Logger = logging.getLogger(name=__name__)


def print_header(content: str) -> None:
    _ = os.system(command = "clear")
    term_size: os.terminal_size = shutil.get_terminal_size(fallback=(80, 20))
    print("".center(term_size.columns, '-'))
    print(content.center(term_size.columns))
    print("".center(term_size.columns, '-'))
    print()
    print()


def print_book_dir() -> None:
    dir_list: list[str] = ["CHECKOUT BOOK", "CHECK-IN BOOK", "FIND BOOK", "LIST BOOKS",
                "ADD BOOK", "MAIN DIRECTORY", "EXIT"]
    dir_dict: dict[str, str] = {}
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})
    print_header(content = "BOOK DIRECTORY")
    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    try:
        dir: str = input()
        logger.debug(msg=f"User input in book dir: {dir}")
        dir_resolver(dir_dict, user_input=dir)
    except ValueError as e:
        logger.error(msg=repr(e))
        print("INVALID INPUT. PRESS ENTER TO CONTINUE.")
        _ = input()
        return


def print_all_books() -> None:
    print_header(content="ALL BOOKS")
    books: list[Book] | None = book_db.get_all_books()
    print(format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
    if books:
        for book in books:
            print(book.tui_format())
    _ = input("PRESS ENTER TO CONTINUE")


# TODO may need to create a generic util class to format all types of output
def format_output(content: tuple[str, str, str] | list[str]) -> str:
    term_size: os.terminal_size = shutil.get_terminal_size(fallback = (80, 20))
    output: str = content[0]

    while (term_size.columns // 2) > len(output) + 3:
        output += " "
    output += content[1]

    while term_size.columns > len(output + content[2]):
        output += " "
    output += content[2]

    return output


def print_add_book_dir() -> None:
    print_header(content="ADD BOOK")
    title: str = input("BOOK TITLE: ")
    author: str = input("AUTHOR: ")
    available: str = input("AVAILABILITY (Y/N): ")
    new_book: Book = Book(title=title, author=author, available=available)
    if book_db.add_book(book=new_book):
        print("BOOK ADDED SUCCESSFULLY")
        logger.info(msg=f"Book added by user: {title}")
    else:
        logger.error(msg=f"Book not able to be added: {title};{author};{available}")
        print("BOOK ADDED UNSUCESSFULLY")
    _ = input()


def print_check_out_book()-> None:
    print_header(content="CHECKOUT BOOK")
    title: str = input("BOOK TITLE: ")
    books: list[str] | None = book_db.get_book_by_title_for_checkout(title)
    print()
    if books:
        book_dict: dict[str,str] = {}
        for i in range(0, len(books)):
            book_dict.update({str(i + 1): books[i][0]})
            print(f"{i + 1}. {book_dict.get(str(i + 1))}")
        book: str = input("BOOK TO CHECKOUT: ")
        if book_db.checkout_book_by_title(title=book_dict.get(book)):
            print("BOOK CHECKED IN")
        else:
            print("BOOK CHECKED OUT")
    else:
        print("NO BOOKS FOUND")
    _ = input()


def print_check_in_book() -> None:
    print_header(content="CHECK-IN BOOK")
    title: str = input("BOOK TITLE: ")
    books: list[str] | None = book_db.get_book_by_title_for_check_in(title)
    print()
    if books:
        book_dict: dict[str, str] = {}
        for i in range(0, len(books)):
            book_dict.update({str(i + 1): books[i][0]})
            print(f"{i + 1}. {book_dict.get(str(i + 1))}")
        book: str = input("BOOK TO CHECK-IN: ")
        if book_db.checkin_book_by_title(title=book_dict.get(book)):
            print("BOOK CHECKED IN")
        else:
            print("BOOK NOT CHECKED IN")
    else:
        print("NO BOOKS FOUND")
    _ = input()


def print_find_book_dir():
    print_header(content="FIND BOOK")

    dir_list: list[str] = ["SEARCH BY TITLE", "SEARCH BY AUTHOR",
                "SEARCH BY AVAILABILITY"]
    dir_dict:dict[str, str] = {}
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})

    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    dir_resolver(dir_dict, user_input=input())


def print_find_book_by_title():
    _ = os.system(command="clear")
    print_header(content="SEARCH BOOKS BY TITLE")
    title:str = input("BOOK TITLE: ")
    books:list [Book] | None = book_db.get_book_by_title(title)
    print()
    if books:
        print(format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(book.tui_format())
    else:
        print("NO BOOKS FOUND")
    _ = input()


def print_find_book_by_author():
    _ = os.system(command="clear")
    print_header(content="SEARCH BOOKS BY AUTHOR")
    author:str = input("BOOK AUTHOR: ")
    books:list[Book] | None = book_db.get_book_by_author(author)
    print()
    if books:
        print(format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(book.tui_format())
    else:
        print("NO BOOKS FOUND")
    _ = input()


def print_find_book_by_availability():
    _ = os.system(command="clear")
    print_header(content="SEARCH BOOKS BY AVAILABILITY")
    availability:str = input("BOOK AVAILABILITY (Y/N): ")
    books:list[Book] | None = book_db.get_book_by_availability(availability)
    print()
    if books:
        print(format_output(content=("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(book.tui_format())
    else:
        print("NO BOOKS FOUND")
    _= input()


def dir_resolver(dir_dict: dict[str, str], user_input: str) -> None:
    if dir_dict.get(user_input) == "FIND BOOK":
        logger.debug(msg="User searching books.")
        print_find_book_dir()
    elif dir_dict.get(user_input) == "CHECKOUT BOOK":
        logger.debug(msg="User checking out a book.")
        print_check_out_book()
    elif dir_dict.get(user_input) == "CHECK-IN BOOK":
        logger.debug(msg="User checking in a book.")
        print_check_in_book()
    elif dir_dict.get(user_input) == "LIST BOOKS":
        logger.debug(msg="User listing all books.")
        print_all_books()
    elif dir_dict.get(user_input) == "MAIN DIRECTORY":
        logger.debug(msg="User returning to main directory.")
        return
    elif dir_dict.get(user_input) == "ADD BOOK":
        logger.debug(msg="User adding book.")
        try:
            print_add_book_dir()
        except Exception as e:
            logger.error(msg=repr(e))
    elif dir_dict.get(user_input) == "SEARCH BY TITLE":
        logger.debug(msg="User is searching for book by title.")
        print_find_book_by_title()
    elif dir_dict.get(user_input) == "SEARCH BY AUTHOR":
        logger.debug(msg="User is searching for book by author.")
        print_find_book_by_author()
    elif dir_dict.get(user_input) == "SEARCH BY AVAILABILITY":
        logger.debug(msg="User is searching for book by availability.")
        print_find_book_by_availability()
    elif dir_dict.get(user_input) == "EXIT":
        logger.info(msg="User exiting system.")
        _ = os.system(command="clear")
        sys.exit()
    else:
        raise ValueError(f"Invalid Input Detected: {dir}")
