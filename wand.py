#!/usr/bin/env python

import sys
import os
from tkinter import *
from tkinter import ttk

class Wand(ttk.Frame):
    """Main application class. Manages windows/frames"""
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master=master)
        master.withdraw()
        self.master = master
        self.wincount = 0
        self.bind_class('Toplevel', '<Destroy>', self.countwins)
        # TODO load config file here
        filename = os.path.realpath(filename) if filename else ''
        self.open(filename)
    def open(self, filename):
        win = Toplevel(self.master)
        Editor(win, filename)
        self.wincount += 1
    def countwins(self, event):
        if self.wincount > 1:
            self.wincount -= 1
        else:
            self.master.destroy()

class Editor(ttk.Frame):
    """An editor window."""
    def __init__(self, master, filename):
        ttk.Frame.__init__(self, master=master)
        self.pack(fill=BOTH, expand=1)
        self.tk_focusFollowsMouse()
        try:
            with open(filename, 'r') as file:
                buf = file.read()
            self.filename = filename
        except FileNotFoundError:
            #TODO indicate to user this is a new file?
            buf = ''
            self.filename = ''
        self.master.title(self.filename)
        self.build_widgets(buf)
    def build_widgets(self, buf):
        # controls frame has URL bar and basic buttons,
        # such as load/refresh, undo, redo, save,
        # and close.
        self.controls = ttk.Frame(self)
        self.controls.pack(side=TOP, fill=BOTH, expand=1)
        self.urlbar = ttk.Entry(self.controls)
        self.urlbar.insert(0, self.filename)
        self.urlbar.pack(side=LEFT, fill=BOTH, expand=1)
        r = ttk.Button(self.controls, text="Load", command=self.refresh)
        r.pack(side=RIGHT)
        
        # below the controls frame is the main editor window
        self.editor = Text(self)
        self.editor['insertunfocussed'] = 'solid' #don't ever hide cursor
        self.editor.insert(0.0, buf)
        self.editor.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollY = ttk.Scrollbar(self, orient=VERTICAL,
                                     command=self.editor.yview)
        self.scrollY.pack(side=RIGHT, fill=Y)
        self.editor['yscrollcommand'] = self.scrollY.set
        
        self.menu = SamMenu(self.master, '<3>', [('find', self.find),
                                                 ('copy', self.copy),
                                                 ('find', self.find)], 1)
    def refresh(self):
    	print('refresh')
    def find(self):
        print('find')
    def copy(self):
        print('copy')
        
class SamMenu(Menu):
    """SamMenu behaves like the mouse menus from the text editor sam.
    The menu stays open only while the mouse button is held down, and
    selects whatever is under the mouse when the mouse button is
    released. The "primary" menu entry is directly under the mouse when
    the menu appears."""
    def __init__(self, root, button, items, primary):
        Menu.__init__(self, root, tearoff=0)
        self.primary = primary
        for i in items:
            self.add_command(label=i[0], command=i[1])
        root.bind(button, self.popup)
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

    root = Tk()
    wand = Wand(root, filename)
    root.mainloop()
