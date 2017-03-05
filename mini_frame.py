#!/usr/bin/env python

import wx

class MiniFrame(wx.MiniFrame):
    def __init__(self):
        wx.MiniFrame.__init__(
            self,
            parent=None,
            id=-1,
            title='Mini Frame',
            style=wx.STAY_ON_TOP|wx.CAPTION,
            size=(300, 100)
        )
        panel = wx.Panel(self, -1, size=(300, 100))
        button = wx.Button(panel, -1, "Close Me", pos=(15, 15))
        self.Bind(wx.EVT_BUTTON, self.OnCloseMe, button)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MiniFrame()
    frame.Show(True)
    app.MainLoop()
