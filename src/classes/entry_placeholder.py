# Third party imports
import tkinter as tk


class EntryPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="", color="grey", cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master,  cnf, **kw)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self["fg"]

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def get(self):
        if self["fg"] == self.placeholder_color:
            return ""
        return super().get()

    def insert(self, index, string):
        if not self.get():
            self.delete("0", "end")
            self["fg"] = self.default_fg_color
        super().insert(index, string)

    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

    def foc_in(self, *args):
        if self["fg"] == self.placeholder_color:
            self.delete("0", "end")
            self["fg"] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
