#!/usr/bin/env python

import wx

class SimpleDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'Dialog Subclass', size=(300, 200))

        grid = wx.GridSizer(cols=2, hgap=4, vgap=4)
        okBtn = wx.Button(self, wx.ID_OK, "Ok")
        cancelBtn = wx.Button(self, wx.ID_CANCEL, "Canel")
        grid.AddMany([okBtn, cancelBtn])
        self.SetSizer(grid)

if __name__ == '__main__':
    app = wx.App(False)
    dlg = SimpleDialog()
    result = dlg.ShowModal()
    if result == wx.ID_OK:
        print("Ok")
    else:
        print("Cancel")
    dlg.Destroy()
