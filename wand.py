#!/usr/bin/env python

import sys
import itertools
from tkinter import *
from tkinter import ttk

class Wand():
    def __init__(self, filename):
        self.editors = {}
        # TODO load config file here
        self.open(filename)
    def open(self, filename):
        if filename in self.editors:
            ed = self.editors[filename][0]
            n = Editor(filename, peer=ed)
            self.editors[filename].append(n)
        else:
            n = Editor(filename)
            self.editors[filename] = [n]

class Editor(ttk.Frame):
    def __init__(self, filename, master=None, peer=None):
        ttk.Frame.__init__(self, master=master)
        if peer:
            self.editor = peer.editor.peer_create(master)
        else:
            try:
                with open(filename, 'r') as file:
                    buf = file.read()
                    self.master.title(filename)
            except FileNotFoundError:
                buf = ''
                self.master.title('Untitled')
            self.editor = TextHack(self)
            self.editor.insert(0.0, buf)

        self.editor.pack(side=LEFT, fill=BOTH, expand=1)  
        self.pack(fill=BOTH, expand=1)
        self.scrollY = ttk.Scrollbar(self, orient=VERTICAL,
                                     command=self.editor.yview)
        self.scrollY.pack(side=RIGHT, fill=Y)
        self.editor['yscrollcommand'] = self.scrollY.set
        
        self.menu = SamMenu(self.master, '<3>', [('find', self.find),
                                                 ('copy', self.copy),
                                                 ('find', self.find)], 1)
        self.bind('<Destroy>', self.close)
    def close(self, event):
        #TODO unregister with Wand (Wand keeps track of editor peers).
        pass
    def find(self):
        print('find')
    def copy(self):
        print('copy')

class TextHack(Text):
    """Same as regular Text, but implements fix from
    https://bugs.python.org/issue17945"""

    peer_count = itertools.count(1)
    
    def __init__(self, master=None, **kw):
        Text.__init__(self, master, **kw)

    def peer_create(self, master=None, cnf={}, **kw): # new in Tk 8.5
            """Creates a peer text widget and any optional standard
            configuration options. By default the peer will have the same
            start and and end line as the parent widget, but these can be
            overriden with the standard configuration options."""
            if master is None:
                master = self.master
            if 'name' not in cnf:
                peername = '%s%s%d' % (self._name, '_peer',
                                       next(self.peer_count))
            else:
                peername = cnf['name']
                cnf.pop('name')
            if master == '.':
                peerpath = '.' + peername
            else:
                peerpath = master._w + '.' + peername
            self.tk.call(self._w, 'peer', 'create', peerpath,
                     *self._options(cnf, kw))
            peer = _textpeer(master, peername)
            return peer

class _textpeer(Text):
    """Internal class used to represent a text peer. Part of fix for
    https://bugs.python.org/issue17945"""
    def __init__(self, master, name):
        BaseWidget._setup(self, master, {'name': name})
        
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

    wand = Wand(filename)
    wand.open(filename)
    wand.mainloop()
