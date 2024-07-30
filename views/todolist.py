from models.todo import Todo
from tkinter.ttk import Checkbutton, Frame
from controllers.todocontroller import TodoController
from tkinter import TOP, W, IntVar, Menu, Variable
from tkinter.ttk import Checkbutton, Frame


class TodoList(Frame):
    def  __init__(self, master):
        super().__init__(master)
        self.controls: list[dict[Variable, Checkbutton, Todo]] = []
        self.controller = TodoController()
        self.controller.on_loaded(lambda: self.loaded())
        self.controller.on_added(lambda t: self.added(t))
        self.controller.on_removed(lambda t: self.removed(t))
        self.controller.load()


    def loaded(self):
        for todo in self.controller.todos:
            ctrl = self.create_item(todo)
            self.controls.append(ctrl)
            ctrl['btn'].pack(side=TOP, anchor=W)


    def added(self, todo: Todo):
        ctrl = self.create_item(todo)
        self.controls.append(ctrl)
        ctrl['btn'].pack(side=TOP, anchor=W)


    def removed(self, todo: Todo):
        for ctrl in self.controls:
            if ctrl['todo'] == todo:
                ctrl['btn'].pack_forget()
                self.controls.remove(ctrl)
                break


    def create_item(self, todo: Todo) -> dict[Variable, Checkbutton, Todo]:
        var = IntVar(self, int(todo.done))

        def onclick():
            todo.done = bool(var.get())
            self.controller.update_done(todo)

        btn = Checkbutton(self, text=todo.title, variable=var, onvalue=1, offvalue=0, command=onclick)
        menu = Menu(btn, tearoff=False)
        menu.add_command(label='Delete', command=lambda: self.controller.remove(todo))
        btn.bind('<Button-3>', lambda e: menu.post(e.x_root, e.y_root))
        return {'var': var, 'btn':  btn, 'todo': todo}