import shutil
from typing import override


class Book:

    def __init__(self, title: str, author: str, available: str) -> None:
        self.title = title
        self.author = author
        self.available = available

# Validate if the data is clean and does not already exist in the database
    def validate(self):
        pass

    def checkout(self):
        pass

    @override
    def __repr__(self) -> str:
        term_size = shutil.get_terminal_size(fallback = (80, 20))
        output: str = self.title

        while (term_size.columns // 2) > len(output) + 3:
            output += " "
        output += self.author

        while term_size.columns > len(output + self.available):
            output += " "
        output += self.available

        return output
