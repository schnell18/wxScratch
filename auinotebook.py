#!/usr/bin/env python

import wx
import wx.aui

class MyFrame(wx.Frame):
    def __init(self, parent):
        wx.Frame.__init__(self, parent)
        self.notebook = wx.aui.AuiNotebook(
            self,
            style=wx.aui.AUI_NB_DEFAULT_STYLE
        )
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 4)
        self.SetSizer(mainSizer)
        self.Layout()
        self.Centre()


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
