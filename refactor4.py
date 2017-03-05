#!/usr/bin/env python
import wx

class RefactorExample(wx.Frame):
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Refactor Example', size=(340, 200))
        panel = wx.Panel(self, -1)
        panel.SetBackgroundColour("White")

        self.creteMenuBar()
        self.creteButtonBar(panel, yPos=10)
        self.creteForm(panel)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def creteForm(self, panel):
        for lbl, pos in self.formData():
            self.buildFormField(panel, lbl, pos)

    def buildFormField(self, panel, lbl, pos):
        static = wx.StaticText(panel, wx.NewId(), lbl, pos)
        static.SetBackgroundColour("White")
        inputPos = (pos[0] + 75, pos[1])
        wx.TextCtrl(panel, wx.NewId(), "", size=(100, -1), pos=inputPos)

    def formData(self):
        return (
            ('First Name', (10, 50)),
            ('Last Name', (10, 80))
        )

    def creteMenuBar(self):
        menuBar = wx.MenuBar()
        for menuData in self.menuData():
            lbl = menuData[0]
            items = menuData[1:]
            menuBar.Append(self.buildMenu(items), lbl)
        self.SetMenuBar(menuBar)

    def buildMenu(self, items):
        menu = wx.Menu()
        for lbl, txt, hdl in items:
            if lbl:
                mi = menu.Append(-1, lbl, txt)
                self.Bind(wx.EVT_MENU, hdl, mi)
            else:
                mi = menu.AppendSeparator()
        return menu

    def menuData(self):
        return (
            ('&File',
                ('&Open', 'Open in status bar', self.OnOpen),
                ('&Quit', 'Quit', self.OnQuit)
            ),
            ('&Edit',
                ('&Copy', 'Copy', self.OnCopy),
                ('C&ut', 'Cut', self.OnCut),
                ('&Paste', 'Paste', self.OnPaste),
                ('', '', ''),
                ('&Options...', 'DisplayOptions', self.OnOptions)
            )
        )

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
    def OnQuit(self, event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.App()
    frame = RefactorExample(parent=None, id=-1)
    frame.Show()
    app.MainLoop()
