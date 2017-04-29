#!/usr/bin/env python

import os
import sys
import tkinter as tk
from tkinter import ttk


class _Tconst:
    """some text constants"""
    Load = "→"
    Refresh = "↺"


class Wand(ttk.Frame):
    """Main application class. Manages windows/frames"""
    def __init__(self, master, filename):
        super().__init__(master)
        master.withdraw()
        self.wincount = 0
        self.bind_class('Toplevel', '<Destroy>', self.countwins)
        # TODO load config file here
        filename = os.path.realpath(filename) if filename else ''
        self.open(filename)
    def open(self, filename):
        win = tk.Toplevel(self.master)
        EditFrame(win, filename)
        self.wincount += 1
    def countwins(self, event):
        if self.wincount > 1:
            self.wincount -= 1
        else:
            self.master.destroy()


class EditFrame(ttk.Frame):
    def __init__(self, master, filename):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=1)
        self.tk_focusFollowsMouse()
        self.filename = filename
        self.build_widgets()
        self.loadURL()
    def build_widgets(self):
        # controls frame has URL bar and basic buttons,
        # such as load/refresh, undo, redo, save,
        # and close.
        self.controls = ttk.Frame(self)
        self.controls.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.urlbar = ttk.Entry(self.controls)
        self.urlbar.insert(0, self.filename)
        self.urlbar.bind('<Return>', self.loadURL)
        self.urlbar.bind('<<Paste>>', self.showLoadOrRefresh)
        self.urlbar.bind('<KeyRelease>', self.showLoadOrRefresh)
        self.urlbar.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.bLoad = ttk.Button(self.controls, text=_Tconst.Load, command=self.loadURL)
        self.bLoad.pack(side=tk.RIGHT)
        
        # below the controls frame is the main editor window
        self.editor = Editor(self)
        self.editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.scrollY = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                     command=self.editor.yview)
        self.scrollY.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor['yscrollcommand'] = self.scrollY.set

    def loadURL(self, e=None):
        '''Load the file listed in the urlbar'''
        # TODO prompt user if buffer is dirty with editor.edit_modified()
        f = self.urlbar.get()
        different = True if f == self.filename else False
        try:
            with open(f, 'r') as file:
                buf = file.read()
                self.editor.replace(0.0, END, buf)
                if different:
                    # loaded a new file. Can't undo to "unload" file.
                    self.editor.edit_reset()
                self.bLoad['text'] = _Tconst.Refresh
                self.filename = f
        except FileNotFoundError:
            pass
            #TODO indicate to user this is a new file?
        self.master.title(self.filename)
        
    def showLoadOrRefresh(self, e=None):
        if self.urlbar.get() == self.filename:
            self.bLoad['text'] = _Tconst.Refresh
        else:
            self.bLoad['text'] = _Tconst.Load

        
class SamMenu(tk.Menu):
    """SamMenu behaves like the mouse menus from the text editor sam.
    The menu stays open only while the mouse button is held down, and
    selects whatever is under the mouse when the mouse button is
    released. The "select" menu entry is directly under the mouse when
    the menu appears."""
    def __init__(self, master):
        super().__init__(master=master, tearoff=0)

    def popup(self, event, select=0):
        # 5 is magic. It might only look good with default font size...
        yoff = self.yposition(select) + 5
        xoff = self.winfo_reqwidth() // 2
        self.post(event.x_root - xoff, event.y_root - yoff)
        # Need to grab pointer for menu to work right. Parent widget has 
        # pointer grab after button press for drag events.
        self.grab_set()


class CopyPasteMenu(SamMenu):
    def __init__(self, tk_text_window):
        super().__init__(tk_text_window)
        self.add_command(label='Cut', command=self.cut)
        self.add_command(label='Copy', command=self.copy)
        self.add_command(label='Paste', command=self.paste)

    def popup(self, event):
        if self.master.tag_ranges(tk.SEL):
            self.entryconfig(0, state=tk.ACTIVE)
            self.entryconfig(1, state=tk.ACTIVE)
            select = 1
        else:
            # if no selection, can't cut or copy
            self.entryconfig(0, state=tk.DISABLED)
            self.entryconfig(1, state=tk.DISABLED)
            select = 2
        super().popup(event, select)

    def cut(self):
        self.master.event_generate('<<Cut>>')

    def copy(self):
        self.master.event_generate('<<Copy>>')

    def paste(self):
        self.master.event_generate('<<Paste>>')


class ButtonEvent():
    def __init__(self, seq, act):
        self.seq = seq
        self.act = act

class Selector:
    """Control a text selection. Text selection is word-based, not
    character based, because ordinarilly, users want to select entire
    words, not parts of words.
    """
    def __init__(self, textWindow, tagname):
        """The selector will create selections in the provided text
        window. The selection will be tagged with tagname; use
        textWindow.tag_configure to adjust how the selection will be
        displayed.
        """
        self.master = textWindow
        self.name = tagname
        self.start = ''
        self.end = ''

    def _tag(self, i1, i2, func=''):
        """Support backwards selections"""
        if self.master.compare(i1, '<=', i2):
            getattr(self.master, func)(self.name, i1+' wordstart', i2+' wordend')
        else:
            getattr(self.master, func)(self.name, i2+' wordstart', i1+' wordend')

    def tag_add(self, i1, i2): self._tag(i1, i2, func='tag_add')

    def tag_remove(self, i1, i2): self._tag(i1, i2, func='tag_remove')
        
    def begin_select(self, event):
        self.oldstart = self.start
        self.start = '@{},{}'.format(event.x, event.y)
        self.master.bind_all('<Motion>', self.update_select)

    def update_select(self, event):
        if self.oldstart:
            self.tag_remove(self.oldstart, self.end)
            self.oldstart = ''
        else:
            self.unselect()
        self.end = '@{},{}'.format(event.x, event.y)
        self.tag_add(self.end, self.start)

    def end_select(self, event):
        self.master.unbind_all('<Motion>')

    def unselect(self):
        if self.end:
            self.tag_remove(self.start, self.end)


class MouseEvents:
    """Add-in for mouse chording events. Assumes self inherits from tk.Text"""
    def mouse_events_start(self):
        self.bind('<ButtonPress>', self._bpress_event)
        # bind all so menu buttons don't steal the release event
        self.bind_all('<ButtonRelease>', self._brel_event)
        self.cpMenu = CopyPasteMenu(self)
        self.chord = []
        s = Selectable(self, 'sel2')
        self.tag_configure('sel2', background='red', foreground='white')
        self.bp_events = [
            ButtonEvent([1,3], self.cpMenu.popup),
            ButtonEvent([8], s.begin_select),
            #ButtonEvent([8,3], self.exMenu.popup),
        ]
        self.br_events = [
            ButtonEvent([8], s.end_select),
        ]

    def _bpress_event(self, event):
        self.chord.append(event.num)
        for e in self.bp_events:
            if e.seq == self.chord:
                e.act(event)
                return

    def _brel_event(self, event):
        for e in self.br_events:
            if e.seq == [event.num]:
                e.act(event)
        if event.num in self.chord:
            self.chord.remove(event.num)


class Editor(tk.Text, MouseEvents):
    def __init__(self, master):
        super().__init__(master)
        self['insertunfocussed'] = 'solid' #don't ever hide cursor
        self.mouse_events_start()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = ''

    root = tk.Tk()
    wand = Wand(root, filename)
    root.mainloop()
