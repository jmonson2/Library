from abc import ABC, abstractmethod

class AbstractETL(ABC):

    @abstractmethod
    def extract(self) -> None:
        pass 


    @abstractmethod
    def transform(self) -> None:
        pass


    @abstractmethod
    def load(self) -> None:
        pass


    @abstractmethod
    def run(self) -> None:
        pass
