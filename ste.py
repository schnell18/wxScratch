#!/usr/bin/env python
import wx
import os.path
import codecs

class MainWindow(wx.Frame):

    def __init__(self, parent, title, size=(400, 600)):
        wx.Frame.__init__(self, parent, title=title, size=size)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()

        # Setting up the menu
        filemenu = wx.Menu()
        # wx.ID_ABOUT and wx.ID_EXIT are wxWidgets standard IDs
        mi_about = filemenu.Append(wx.ID_ABOUT, "&About", "Information about")
        filemenu.AppendSeparator()
        mi_exit = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit the program")
        mi_open = filemenu.Append(wx.ID_ANY, "&Open", "Open file")
        mi_save = filemenu.Append(wx.ID_ANY, "&Save", "Save file")
        self.Bind(wx.EVT_MENU, self.OnAbout, mi_about)
        self.Bind(wx.EVT_MENU, self.OnExit, mi_exit)
        self.Bind(wx.EVT_MENU, self.OnOpen, mi_open)
        self.Bind(wx.EVT_MENU, self.OnSave, mi_save)

        # Setting up the menu
        editmenu = wx.Menu()
        editmenu.Append(wx.ID_ANY, "&Undo", "Undo last edit")
        editmenu.AppendSeparator()
        editmenu.Append(wx.ID_ANY, "&Redo", "Redo last edit")

        # create the menubar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        menubar.Append(editmenu, "&Edit")
        self.SetMenuBar(menubar)

    def OnAbout(self, event):
        dlg = wx.MessageDialog(
            self,
            "A smale text editor",
            "About Simple Editor",
            wx.OK
        )
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self, event):
        self.dirname = ''
        dlg = wx.FileDialog(
            self,
            "Choose a file",
            self.dirname,
            "",
            "*.*"
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            fp = os.path.join(self.dirname, self.filename)
            with open(fp, 'r') as f:
                self.control.SetValue(f.read())
            dlg.Destroy()

    def OnSave(self, event):
        fp = os.path.join(self.dirname, self.filename)
        with codecs.open(fp, 'w', 'utf-8') as f:
            f.write(self.control.GetValue())


if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MainWindow(None, 'Simple Editor', size=(600, 400))
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
