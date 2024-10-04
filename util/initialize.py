import sqlite3
import logging
import os

class Initialize:
    db_path: str = os.getcwd() + "/sqlite/library.db" 

    def __init__(self) -> None:
        self.db_path = os.getcwd() + "/sqlite/library.db"
        self.logger: logging.Logger = logging.getLogger(name=__name__)

    def initialize(self) -> bool:
        return self.initialize_database() and self.initialize_logs()

    def initialize_database(self) -> bool:
        if os.path.exists(self.db_path):
            return True
        success: bool = False
        self.logger.info(msg="Intializing Database")
        if not os.path.exists(path=os.getcwd() + "/sqlite"):
            os.mkdir(path=os.getcwd() + "/sqlite")
        con: sqlite3.Connection = sqlite3.connect(self.db_path)
        create_books_sql: str = "create table books(id integer primary key autoincrement, title text not null, \
            author text not null, available text not null, date_created text not null, check_in_date text, \
            check_out_date text);"
        try:
            _ = con.execute(create_books_sql)
            con.commit()
            self.logger.info(msg="Database Initialized")
            success = True
        except Exception as e:
            con.rollback()
            os.remove(path=self.db_path)
            self.logger.error(msg=f"Failed to Intialize Database: {repr(e)}")
        finally:
            con.close()
            return success

    def initialize_logs(self) -> bool:
        try:
            os.makedirs(name=os.path.dirname("logs/"), exist_ok=True)
            logging.basicConfig(
                filename="logs/library.log",
                encoding="utf-8",
                filemode="a",
                format="{asctime} - {levelname} - {funcName} - {lineno} - {message}",
                style="{",
                datefmt="%Y-%m-%d %H:%M",
                level=logging.DEBUG)
            return True
        except Exception as e:
            print(repr(e))
            return False
