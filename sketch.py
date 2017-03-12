#!/usr/bin/env python
import wx
import wx.lib.buttons as buttons
import wx.html
import wx.adv
import os
import cPickle

class ControlPanel(wx.Panel):
    BMP_SIZE = 24
    BMP_BORDER = 3
    NUM_COLS = 4
    SPACING = 4
    colorList = ('Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple',
              'Brown', 'Aquamarine', 'Forest Green', 'Light Blue',
              'Goldenrod', 'Cyan', 'Orange', 'Navy', 'Dark Grey',
              'Light Grey')
    maxThickness = 16

    def __init__(self, parent, ID, sketch):
        wx.Panel.__init__(self, parent, ID,
                          style=wx.RAISED_BORDER)
        self.sketch = sketch
        buttonSize = (self.BMP_SIZE + 2 * self.BMP_BORDER,
                      self.BMP_SIZE + 2 * self.BMP_BORDER)
        colorGrid = self.createColorGrid(parent, buttonSize)
        thicknessGrid = self.createThicknessGrid(buttonSize)
        self.layout(colorGrid, thicknessGrid)

    def createColorGrid(self, parent, buttonSize):
        self.colorMap = {}
        self.colorButtons = {}
        colorGrid = wx.GridSizer(cols=self.NUM_COLS, hgap=2, vgap=2)
        for eachColor in self.colorList:
            bmp = parent.MakeBitmap(
                eachColor, size=(self.BMP_SIZE, self.BMP_SIZE)
            )
            b = buttons.GenBitmapToggleButton(self, -1, bmp, size=buttonSize)
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.OnSetColour, b)
            colorGrid.Add(b, 0)
            self.colorMap[b.GetId()] = eachColor
            self.colorButtons[eachColor] = b
        self.colorButtons[self.colorList[0]].SetToggle(True)
        return colorGrid

    def createThicknessGrid(self, buttonSize):
        self.thicknessIdMap = {}
        self.thicknessButtons = {}
        thicknessGrid = wx.GridSizer(cols=self.NUM_COLS, hgap=2, vgap=2)
        for x in range(1, self.maxThickness + 1):
            b = buttons.GenToggleButton(self, -1, str(x), size=buttonSize)
            b.SetBezelWidth(1)
            b.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.OnSetThickness, b)
            thicknessGrid.Add(b, 0)
            self.thicknessIdMap[b.GetId()] = x
            self.thicknessButtons[x] = b
        self.thicknessButtons[1].SetToggle(True)
        return thicknessGrid

    def layout(self, colorGrid, thicknessGrid):
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(colorGrid, 0, wx.ALL, self.SPACING)
        box.Add(thicknessGrid, 0, wx.ALL, self.SPACING)
        self.SetSizer(box)
        box.Fit(self)

    def OnSetColour(self, event):
        print("Entering OnSetColour")
        color = self.colorMap[event.GetId()]
        print("Get color: %s" % color)
        if color != self.sketch.color:
            self.colorButtons[self.sketch.color].SetToggle(False)
        self.sketch.SetColor(color)

    def OnSetThickness(self, event):
        thickness = self.thicknessIdMap[event.GetId()]
        if thickness != self.sketch.thickness:
            self.thicknessButtons[self.sketch.thickness].SetToggle(False)
        self.sketch.SetThickness(thickness)

class SketchWindow(wx.Window):

    def __init__(self, parent, ID):
        wx.Window.__init__(self, parent, ID)
        self.SetBackgroundColour("White")
        self.color = "Black"
        self.thickness = 1
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)
        self.lines = []
        self.curLine = []
        self.pos = (0, 0)
        self.InitBuffer()

        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
        self.Bind(wx.EVT_MOTION, self.OnMotion)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_IDLE, self.OnIdle)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def InitBuffer(self):
        size = self.GetClientSize()
        self.buffer = wx.Bitmap(size.width, size.height)
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.DrawLines(dc)
        self.reInitBuffer = False

    def GetLinesData(self):
        return self.lines[:]

    def SetLinesData(self, lines):
        self.lines = lines[:]
        self.InitBuffer()
        self.Refresh()

    def OnLeftDown(self, event):
        self.curLine = []
        self.pos = event.GetPosition()
        self.CaptureMouse()

    def OnLeftUp(self, event):
        if self.HasCapture():
            self.lines.append((self.color, self.thickness, self.curLine))
            self.curLine = []
            self.ReleaseMouse()

    def OnMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.DrawMotion(dc, event)
        event.Skip()

    def DrawMotion(self, dc, event):
        dc.SetPen(self.pen)
        newPos = event.GetPosition()
        coords = (self.pos, newPos)
        self.curLine.append(coords)
        dc.DrawLine(*coords)
        self.pos = newPos

    def OnSize(self, event):
        self.reInitBuffer = True

    def OnIdle(self, event):
        self.InitBuffer()
        self.Refresh(False)

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)

    def DrawLines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def SetColor(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def SetThickness(self, num):
        self.thickness = num
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)


class SketchAbout(wx.Dialog):
    text = '''
<html>
   <body bgcolor="#ACAA60">
   <center><table bgcolor="#455481" width="100%" cellspacing="0"
   cellpadding="0" border="1">
   <tr>
       <td align="center"><h1>Sketch!</h1></td>
   </tr>
   </table>
   </center>
   <p><b>Sketch</b> is a demonstration program for
   <b>wxPython In Action</b>
   Chapter 6. It is based on the SuperDoodle demo included
   with wxPython, available at
   <a href="http://www.wxpython.org/">http://www.wxpython.org/</a>
   </p>
   <p><b>SuperDoodle</b> and <b>wxPython</b> are brought to you by
   <b>Robin Dunn</b> and <b>Total Control Software</b>, Copyright
   &copy; 1997-2006.</p>
   </body>
</html>
'''


    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, 'About Sketch', size=(440, 400))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, "Okay")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()

class SketchFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Sketch Frame", size=(800,600))
        self.title = self.GetTitle()
        self.sketch = SketchWindow(self, -1)
        self.sketch.Bind(wx.EVT_MOTION, self.OnSketchMotion)
        self.createStatusBar()
        self.createMenuBar()
        self.createToolBar()
        self.createPanel()
        self.filename = ""

    def createPanel(self):
        controlPanel = ControlPanel(self, -1, self.sketch)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(controlPanel, 0, wx.EXPAND)
        box.Add(self.sketch, 1, wx.EXPAND)
        self.SetSizer(box)

    def createSimpleTool(self, label, filename, help, handler):
        if not label:
            self.toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = self.toolbar.AddTool(-1, label, bmp, shortHelp=help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def createColorTool(self, color):
        bmp = self.MakeBitmap(color)
        newId = wx.NewId()
        tool = self.toolbar.AddRadioTool(-1, color, bmp, shortHelp=color)
        self.Bind(wx.EVT_MENU, self.OnColor, tool)

    def MakeBitmap(self, color, size=(16, 15)):
        bmp = wx.Bitmap(*size)
        dc = wx.MemoryDC()
        dc.SelectObject(bmp)
        dc.SetBackground(wx.Brush(color))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def toolbarData(self):
        return (
            ("New", "new.png", "Create new sketch", self.OnNew),
            ("", "", "", ""),
            ("Open", "open.png", "Open existing sketch", self.OnOpen),
            ("Save", "save.png", "Save existing sketch", self.OnSave)
        )

    def toolbarColorData(self):
        return ("Black", "Red", "Green", "Blue")

    def createToolBar(self):
        self.toolbar = self.CreateToolBar(wx.TB_TEXT)
        for each in self.toolbarData():
            self.createSimpleTool(*each)
        self.toolbar.AddSeparator()
        for color in self.toolbarColorData():
            self.createColorTool(color)
        self.toolbar.Realize()

    def createMenuBar(self):
        menuBar = wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel = eachMenuData[0]
            menuItems = eachMenuData[1]
            menuBar.Append(self.createMenu(menuItems), menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self, menuData):
        menu = wx.Menu()
        for eachItem in menuData:
            if len(eachItem) == 2:
                label = eachItem[0]
                subMenu = self.createMenu(eachItem[1])
                menu.Append(wx.NewId(), label, subMenu)
            else:
                self.createMenuItem(menu, *eachItem)
        return menu

    def createMenuItem(self, menu, label, status, handler, kind=wx.ITEM_NORMAL):
        if not label:
            menu.AppendSeparator()
            return
        menuItem = menu.Append(-1, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menuItem)

    def menuData(self):
        return [
            ("&File", (
                ("&New"  , "New Sketch file"  , self.OnNew)  ,
                ("&Open" , "Open sketch file" , self.OnOpen) ,
                ("&Save" , "Save sketch file" , self.OnSave) ,
                ("", "", ""),
                ("&Color", (
                    ("&Black"    , "" , self.OnColor      , wx.ITEM_RADIO) ,
                    ("&Red"      , "" , self.OnColor      , wx.ITEM_RADIO) ,
                    ("&Green"    , "" , self.OnColor      , wx.ITEM_RADIO) ,
                    ("&Blue"     , "" , self.OnColor      , wx.ITEM_RADIO) ,
                    ("&Other..." , "" , self.OnOtherColor , wx.ITEM_RADIO)
                )),
                ("", "", ""),
                ("&Quit", "Quit", self.OnCloseWindow),
                ("&About", "About", self.OnAbout)
            )
        )]

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

    def OnSketchMotion(self, event):
        self.statusbar.SetStatusText("Pos: %s" % str(event.GetPosition()), 0)
        self.statusbar.SetStatusText("Cur Pts: %s" % len(self.sketch.curLine), 1)
        self.statusbar.SetStatusText("Line Count: %s" % len(self.sketch.lines), 2)
        event.Skip()

    def OnNew(self, event): pass

    def OnAbout(self, event):
        dlg = SketchAbout(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnColor(self, event):
        menubar = self.GetMenuBar()
        itemId = event.GetId()
        item = menubar.FindItemById(itemId)
        if not item:
            item = self.toolbar.FindById(itemId)
            color = item.GetShortHelp()
        else:
            color = item.GetLabel()
        print("Get color: %s" % color)
        self.sketch.SetColor(color)

    def OnOtherColor(self, event):
        dlg = wx.ColourDialog(self)
        dlg.GetColourData().SetChooseFull(True)
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour()
            self.sketch.SetColor(color)
        dlg.Destroy()

    def OnCloseWindow(self, event):
        self.Destroy()

    def SaveFile(self):
        if self.filename:
            data = self.sketch.GetLinesData()
            f = open(self.filename, 'w')
            cPickle.dump(data, f)
            f.close()

    def ReadFile(self):
        if self.filename:
             try:
                 f = open(self.filename, 'r')
                 data = cPickle.load(f)
                 f.close()
                 self.sketch.SetLinesData(data)
             except cPickle.UnpicklingError:
                 wx.MessageBox(
                     "%s is not a sketch file." % self.filename,
                     "oops!",
                     style=wx.OK|wx.ICON_EXCLAMATION
                 )

    wildcard = "Sketch files (*.sketch)|*.sketch|All files (*.*)|*.*"

    def OnOpen(self, event):
        dlg = wx.FileDialog(
            self,
            "Open sketch file...",
            os.getcwd(),
            style=wx.FD_OPEN,
            wildcard=self.wildcard
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

    def OnSave(self, event):
        if not self.filename:
            self.OnSaveAs(event)
        else:
            self.SaveFile()

    def OnSaveAs(self, event):
        dlg = wx.FileDialog(
            self,
            "Save sketch as...",
            os.getcwd(),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            wildcard=self.wildcard
        )
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
            if not os.path.splitext(filename)[1]:
                filename = filename + '.sketch'
            self.filename = filename
            self.SaveFile()
            self.SetTitle(self.title + ' -- ' + self.filename)
        dlg.Destroy()

class SketchApp(wx.App):
    def OnInit(self):
        image = wx.Image("splash.png", wx.BITMAP_TYPE_PNG)
        bmp = image.ConvertToBitmap()
        wx.adv.SplashScreen(
            bmp,
            wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
            3000,
            None,
            -1
        )
        wx.Yield()
        frame = SketchFrame(None)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


if __name__ == '__main__':
    app = SketchApp(False)
    app.MainLoop()
