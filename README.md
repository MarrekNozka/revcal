RevCal
===============

`revcal` is graphics calculator with 
[reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation).

Features
--------------

* easy to use GUI
* full control from keyboard
* easy adding own math operation ans own constants
* Issues are welcome

![](shot.png)


Keys
--------

* `Tab`: switch between stack and entry
* `Up`, `Down`: focus item in stack
* `Shift+Up`, `Shift+Down`: move item in stack

Commands
----------

* `rad`, `deg`: switch between radians and degrees. 
* `c`, `cp`: copy item in stack
* `d`, `del`: remove item from stack
* `s`, `swap`: swap last two items in stack
* `Q`: quit


Math and constansts
-----------------------

All is vary easy to configure in
[`main.py`](main.py). Just add the key to dictionary
`opr2` or `opr1`. Dictionary `opr2` contains function witch two parametrs and `opr1`
contains function with one parameter.

Similary dictionary `const` contains constants.

In goniometric functions is used function `goniowrap` and `a_goniowrap`. It is
importent for possibility of radians and degrees switching.
