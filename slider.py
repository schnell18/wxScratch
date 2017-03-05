#!/usr/bin/env python
import wx
import os.path

class MainWindow(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Slider Example', size=(340, 320))
        panel = wx.Panel(self, -1)
        self.count = 0
        slider = wx.Slider(
            panel,
            value=25,
            style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS
        )
        slider.SetTickFreq(5)
        # slider = wx.Slider(panel, 100, 25, 1, 100, pos=(125, 50),
        #         size=(-1, 250),
        #         style=wx.SL_VERTICAL | wx.SL_AUTOTICKS | wx.SL_LABELS )
        # slider.SetTickFreq(20)


if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MainWindow()
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
