from os import terminal_size
import shutil
from pydantic import BaseModel

class Book(BaseModel):
    title: str
    author: str
    available: str

    def format(self) -> str:
        term_size: terminal_size = shutil.get_terminal_size(fallback = (80, 20))
        output: str = self.title

        while (term_size.columns // 2) > len(output) + 3:
            output += " "
        output += self.author

        while term_size.columns > len(output + self.available):
            output += " "
        output += self.available
        return output
