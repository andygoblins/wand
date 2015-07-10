#!/usr/bin/env python

import sys
from tkinter import *
from tkinter import ttk

class Wand(ttk.Frame):
    def __init__(self, filename):
        ttk.Frame.__init__(self, master=None)
        try:
            with open(filename, 'r') as file:
                buf = file.read()
                self.master.title(filename)
        except FileNotFoundError:
            buf = ''
            self.master.title('Untitled')

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
            
        self.grid(sticky=N+S+E+W)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.editor = Text(self)
        self.editor.insert(0.0, buf)
        self.editor.grid(row=0, column=0, sticky=N+S+E+W)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = ''

    wand = Wand(filename)
    wand.mainloop()
