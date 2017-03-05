#!/usr/bin/env python
import wx
import os.path
import codecs

class TwoButtonEvent(wx.PyCommandEvent):
    def __init__(self, evt_type, id):
        wx.PyCommandEvent.__init__(self, evt_type, id)
        self.click_count = 0

    def GetClickCount(self):
        return self.click_count

    def SetClickCount(self, count):
        self.click_count = count

myEVT_TWO_BUTTON = wx.NewEventType()
EVT_TWO_BUTTON = wx.PyEventBinder(myEVT_TWO_BUTTON, 1)

class TwoButtonPanel(wx.Panel):
    def __init__(self, parent, id=-1, left_text="Left", right_text="Right"):
        wx.Panel.__init__(self, parent, id)

        box_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_btn = wx.Button(self, label=left_text)
        self.right_btn = wx.Button(self, label=right_text)
        box_sizer.Add(self.left_btn, 0, wx.ALL)
        box_sizer.Add(self.right_btn, 0, wx.ALL)

        self.left_click = False
        self.right_click = False
        self.click_count = 0
        self.left_btn.Bind(wx.EVT_LEFT_DOWN, self.OnLeftClick)
        self.right_btn.Bind(wx.EVT_LEFT_DOWN, self.OnRightClick)
        self.SetSizer(box_sizer)

    def OnLeftClick(self, event):
        self.left_click = True
        self.OnClick()
        event.Skip()

    def OnRightClick(self, event):
        self.right_click = True
        self.OnClick()
        event.Skip()

    def OnClick(self):
        self.click_count += 1
        if self.right_click and self.left_click:
            self.right_click = False
            self.left_click = False
            evt = TwoButtonEvent(myEVT_TWO_BUTTON, self.GetId())
            evt.SetClickCount(self.click_count)
            self.GetEventHandler().ProcessEvent(evt)


class MainWindow(wx.Frame):

    def __init__(self, parent, title, size=(400, 600)):
        wx.Frame.__init__(self, parent, title=title, size=size)
        self.panel = TwoButtonPanel(self)
        self.Bind(EVT_TWO_BUTTON, self.OnTwoClick, self.panel)

    def OnTwoClick(self, event):
        self.SetTitle("Click Count: %s" % event.GetClickCount())

if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MainWindow(None, 'Two Button Event', size=(600, 400))
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
