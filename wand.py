#!/usr/bin/env python

import sys
from gi.repository import Gtk, GtkSource, GObject

class Wand():
    def __init__(self, filename):
        self.window = Gtk.Window()
        self.window.connect('delete-event', Gtk.main_quit)

        self.filename = filename
        try:
            with open(filename, 'r') as file:
                buf = file.read()
        except FileNotFoundError:
            buf = ''
            filename = 'Untitled'
        self.buffer = GtkSource.Buffer(text=buf)
        self.scroll = Gtk.ScrolledWindow()
        self.editor = GtkSource.View(buffer=self.buffer)
        self.scroll.add(self.editor)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.cmd = cmdBox(self.editor)
        self.box.pack_start(self.cmd, False, False, 0)
        self.box.pack_start(self.scroll, True, True, 0)
        self.window.add(self.box)

        self.window.show_all()

class CmdBox(Gtk.Box):
    def __init__(self, sourceView):
        self.sourceView = sourceView
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.HORIZONTAL)
        
        self.entry = Gtk.Entry()
        self.pack_start(self.entry, True, True, 0)

        # button text changes, gives feedback to user about current command
        self.xec = Gtk.Button(label='verb')
        self.pack_start(self.xec, False, False, 0)

        self.entry.connect('insert-at-cursor', self.parseCmd)
        self.entry.connect('delete-from-cursor', self.parseCmd)

    def parseCmd(self, *args):
        if self.cmd:
            #self.cmd = Cmd(text)
            pass
        else:
            #self.cmd.setCmdTxt(text)
            pass
        print(self.entry.get_text())

class Cmd():
    def __init__(self, cmdtxt):
        self.next = None
        self.desc = ''
        self._parse(cmdtxt)

    def _parse(txt):
        #sets cmd description
        pass

    def ok():
        #return true if cmd is valid
        pass

    def setCmdTxt(txt):
        self._parse(txt)

if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        filename = ''
    Wand(filename)
    Gtk.main()
