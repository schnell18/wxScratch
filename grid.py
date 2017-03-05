#!/usr/bin/env python
import wx
import wx.grid

class MainWindow(wx.Frame):

    def __init__(self, parent, title, size=(400, 600)):
        wx.Frame.__init__(self, parent, title=title, size=size)
        grid = wx.grid.Grid(self)
        grid.CreateGrid(50, 50)
        for row in range(20):
            for col in range(6):
                grid.SetCellValue(row, col, "Cell (%d,%d)" % (row, col))

if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MainWindow(None, 'Simple Editor', size=(600, 400))
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
