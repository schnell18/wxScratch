#!/usr/bin/env python
import wx

class TextFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            None,
            -1,
           'Basic Text Example',
           size=(500, 400)
        )

        basic_lbl = wx.StaticText(self, -1, "User Name")
        basic_txt = wx.TextCtrl(self, -1, "John Doe")

        pwd_lbl = wx.StaticText(self, -1, "Password")
        pwd_txt = wx.TextCtrl(self, -1, "password", style=wx.TE_PASSWORD)
        sizer = wx.FlexGridSizer(cols=2, hgap=5, vgap=5)
        sizer.Add(basic_lbl)
        sizer.Add(basic_txt, 1, wx.ALL | wx.EXPAND)
        sizer.Add(pwd_lbl)
        sizer.Add(pwd_txt, 0, wx.EXPAND)
        self.SetSizerAndFit(sizer)

if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = TextFrame()
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
