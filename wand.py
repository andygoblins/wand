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
        
        self.menu = SamMenu(self.master, '<3>', [('find', self.find),('copy', self.copy),('find', self.find)], 1)

    def find(self):
        print('find')
        
    def copy(self):
        print('copy')
        
class SamMenu(Menu):
    def __init__(self, root, button, items, primary):
        Menu.__init__(self, root, tearoff=0)
        self.primary = primary
        for i in items:
            self.add_command(label=i[0], command=i[1])
        root.bind(button, self.popup)
        #TODO need to make menu options still active even if mouse moves past bounds.
        #self.bind('<Leave>', lambda e: "break")
        #self.bind('<Enter>', lambda e: "break")
        
    def popup(self, event):
        # 5 is magic. It might only look good with default font size...
        yoff = self.yposition(self.primary) + 5
        xoff = self.winfo_reqwidth() // 2
        self.post(event.x_root - xoff, event.y_root - yoff)
        # Need to grab pointer for menu to work right. Parent widget has 
        # pointer grab after button press for drag events.
        self.grab_set()

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = ''

    wand = Wand(filename)
    wand.mainloop()
