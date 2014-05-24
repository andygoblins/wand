#!/usr/bin/env python

import sys
from gi.repository import Gtk, GtkSource, GObject

class Wand():
    def __init__(self, filenames):
        self.window = Gtk.Window()
        self.window.connect('delete-event', Gtk.main_quit)

        self.notebook = Gtk.Notebook()
        self.window.add(self.notebook)

        fail = []
        for filename in filenames:
            try:
                buf = FileBuffer(filename)
                tab = Tab(buf)
                self.notebook.append_page(tab, tab.label)
            except OSError as e:
                fail.append((filename, e))

        if not filenames or len(fail) == len(filenames):
            buf = FileBuffer('')
            tab = Tab(buf)
            self.notebook.append_page(tab, tab.label)

        #TODO user friendliness: watch file for changes
        #TODO user friendliness: make a infobar for readonly files

        #TODO popup with I/O errors here

        self.window.show_all()

class Tab(Gtk.Box):
    def __init__(self, filebuffer):
        Gtk.Box.__init__(self, orientation=Gtk.Orientation.VERTICAL)

        self.cmd = Gtk.Entry()
        self.pack_start(self.cmd, False, False, 0)

        self.scroll = Gtk.ScrolledWindow()
        self.editor = GtkSource.View(buffer=filebuffer)
        self.scroll.add(self.editor)
        self.pack_start(self.scroll, True, True, 0)

        #TODO label should have an 'x' for closing
        self.label = Gtk.Label(filebuffer.filename)

class FileBuffer(GtkSource.Buffer):
    def __init__(self, filename):
        if filename:
            self.filename = filename
            try:
                with open(filename, 'r') as file:
                    buf = file.read()
            except FileNotFoundError:
                buf = ''
        else:
            self.filename = 'Untitled'
            buf = ''

        #TODO load buffer settings based on preferences
        GtkSource.Buffer.__init__(self, text=buf)

    def save(self):
        #TODO possible error: permission denied
        pass

    def rename(str):
        pass

if __name__ == '__main__':
    Wand(sys.argv[1:])
    Gtk.main()
