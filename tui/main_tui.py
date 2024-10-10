import shutil
import os
import logging
from typing import Literal, override
from tui.book_tui import BookTui
from tui.tui import Tui
from util.initialize import Initialize

running: bool = True

# TUI Loop
def tui() -> Literal[0]:
    initializer: Initialize = Initialize()
    if initializer.initialize():
        main_tui: MainTui = MainTui()
        while running:
            _ = os.system(command="clear")
            main_tui.print_dir()
            _ = os.system(command="clear")
    return 0

class MainTui(Tui):
    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(name=__name__)
        self.book_tui: BookTui = BookTui()
        self.dir_list: list[str] = ["BOOKS", "EXIT"]
        self.dir_dict: dict[str, str] = self.create_dir_dict()
        self.init_util: Initialize = Initialize()
        # Converting into a dictionary so that we can add new directories
        # without having to change indexes for navigation logic


    @override
    def create_dir_dict(self) -> dict[str, str]:
        dir_dict: dict[str, str] = {}
        for i in range(0, len(self.dir_list)):
            dir_dict.update({str(i + 1): self.dir_list[i]})
        return dir_dict

    @override
    def print_header(self, content: str) -> None:
        _ = os.system(command="clear")
        term_size: os.terminal_size = shutil.get_terminal_size(fallback=(80, 20))
        print("".center(term_size.columns, '-'))
        print(content.center(term_size.columns))
        print("".center(term_size.columns, '-'))
        print()
        print()


    @override
    def print_dir(self) -> None:
        for i in range(1, len(self.dir_dict) + 1):
            print(f"{i}. {self.dir_dict.get(str(i))}")
        try:
            dir: str = input()
            self.logger.debug(msg=f"User input in main dir: {dir}")
            self.dir_resolver(user_input=dir)
        except ValueError as e:
            self.logger.error(msg=repr(e))
            _ = input("INVALID INPUT. PRESS ENTER TO CONTINUE.")
            _ = tui()


    @override
    def dir_resolver(self, user_input: str) -> None:
        if self.dir_dict.get(user_input) == "BOOKS":
            self.logger.debug(msg="User entering book dir.")
            self.book_tui.print_dir()
        elif self.dir_dict.get(user_input) == "EXIT":
            self.logger.info(msg="User exiting system.")
            _ = os.system(command="clear")
            global running
            running = False
            return
        else:
            raise ValueError(f"Invalid Input Detected: {dir}")


_ = tui()
