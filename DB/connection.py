from sqlite3 import connect, Cursor
from os import getenv

class SQLiteConnection():
    def __init__(self) -> None:
        self.conn = connect(getenv('PATH_TO_DB'))
        self.cur = Cursor(self.conn)
    
    def __enter__(self, *args, **kwargs):
        return self
    
    def __exit__(self, *args, **kwargs):
        self.conn.commit()
        self.conn.close()