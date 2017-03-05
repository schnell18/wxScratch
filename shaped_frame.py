#!/usr/bin/env python

import wx
import images

class ShapedFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self,
            parent=None,
            id=-1,
            title='Shaped Frame',
            style=wx.FRAME_SHAPED | wx.SIMPLE_BORDER | wx.FRAME_NO_TASKBAR
        )
        self.hasShape = False
        self.bmp = images.getVippiBitmap()
        self.SetClientSize((self.bmp.GetWidth(), self.bmp.GetHeight()))
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0, 0, True)
        self.SetWindowShape()
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleClick)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        self.Bind(wx.EVT_RIGHT_UP, self.OnExit)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_WINDOW_CREATE, self.SetWindowShape)

    def SetWindowShape(self, event=None):
        r = wx.Region(self.bmp)
        self.hasShape = self.SetShape(r)

    def OnDoubleClick(self, event):
        if self.hasShape:
            self.SetShape(wx.Region())
            self.hasShape = False
        else:
            self.SetWindowShape()

    def OnPaint(self, event=None):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0 , True)

    def OnExit(self, event=None):
        self.Close()

    def OnLeftDown(self, event=None):
        self.CaptureMouse()
        pos = self.ClientToScreen(event.GetPosition())
        origin = self.GetPosition()
        self.delta = wx.Point(pos.x - origin.x, pos.y - origin.y)

    def OnMouseMove(self, event=None):
        if event.Dragging() and event.LeftIsDown():
            pos = self.ClientToScreen(event.GetPosition())
            newPos = (pos.x - self.delta.x, pos.y - self.delta.y)
            self.Move(newPos)

    def OnLeftUp(self, event=None):
        if self.HasCapture():
            self.ReleaseMouse()

if __name__ == '__main__':
    app = wx.App(False)
    frame = ShapedFrame()
    frame.Show(True)
    app.MainLoop()
