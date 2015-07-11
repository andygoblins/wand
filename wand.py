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
            
        self.pack(fill=BOTH, expand=1)
        
        self.editor = Text(self)
        self.editor.insert(0.0, buf)
        self.editor.pack(side=LEFT, fill=BOTH, expand=1)
        
        self.scrollY = ttk.Scrollbar(self, orient=VERTICAL, command=self.editor.yview)
        self.scrollY.pack(side=RIGHT, fill=Y)
        self.editor['yscrollcommand'] = self.scrollY.set

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = ''

    wand = Wand(filename)
    wand.mainloop()
