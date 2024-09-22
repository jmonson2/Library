import shutil
import os
import logging

from db import book_db
from tui import user_tui, book_tui

os.makedirs(os.path.dirname("logs/"), exist_ok=True)
running = True
logging.basicConfig(
    filename="logs/library.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {funcName} - {lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG)
logger = logging.getLogger(__name__)


def cli(argv=None):
    while running:
        os.system("clear")
        print_main_dir()
        os.system("clear")
    exit(0)


def print_header():
    term_size = shutil.get_terminal_size((80, 20))
    print("".center(term_size.columns, '-'))
    print("LIBRARY CLI".center(term_size.columns))
    print("".center(term_size.columns, '-'))
    print()
    print()


def print_main_dir():
    dir_list = ["BOOKS", "EXIT"]
    dir_dict = {}
# Converting into a dictionary so that we can add new directories
# without having to change indexes for navigation logic
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})
    print_header()
    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    try:
        dir = input()
        logger.debug(f"User input in main dir: {dir}")
        dir_resolver(dir_dict, dir)
    except ValueError as e:
        logger.error(repr(e))
        print("INVALID INPUT. PRESS ENTER TO CONTINUE.")
        input()
        cli()


def dir_resolver(dir_dict, user_input):
    if dir_dict.get(user_input) == "BOOKS":
        logger.debug("User entering book dir.")
        book_tui.print_book_dir()
    elif dir_dict.get(user_input) == "EXIT":
        logger.info("User exiting system.")
        os.system("clear")
        global running
        running = False
        return
    else:
        raise ValueError(f"Invalid Input Detected: {dir}")


cli()
