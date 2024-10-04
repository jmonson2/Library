from abc import abstractmethod

class Tui:
    @abstractmethod
    def print_header(self, content: str) -> None:
        pass


    @abstractmethod
    def print_dir(self) -> None:
        pass


    @abstractmethod
    def dir_resolver(self, user_input: str) -> None:
        pass

    @abstractmethod
    def create_dir_dict(self) -> dict[str, str]:
        pass
