#!/usr/bin/env python
import wx

class RefactorExample(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Refactor Example', size=(340, 200))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")

        self.creteButtonBar(panel, yPos=10)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        openMenuItem = menu1.Append(-1, "&Open", "Copy in status bar")
        self.Bind(wx.EVT_MENU, self.OnOpen, openMenuItem)
        quitMenuItem = menu1.Append(-1, "&Quit", "Quit")
        self.Bind(wx.EVT_MENU, self.OnCloseWindow, quitMenuItem)
        menuBar.Append(menu1, "&File")
        menu2 = wx.Menu()
        copyItem = menu2.Append(-1, "&Copy", "Copy")
        self.Bind(wx.EVT_MENU, self.OnCopy, copyItem)
        cutItem = menu2.Append(-1, "C&ut", "Cut")
        self.Bind(wx.EVT_MENU, self.OnCut, cutItem)
        pasteItem = menu2.Append(-1, "Paste", "Paste")
        self.Bind(wx.EVT_MENU, self.OnPaste, pasteItem)
        menuBar.Append(menu2, "&Edit")
        self.SetMenuBar(menuBar)
        static = wx.StaticText(panel, wx.NewId(), "First Name", pos=(10, 50))
        static.SetBackgroundColour("White")
        text = wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=(80, 50))
        static2 = wx.StaticText(panel, wx.NewId(), "Last Name", pos=(10, 80))
        static2.SetBackgroundColour("White")
        text2 = wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=(80, 80))

        menu2.AppendSeparator()
        optItem = menu2.Append(-1, "&Options...", "Display Options")
        self.Bind(wx.EVT_MENU, self.OnOptions, optItem)

    def buttonData(self):
        return (
            ("First", self.OnFirst),
            ("<< PREV", self.OnPrev),
            ("NEXT >>", self.OnNext),
            ("Last", self.OnLast)
        )

    def creteButtonBar(self, panel, yPos=0):
        btn_data = self.buttonData()
        xPos = 0
        for lbl, hdl in btn_data:
            pos = (xPos, yPos)
            btn = self.buildButton(panel, lbl, hdl, pos)
            xPos += btn.GetSize().width

    def buildButton(self, parent, label, handler, pos=(0, 0)):
        btn = wx.Button(parent, label=label, pos=pos)
        self.Bind(wx.EVT_BUTTON, handler, btn)
        return btn

    # Just grouping the empty event handlers together
    def OnPrev(self, event): pass
    def OnNext(self, event): pass
    def OnLast(self, event): pass
    def OnFirst(self, event): pass
    def OnOpen(self, event): pass
    def OnCopy(self, event): pass
    def OnCut(self, event): pass
    def OnPaste(self, event): pass
    def OnOptions(self, event): pass
    def OnCloseWindow(self, event):
        self.Destroy()

if __name__ == '__main__':
    app = wx.App()
    frame = RefactorExample(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
