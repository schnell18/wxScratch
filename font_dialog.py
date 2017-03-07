#!/usr/bin/env python

import wx

if __name__ == '__main__':
    app = wx.App(False)

    dlg = wx.FontDialog(None, wx.FontData())
    if dlg.ShowModal() == wx.ID_OK:
        data = dlg.GetFontData()
        font = data.GetChosenFont()
        color = data.GetColour()
        print 'You selected: %s, %d points\n' % (font.GetFaceName(), font.GetPointSize())
    dlg.Destroy()
