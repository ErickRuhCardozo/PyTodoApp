from database.db import Db
from models.todo import Todo
from dataclasses import asdict
from typing import Callable


class TodoController:
    def __init__(self):
        self.todos: list[Todo] = []
        self.added_handlers: list[Callable[[Todo], None]] = []
        self.removed_handlers: list[Callable[[Todo], None]] = []
        self.loaded_handlers: list[Callable[[], None]] = []


    def load(self):
        with Db.connect() as conn:
            cursor = conn.execute('SELECT * FROM todos')
            
            for id, title, done in cursor.fetchall():
                self.todos.append(Todo(id, title, bool(done)))

            for callback in self.loaded_handlers:
                callback()

    
    def on_loaded(self, callback: Callable[[], None]):
        self.loaded_handlers.append(callback)
    

    def add(self, todo: Todo):
        with Db.connect() as conn:
            cursor = conn.execute('INSERT INTO todos VALUES (NULL, :title, :done)', asdict(todo))
            if cursor.rowcount > 0:
                self.todos.append(todo)
                for callback in self.added_handlers:
                    callback(todo)
    

    def on_added(self, callback: Callable[[Todo], None]):
        self.added_handlers.append(callback)

    
    def update_done(self, todo: Todo):
        """Updates the 'done' column for the given Todo."""
        with Db.connect() as conn:
            conn.execute('UPDATE todos SET done=:done WHERE id=:id', asdict(todo))
    

    def remove(self, todo: Todo):
        with Db.connect() as conn:
            cursor = conn.execute('DELETE FROM todos WHERE id=:id', asdict(todo))
            if cursor.rowcount > 0:
                self.todos.remove(todo)
                for callback in self.removed_handlers:
                    callback(todo)
    

    def on_removed(self, callback: Callable[[Todo], None]):
        self.removed_handlers.append(callback)
