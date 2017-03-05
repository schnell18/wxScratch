#!/usr/bin/env python
import wx
import os.path
import codecs

class GaugeFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Gauge Example', size=(400, 600))

        panel = wx.Panel(self, -1)
        self.count = 0
        self.gauge = wx.Gauge(panel, -1, 50, (20, 50), (250, 25))
        self.gauge.SetBezelFace(3)
        self.gauge.SetShadowWidth(3)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def OnIdle(self, event):
        self.count = self.count + 1
        if self.count >= 50:
            self.count = 0
        self.gauge.SetValue(self.count)

if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = GaugeFrame()
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
