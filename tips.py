#!/usr/bin/env python
import wx
import wx.adv

if __name__ == "__main__":
    app = wx.App()
    provider = wx.adv.CreateFileTipProvider("tips.txt", 0)
    wx.adv.ShowTip(None, provider, True)
