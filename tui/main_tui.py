import shutil
import os
import logging
from typing import Literal
from tui import book_tui
from db import init_db

os.makedirs(name=os.path.dirname("logs/"), exist_ok=True)
running = True
logging.basicConfig(
    filename="logs/library.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {funcName} - {lineno} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    level=logging.DEBUG)
logger: logging.Logger = logging.getLogger(name=__name__)


def cli() -> Literal[0]:
    while running:
        _ = os.system(command="clear")
        print_main_dir()
        _ = os.system(command="clear")
    return 0


def print_header() -> None:
    _ = os.system(command="clear")
    term_size: os.terminal_size = shutil.get_terminal_size(fallback=(80, 20))
    print("".center(term_size.columns, '-'))
    print("LIBRARY CLI".center(term_size.columns))
    print("".center(term_size.columns, '-'))
    print()
    print()


def print_main_dir() -> None:
    if not init_db.exists_database():
        _ = input("DATABASE NOT FOUND, INITIALIZING DATABASE. PRESS ENTER TO CONTINUE")
        if not init_db.create_database():
            _ = input("DATABASE COULD NOT BE CREATED. SHUTTING DOWN")
            global running
            running = False
            return
    dir_list: list[str] = ["BOOKS", "EXIT"]
    dir_dict: dict[str, str] = {}
    # Converting into a dictionary so that we can add new directories
    # without having to change indexes for navigation logic
    for i in range(0, len(dir_list)):
        dir_dict.update({str(i + 1): dir_list[i]})
    print_header()
    for i in range(1, len(dir_dict) + 1):
        print(f"{i}. {dir_dict.get(str(i))}")
    try:
        dir: str = input()
        logger.debug(msg=f"User input in main dir: {dir}")
        dir_resolver(dir_dict, user_input=dir)
    except ValueError as e:
        logger.error(msg=repr(e))
        _ = input("INVALID INPUT. PRESS ENTER TO CONTINUE.")
        _ = cli()


def dir_resolver(dir_dict:dict[str, str], user_input: str) -> None:
    if dir_dict.get(user_input) == "BOOKS":
        logger.debug(msg="User entering book dir.")
        book_tui.print_book_dir()
    elif dir_dict.get(user_input) == "EXIT":
        logger.info(msg="User exiting system.")
        _ = os.system(command="clear")
        global running
        running = False
        return
    else:
        raise ValueError(f"Invalid Input Detected: {dir}")


_ = cli()
