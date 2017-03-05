#!/usr/bin/env python
import wx
import wx.dataview

class MainWindow(wx.Frame):

    def __init__(self, parent, title, size=(400, 600)):
        wx.Frame.__init__(self, parent, title=title, size=size)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        b_sizer = wx.BoxSizer(wx.HORIZONTAL)

        listctrl = wx.dataview.DataViewListCtrl(self, wx.ID_ANY)

        listctrl.AppendToggleColumn("Toggle")
        listctrl.AppendTextColumn("Text", )
        listctrl.AppendProgressColumn("Completion", )

        data = [True, "row 1", 10]
        listctrl.AppendItem(data)

        data = [False, "row 3", 35]
        listctrl.AppendItem(data)
        b_sizer.Add(listctrl, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizerAndFit(b_sizer)


if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MainWindow(None, 'Simple Editor', size=(600, 400))
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
