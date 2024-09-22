import shutil
import os
import logging
import sys
from model.book import Book
from db import book_db

logger = logging.getLogger(__name__)


def print_header(content):
    os.system("clear")
    term_size = shutil.get_terminal_size((80, 20))
    print("".center(term_size.columns, '-'))
    print(content.center(term_size.columns))
    print("".center(term_size.columns, '-'))
    print()
    print()


def print_book_dir():
    dir_list = ["CHECKOUT BOOK", "CHECK-IN BOOK", "FIND BOOK", "LIST BOOKS",
                "ADD BOOK", "MAIN DIRECTORY", "EXIT"]
    dir_dict = {}
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})
    print_header("BOOK DIRECTORY")
    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    try:
        dir = input()
        logger.debug(f"User input in book dir: {dir}")
        dir_resolver(dir_dict, dir)
    except ValueError as e:
        logger.error(repr(e))
        print("INVALID INPUT. PRESS ENTER TO CONTINUE.")
        input()
        return


def print_all_books():
    print_header("ALL BOOKS")
    books = book_db.get_all_books()
    print(format_output(("TITLE", "AUTHOR", "AVAILABLE")))
    for book in books:
        print(format_output(book))
    input("PRESS ENTER TO CONTINUE")


# TODO may need to create a generic util class to format all types of output
def format_output(content):
    term_size = shutil.get_terminal_size((80, 20))
    output = content[0]

    while (term_size.columns // 2) > len(output) + 3:
        output += " "
    output += content[1]

    while term_size.columns > len(output + content[2]):
        output += " "
    output += content[2]

    return output


def print_add_book_dir():
    print_header("ADD BOOK")
    title = input("BOOK TITLE: ")
    author = input("AUTHOR: ")
    available = input("AVAILABILITY (Y/N): ")
    new_book = Book(title, author, available)
    if book_db.add_book(new_book):
        print("BOOK ADDED SUCCESSFULLY")
    else:
        print("BOOK ADDED UNSUCESSFULLY")
    input()


def print_check_out_book():
    print_header("CHECKOUT BOOK")
    title = input("BOOK TITLE: ")
    books = book_db.get_book_by_title_for_checkout(title)
    print()
    if books:
        book_dict = {}
        for i in range(0, len(books)):
            book_dict.update({str(i + 1): books[i][0]})
            print(f"{i + 1}. {book_dict.get(str(i + 1))}")
        title = input("BOOK TO CHECKOUT: ")
        book_db.check_out_book(book_dict.get(title))
    else:
        print("NO BOOKS FOUND")
    input()


def print_check_in_book():
    print_header("CHECK-IN BOOK")
    title = input("BOOK TITLE: ")
    books = book_db.get_book_by_title_for_check_in(title)
    print()
    if books:
        book_dict = {}
        for i in range(0, len(books)):
            book_dict.update({str(i + 1): books[i][0]})
            print(f"{i + 1}. {book_dict.get(str(i + 1))}")
        title = input("BOOK TO CHECK-IN: ")
        book_db.check_in_book(book_dict.get(title))
    else:
        print("NO BOOKS FOUND")
    input()


def print_find_book_dir():
    print_header("FIND BOOK")

    dir_list = ["SEARCH BY TITLE", "SEARCH BY AUTHOR",
                "SEARCH BY AVAILABILITY"]
    dir_dict = {}
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})

    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    dir_resolver(dir_dict, input())


def print_find_book_by_title():
    os.system("clear")
    print_header("SEARCH BOOKS BY TITLE")
    title = input("BOOK TITLE: ")
    books = book_db.get_book_by_title(title)
    print()
    if books:
        print(format_output(("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(format_output(book))
    else:
        print("NO BOOKS FOUND")
    input()


def print_find_book_by_author():
    os.system("clear")
    print_header("SEARCH BOOKS BY AUTHOR")
    author = input("BOOK AUTHOR: ")
    books = book_db.get_book_by_author(author)
    print()
    if books:
        print(format_output(("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(format_output(book))
    else:
        print("NO BOOKS FOUND")
    input()


def print_find_book_by_availability():
    os.system("clear")
    print_header("SEARCH BOOKS BY AVAILABILITY")
    availability = input("BOOK AVAILABILITY (Y/N): ")
    books = book_db.get_book_by_availability(availability)
    print()
    if books:
        print(format_output(("TITLE", "AUTHOR", "AVAILABLE")))
        for book in books:
            print(format_output(book))
    else:
        print("NO BOOKS FOUND")
    input()


def dir_resolver(dir_dict, user_input):
    if dir_dict.get(user_input) == "FIND BOOK":
        logger.debug("User searching books.")
        print_find_book_dir()
    elif dir_dict.get(user_input) == "CHECKOUT BOOK":
        logger.debug("User checking out a book.")
        print_check_out_book()
    elif dir_dict.get(user_input) == "CHECK-IN BOOK":
        logger.debug("User checking in a book.")
        print_check_in_book()
    elif dir_dict.get(user_input) == "LIST BOOKS":
        logger.debug("User listing all books.")
        print_all_books()
    elif dir_dict.get(user_input) == "MAIN DIRECTORY":
        logger.debug("User returning to main directory.")
        return
    elif dir_dict.get(user_input) == "ADD BOOK":
        logger.debug("User adding book.")
        try:
            print_add_book_dir()
        except Exception as e:
            logger.error(repr(e))
    elif dir_dict.get(user_input) == "SEARCH BY TITLE":
        logger.debug("User is searching for book by title.")
        print_find_book_by_title()
    elif dir_dict.get(user_input) == "SEARCH BY AUTHOR":
        logger.debug("User is searching for book by author.")
        print_find_book_by_author()
    elif dir_dict.get(user_input) == "SEARCH BY AVAILABILITY":
        logger.debug("User is searching for book by availability.")
        print_find_book_by_availability()
    elif dir_dict.get(user_input) == "EXIT":
        logger.info("User exiting system.")
        os.system("clear")
        sys.exit()
    else:
        raise ValueError(f"Invalid Input Detected: {dir}")
