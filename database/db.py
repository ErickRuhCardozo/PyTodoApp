from os.path import exists
from sqlite3 import Connection, connect


class Db:
    NAME = 'todos.db3'


    @classmethod
    def exists(cls) -> bool:
        return exists(cls.NAME)

    
    @classmethod
    def create(cls):
        if cls.exists():
            return
        
        with connect(cls.NAME) as conn:
            cls.create_schema(conn)


    @classmethod
    def connect(cls) -> Connection:
        return connect(cls.NAME)


    @staticmethod
    def create_schema(conn: Connection):
        conn.execute('CREATE TABLE todos (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done INTEGER)')