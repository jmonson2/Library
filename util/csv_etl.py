from typing import override
from util.abstract_etl import AbstractETL
from util.paths import Paths
from pathlib import Path
from model.book import Book
from db.book_db import BookDB
import csv

class CsvETL(AbstractETL):

    def __init__(self) -> None:
        self.__paths = Paths()
        self.__files: set[Path] = self.__get_fd_for_import()
        self.__book_db: BookDB = BookDB()
        self.__list_dict_books: list[dict[str, str]] = []
        self.__books: list[Book] = []

    @override
    def extract(self) -> None:
        for csv_path in self.__get_fd_for_import():
            with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.__list_dict_books.append(row)

    @override
    def transform(self) -> None:
        for b_dict in self.__list_dict_books:
            self.__books.append(
                Book(
                     title=b_dict.get("Title"),
                     author=b_dict.get("Author"),
                     available=b_dict.get("Available")
                )
            )

    @override
    def load(self) -> None:
        for book in self.__books:
            _ = self.__book_db.add_book(book)

    @override
    def run(self) -> None:
        self.extract()
        self.transform()
        self.load()
        
    def __get_fd_for_import(self) -> set[Path]:
        csv_filenames: set[Path] = set()
        csv_files = Path.glob(self.__paths.import_path, "*.csv")
        for csv_file in csv_files:
            csv_filenames.add(csv_file)
        return csv_filenames


test = CsvETL()
test.run()
