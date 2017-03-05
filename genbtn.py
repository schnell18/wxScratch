#!/usr/bin/env python

import wx
import wx.lib.buttons as buttons

class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
        panel = wx.Panel(self)

        # Build a bitmap button and a normal one
        # bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_OTHER, (16, 16))
        bmp = wx.ArtProvider.GetBitmap('wxART_INFORMATION', wx.ART_OTHER, (16, 16))
        btn1 = buttons.ThemedGenBitmapButton(panel, -1, bmp, pos=(50, 50))
        btn2 = buttons.GenButton(panel, -1, "Hello World!", pos=(50, 100))


app = wx.App()
frame = MyFrame(None, 'wx.lib.buttons Test')
frame.Show()
app.MainLoop()
