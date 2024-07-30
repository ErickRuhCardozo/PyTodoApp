from models.todo import Todo
from views.todolist import TodoList
from tkinter.ttk import Checkbutton, Entry, Button
from tkinter import Tk, IntVar, TOP, LEFT, X, END, BOTH

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title('Todos')
        self.geometry('300x200')
        self.config(padx=5, pady=5)
        
        self.todostate = IntVar(self, 0)
        self.checkbox = Checkbutton(self, variable=self.todostate)
        self.entry = Entry(self)
        self.addbtn = Button(self, text='Add', command=lambda: self.add_todo())
        self.list = TodoList(self)

        self.list.pack(side=TOP, fill=BOTH, expand=True)
        self.checkbox.pack(side=LEFT)
        self.entry.pack(side=LEFT, fill=X, expand=True)
        self.addbtn.pack(side=LEFT, padx=(5, 0))
        self.mainloop()
    

    def add_todo(self):
        done = self.todostate.get()
        title = self.entry.get()
        todo = Todo(0, title, done)
        self.list.controller.add(todo)
        self.todostate.set(0)
        self.entry.delete(0, END)
        self.entry.focus()


