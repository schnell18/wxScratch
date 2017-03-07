#!/usr/bin/env python

import wx

if __name__ == '__main__':
    app = wx.App(False)
    progressMax = 10
    dlg = wx.ProgressDialog(
        "Upload progress",
        "Time remaining",
        progressMax,
        style=wx.PD_CAN_ABORT
             | wx.PD_ELAPSED_TIME
             | wx.PD_REMAINING_TIME
             | wx.PD_AUTO_HIDE
    )
    keepGoing = True
    count = 0
    while keepGoing and count < progressMax:
        count = count + 1
        wx.Sleep(1)
        keepGoing = dlg.Update(count)
    dlg.Destroy()
