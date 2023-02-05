#!/usr/bin/env python3

from core import Application
import math


opr2 = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "//": lambda x, y: x // y,
    "%": lambda x, y: x % y,
    "**": lambda x, y: x**y,
}

opr1 = {
    "1/": lambda x: 1 / x,
    "V": math.sqrt,
    "!": math.factorial,
}

const = {
    "pi": math.pi,
    "pi2": math.pi / 2,
    "e": math.e,
}

app = Application()

app.opr2 = opr2
app.opr1 = opr1
app.const = const

app.opr1["sin"] = lambda x: math.sin(app.goniowrap(x))
app.opr1["cos"] = lambda x: math.cos(app.goniowrap(x))
app.opr1["tan"] = lambda x: math.tan(app.goniowrap(x))
app.opr1["tg"] = lambda x: math.tan(app.goniowrap(x))
app.opr1["asin"] = lambda x: app.a_goniowrap(math.asin(x))
app.opr1["acos"] = lambda x: app.a_goniowrap(math.acos(x))
app.opr1["atan"] = lambda x: app.a_goniowrap(math.atan(x))
app.opr1["atg"] = lambda x: app.a_goniowrap(math.atan(x))


app.mainloop()
