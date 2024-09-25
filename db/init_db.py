import sqlite3
import logging
import os

logger: logging.Logger = logging.getLogger(name=__name__)
db_path: str = os.getcwd() + "/sqlite/library.db" 


def exists_database() -> bool:
    return True if os.path.exists(path=db_path) else False

def create_database() -> bool:
    success: bool = False
    logger.info(msg="Intializing Database")
    if not os.path.exists(path=os.getcwd() + "/sqlite"):
        os.mkdir(path=os.getcwd() + "/sqlite")
    con: sqlite3.Connection = sqlite3.connect(db_path)
    create_books_sql: str = "create table books(id integer primary key autoincrement, title text not null, \
        author text not null, available text not null, date_created text not null, check_in_date text, \
        check_out_date text);"
    try:
        _ = con.execute(create_books_sql)
        con.commit()
        logger.info(msg="Database Initialized")
        success = True
    except Exception as e:
        con.rollback()
        os.remove(path=db_path)
        logger.error(msg=f"Failed to Intialize Database: {repr(e)}")
    finally:
        con.close()
        return success