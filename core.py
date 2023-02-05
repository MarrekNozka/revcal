#!/usr/bin/env python3

import tkinter as tk
from tkinter import font
import operator
import math

# from tkinter import ttk


class MyEntry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        if "textvariable" not in kw:
            self.variable = tk.StringVar()
            self.config(textvariable=self.variable)
        else:
            self.variable = kw["textvariable"]

    @property
    def value(self):
        return self.variable.get()

    @value.setter
    def value(self, new: str):
        self.variable.set(new)


class Application(tk.Tk):
    name = "RevCal"
    opr2 = {
        "+": operator.add,
        "-": lambda x, y: x - y,
    }

    opr1 = {
        "1/": lambda x: 1 / x,
        "V": math.sqrt,
    }

    const = {
        "pi": math.pi,
        "e": math.e,
    }

    def __init__(self):
        super().__init__(className=self.name)
        self.title(self.name)

        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=18, family="Terminus TTF")

        self.goniowrap = self.rad2rad
        self.a_goniowrap = self.rad2rad
        self.opr1["sin"] = lambda x: math.sin(self.goniowrap(x))
        self.opr1["asin"] = lambda x: self.a_goniowrap(math.asin(x))

        self.listFrame = tk.Frame(self)
        self.entry = MyEntry(self, font=default_font, takefocus=True)
        self.statusFrame = tk.Frame(self)
        self.listFrame.pack(fill="both", expand=1)
        self.entry.pack(anchor="w", fill="both")
        self.statusFrame.pack(fill="both", expand=1)

        self.listbox = tk.Listbox(self.listFrame, width=33, takefocus=True)
        self.btnFrame = tk.Frame(self.listFrame)
        self.listbox.pack(side="left", fill="both", expand=1)
        self.btnFrame.pack(side="left", anchor="s", expand=0, fill="y")

        self.upupBtn = tk.Button(
            self.btnFrame, text="🡅🡅🡅", width=5, command=self.upup, takefocus=False
        )
        self.upBtn = tk.Button(
            self.btnFrame, text=" 🡅 ", width=5, command=self.up, takefocus=False
        )
        self.downBtn = tk.Button(
            self.btnFrame, text=" 🡇 ", width=5, command=self.down, takefocus=False
        )
        self.downdownBtn = tk.Button(
            self.btnFrame, text="🡇🡇🡇", width=5, command=self.downdown, takefocus=False
        )
        self.copyBtn = tk.Button(
            self.btnFrame, text="Copy", width=5, command=self.copy, takefocus=False
        )
        self.deleteBtn = tk.Button(
            self.btnFrame, text="Delete", width=5, command=self.delete, takefocus=False
        )
        self.quitBtn = tk.Button(
            self.btnFrame, text="Quit", width=5, command=self.quit, takefocus=False
        )
        self.emptyFrame = tk.Frame(self.btnFrame, height=33)
        self.quitBtn.pack(side="top")
        self.emptyFrame.pack(expand=1, fill="both")
        self.copyBtn.pack(side="top", pady=3)
        self.deleteBtn.pack(side="top", pady=3)
        self.upupBtn.pack(anchor="n")
        self.upBtn.pack(anchor="n")
        self.downBtn.pack(anchor="n")
        self.downdownBtn.pack(anchor="n")

        self.statusLbl = tk.Label(self.statusFrame, text=">")
        self.gonioBtn = tk.Button(
            self.statusFrame,
            text="RAD",
            width=3,
            command=self.gonioswitch,
            takefocus=False,
        )
        self.statusLbl.pack(side="left", anchor="w")
        self.gonioBtn.pack(side="right")

        self.entry.focus_set()

        self.bind("<Tab>", self.focusswitch)
        self.bind("<Escape>", self.clear)
        # self.listbox.bind("<ButtonRelease-1>", self.click_handler)
        self.listbox.bind("<Shift-Up>", self.up)
        self.listbox.bind("<Shift-Down>", self.down)

        self.entry.bind("<Return>", self.process)
        self.entry.bind("<KP_Enter>", self.process)

        self.offset = 12  # to add items to stack from bottom
        for _ in range(self.offset):
            self.listbox.insert("end", "")

    @property
    def size(self):
        return self.listbox.size() - self.offset

    def status(self, msg):
        self.statusLbl.config(text=msg)

    def process(self, e: tk.Event):
        for v in self.entry.value.split():
            self.token_process(v)
        self.entry.value = ""

    def token_process(self, token: str):
        try:
            token = token.replace(",", ".")
            value = float(token)
            self.listbox.insert("end", value)
            # self.listbox.select_set("end")
            self.listbox.select_anchor("end")
            self.listbox.activate("end")
            self.listbox.see("end")
            self.status(f"> {self.size}")
        except ValueError:
            if token in self.opr2:
                if self.size >= 2:
                    b = self.listbox.get("end")
                    self.listbox.delete("end")
                    a = self.listbox.get("end")
                    self.listbox.delete("end")
                    self.listbox.insert("end", self.opr2[token](a, b))
                    self.status(f"> {self.size}")
                else:
                    self.status("Error: Too few items in stack!")
            if token in self.opr1:
                if self.size >= 1:
                    a = self.listbox.get("end")
                    self.listbox.delete("end")
                    self.listbox.insert("end", self.opr1[token](a))
                    self.status(f"> {self.size}")
                else:
                    self.status("Error: Too few items in stack!")
            if token in self.const:
                self.listbox.insert("end", self.const[token])
                self.status(f"> {self.size}")
            if token == "rad":
                self.goniowrap = self.rad2rad
                self.a_goniowrap = self.rad2rad
                self.gonioBtn.config(text="RAD")
            if token == "deg":
                self.goniowrap = self.deg2rad
                self.a_goniowrap = self.rad2deg
                self.gonioBtn.config(text="DEG")
            if token == "Q":
                self.quit()
            self.listbox.see("end")

    def click_handler(self, e: tk.Event):
        print(self.listbox.curselection()[0])
        print(self.listbox.get("active"))
        print(self.listbox.get("anchor"))

    def focusswitch(self, e: tk.Event):
        self.listbox.focus_set()

    def gonioswitch(self):
        if self.gonioBtn.cget("text") == "RAD":
            self.goniowrap = self.deg2rad
            self.a_goniowrap = self.rad2deg
            self.gonioBtn.config(text="DEG")
        else:
            self.goniowrap = self.deg2rad
            self.a_goniowrap = self.rad2deg
            self.gonioBtn.config(text="RAD")

    def upup(self, e: tk.Event = None):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
        if i - self.offset >= 0:
            item = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(self.offset, item)
            self.listbox.select_set(self.offset)
            self.listbox.select_anchor(self.offset)
            self.listbox.activate(self.offset)
            self.listbox.see("end")

    def up(self, e: tk.Event = None):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
        if i - self.offset >= 1:
            item = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i - 1, item)
            self.listbox.select_set(i - 1)
            self.listbox.select_anchor(i - 1)
            self.listbox.activate(i - 1)
            self.listbox.see("end")

    def down(self, e: tk.Event = None):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
            print("E", end="")
        if i < self.listbox.size() - 1:
            item = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert(i + 1, item)
            self.listbox.select_set(i + 1)
            self.listbox.select_anchor(i + 1)
            self.listbox.activate(i + 1)
            self.listbox.see("end")

    def downdown(self, e: tk.Event = None):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
        if i - self.offset >= 0:
            item = self.listbox.get(i)
            self.listbox.delete(i)
            self.listbox.insert("end", item)
            self.listbox.select_set("end")
            self.listbox.select_anchor("end")
            self.listbox.activate("end")
            self.listbox.see("end")

    def copy(self):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
            print("E", end="")
        if i >= self.offset:
            item = self.listbox.get(i)
            self.listbox.insert(i, item)
            self.listbox.select_set(i)
            self.listbox.select_anchor(i)
            self.listbox.activate(i)
            self.listbox.see("end")
            self.status(f"> {self.size}")

    def delete(self):
        try:
            i = self.listbox.curselection()[0]
        except IndexError:
            i = self.listbox.index("active")
            print("E", end="")
        if i >= self.offset:
            self.listbox.delete(i)
            self.listbox.select_set(i - 1)
            self.listbox.select_anchor(i - 1)
            self.listbox.activate(i - 1)
            self.listbox.see("end")
            self.status(f"> {self.size}")

    def key_handler(self, e: tk.Event):
        print(e.keycode, e.keysym, e.keysym_num)

    def rad2rad(self, x):
        return x

    def deg2rad(self, x):
        return math.radians(x)

    def rad2deg(self, x):
        return math.degrees(x)

    def clear(self, e: tk.Event):
        self.entry.value = ""

    def quit(self, event=None):
        super().quit()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
