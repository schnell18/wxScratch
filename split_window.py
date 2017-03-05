#!/usr/bin/env python

import wx

class SplitFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)
        self.MakeMenuBar()

        self.initpos = 100
        self.sp = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.p2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.p2.Hide()
        self.p1.SetBackgroundColour("pink")
        self.p2.SetBackgroundColour("sky blue")
        self.sp.Initialize(self.p1)
        self.sp.SetMinimumPaneSize(10)

    def MakeMenuBar(self):
        menu = wx.Menu()
        item = menu.Append(-1, "Split horizontally")
        self.Bind(wx.EVT_MENU, self.OnSplitH, item)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanSplit, item)
        item = menu.Append(-1, "Split vertically")
        self.Bind(wx.EVT_MENU, self.OnSplitV, item)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanSplit, item)
        item = menu.Append(-1, "Unsplit")
        self.Bind(wx.EVT_MENU, self.OnUnsplit, item)
        self.Bind(wx.EVT_UPDATE_UI, self.OnCheckCanUnsplit, item)
        menu.AppendSeparator()
        item = menu.Append(wx.ID_EXIT, "E&xit")
        self.Bind(wx.EVT_MENU, self.OnExit, item)
        mbar = wx.MenuBar()
        mbar.Append(menu, "Splitter")
        self.SetMenuBar(mbar)

    def OnSplitH(self, evt):
        self.sp.SplitHorizontally(self.p1, self.p2, self.initpos)

    def OnSplitV(self, evt):
        self.sp.SplitVertically(self.p1, self.p2, self.initpos)

    def OnCheckCanSplit(self, evt):
        evt.Enable(not self.sp.IsSplit())

    def OnCheckCanUnsplit(self, evt):
        evt.Enable(self.sp.IsSplit())

    def OnUnsplit(self, evt):
        self.sp.Unsplit()

    def OnExit(self, evt):
        self.Close()


if __name__ == '__main__':
    app = wx.App(False)
    frame = SplitFrame(None, "Split Window Sample")
    frame.Show(True)
    app.MainLoop()
