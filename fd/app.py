# -*- coding: utf-8 -*-

import ConfigParser
import wx
import wx.aui
from fitness.uilib import ExercisePanel
from fitness.uilib import LessonPanel
from fitness.uilib import CurriculumPanel
from fitness.parser import Parser
from fitness.model import Curriculum
from fitness.model import Lesson
from fitness.model import Exercise
from os.path import expanduser


class FtFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id = wx.ID_ANY,
            title = wx.EmptyString,
            pos = wx.DefaultPosition,
            size = wx.Size(1000, 700),
            style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL
        )

        # create status bar
        self.createStatusBar()
        # create menu bar
        self.createMenuBar()
        # create tool bar
        self.createToolBar()

        # layout main interface
        # splitter window
        self.sp = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        self.left = self.createTreePanel(self.sp)
        self.right = self.createNotbook(self.sp)
        self.sp.SplitVertically(self.left, self.right, 300)

        self.Layout()
        self.Centre()

    def __del__(self):
        pass

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-1, -2, -3])

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
                menu.AppendMenu(wx.NewId(), label, subMenu)
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

    def createTreePanel(self, parent):
        scrollWin = wx.ScrolledWindow(
            parent,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        scrollWin.SetScrollRate(5, 5)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)
        self.tree = wx.TreeCtrl(
            scrollWin,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TR_DEFAULT_STYLE
        )
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)

        il = wx.ImageList(16, 16, True)
        for img in ['curriculum', 'lesson', 'exercise']:
            bmp = wx.Bitmap(img + '.png', wx.BITMAP_TYPE_PNG)
            il.Add(bmp)
        self.tree.AssignImageList(il)
        self.rootId = self.tree.AddRoot("Curriculum Bundle")

        bSizer3.Add(self.tree, 3, wx.EXPAND|wx.RIGHT, 5)
        scrollWin.SetSizer(bSizer3)
        scrollWin.Layout()
        bSizer3.Fit(scrollWin)
        return scrollWin

    def createNotbook(self, parent):
        notebook = wx.aui.AuiNotebook(
            parent,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.aui.AUI_NB_DEFAULT_STYLE
        )

        il = wx.ImageList(16, 16, True)
        for img in ['curriculum', 'lesson', 'exercise']:
            bmp = wx.Bitmap(img + '.png', wx.BITMAP_TYPE_PNG)
            il.Add(bmp)
        notebook.AssignImageList(il)

        return notebook

    def createSimpleTool(self, label, filename, help, handler):
        if not label:
            self.toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = self.toolbar.AddSimpleTool(-1, bmp, shortHelpString=help)
        self.Bind(wx.EVT_MENU, handler, tool)

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
        self.toolbar.Realize()

    def OnSelChanged(self, event):
        notebook = self.right
        data = self.tree.GetItemPyData(event.GetItem())
        #TODO: find or create page
        if isinstance(data, Curriculum):
            curr = CurriculumPanel(notebook, data)
            notebook.AddPage(curr, data.title, True, 0)
        elif isinstance(data, Lesson):
            lesson = LessonPanel(notebook, data)
            notebook.AddPage(lesson, data.title, True, 1)
        else:
            exercise = ExercisePanel(notebook, data)
            notebook.AddPage(exercise, data.action, True, 2)
        # self.right.SetSelection(selection)

    def OnNew(self, event):
        pass

    def OnOpen(self, event):
        dlg = wx.DirDialog(
            self,
            message=u"请选择课程包目录"
        )
        if dlg.ShowModal() == wx.ID_OK:
            print 'You selected: %s' % dlg.GetPath()

            config = ConfigParser.RawConfigParser()
            config.read(expanduser('~/.fitness/config.ini'))
            db_cfg = {t[0]: t[1] for t in config.items('mysql')}
            db_cfg['raise_on_warnings'] = True
            mgr_cfg = {t[0]: t[1] for t in config.items('general')}
            parser = Parser(mgr_cfg, db_cfg)
            bundle = parser.parse_bundle(dlg.GetPath())
            self.loadTree(bundle)


    def OnSave(self, event):
        pass

    def OnColor(self, event):
        pass

    def OnAbout(self, event):
        pass

    def OnOtherColor(self, event):
        pass

    def OnCloseWindow(self, event):
        pass

    def loadTree(self, bundle):
        rootId = self.rootId
        currId = self.tree.AppendItem(rootId, u"课程", 0)
        lessonId = self.tree.AppendItem(rootId, u"子课", 1)
        exerciseId = self.tree.AppendItem(rootId, u"动作", 2)
        for c in bundle.curricula:
            treeItemId = self.tree.AppendItem(currId, text=c.ref_no, image=0)
            self.tree.SetItemPyData(treeItemId, c)
        for l in bundle.lessons:
            treeItemId = self.tree.AppendItem(lessonId, l.title, 1)
            self.tree.SetItemPyData(treeItemId, l)
        for e in bundle.exercises:
            treeItemId = self.tree.AppendItem(exerciseId, e.title, 2)
            self.tree.SetItemPyData(treeItemId, e)
        self.tree.ExpandAll()


if __name__ == '__main__':
    app = wx.App()
    frame = FtFrame(None)
    frame.Show()
    app.MainLoop()
