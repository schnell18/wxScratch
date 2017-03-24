# -*- coding: utf-8 -*-

import ConfigParser
import wx
import wx.aui
from fitness.uilib import IllustrationPanel
from fitness.uilib import ExercisePanel
from fitness.uilib import LessonPanel
from fitness.uilib import LessonExercisePanel
from fitness.uilib import CurriculumPanel
from fitness.parser import Parser
from fitness.model import Curriculum
from fitness.model import Lesson
from fitness.model import LessonExercise
from fitness.model import Exercise
from fitness.model import Illustration
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

        self.imageList = wx.ImageList(16, 16, True)
        for img in [
            'bundle', 'curriculum', 'lesson',
            'exercise', 'illustration', 'segment']:
            bmp = wx.Bitmap(img + '.png', wx.BITMAP_TYPE_PNG)
            self.imageList.Add(bmp)

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

        self.tree.AssignImageList(self.imageList)
        self.rootId = self.tree.AddRoot(u"课程包", 0)

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

        notebook.AssignImageList(self.imageList)
        return notebook

    def createSimpleTool(self, label, filename, help, handler):
        if not label:
            self.toolbar.AddSeparator()
            return
        bmp = wx.Image(filename, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        tool = self.toolbar.AddTool(-1, label, bmp, shortHelp=help)
        # tool = self.toolbar.AddTool(-1, '', bmp, shortHelp=help)
        self.Bind(wx.EVT_MENU, handler, tool)

    def toolbarData(self):
        # return (
        #     ("New", "new.png", u"创建新的课程包", self.OnNew),
        #     ("Open", "open.png", u"打开课程包", self.OnOpen),
        #     ("Save", "save.png", u"保存课程包", self.OnSave),
        #     ("", "", "", ""),
        #     ("Add", "add.png", u"新增", self.OnAdd),
        #     ("Remove", "remove.png", u"删除", self.OnRemove),
        #     ("", "", "", ""),
        #     ("Upload", "upload.png", u"上传", self.OnUpload),
        # )
        return (
            (u"新建", "new.png", u"创建新的课程包", self.OnNew),
            (u"打开", "open.png", u"打开课程包", self.OnOpen),
            (u"保存", "save.png", u"保存课程包", self.OnSave),
            ("", "", "", ""),
            (u"增加", "add.png", u"新增", self.OnAdd),
            (u"删除", "remove.png", u"删除", self.OnRemove),
            ("", "", "", ""),
            (u"导入", "upload.png", u"上传", self.OnUpload),
        )

    def toolbarColorData(self):
        return ("Black", "Red", "Green", "Blue")

    def createToolBar(self):
        self.toolbar = self.CreateToolBar(wx.TB_TEXT)
        for each in self.toolbarData():
            self.createSimpleTool(*each)
        self.toolbar.Realize()

    def OnSelChanged(self, event):
        data = self.tree.GetItemData(event.GetItem())
        if not data:
            return

        notebook = self.right
        page = wx.FindWindowByName(data.name_for_ui(), notebook)
        pageIndex = notebook.GetPageIndex(page)
        if not page and pageIndex < 0 :
            if isinstance(data, Curriculum):
                curr = CurriculumPanel(notebook, data)
                notebook.AddPage(curr, data.title, True, 1)
            elif isinstance(data, Lesson):
                lesson = LessonPanel(notebook, data)
                notebook.AddPage(lesson, data.title, True, 2)
            elif isinstance(data, LessonExercise):
                le = LessonExercisePanel(notebook, data)
                notebook.AddPage(le, data.exercise_ref, True, 5)
            elif isinstance(data, Exercise):
                exercise = ExercisePanel(notebook, data)
                notebook.AddPage(exercise, data.action, True, 3)
            elif isinstance(data, Illustration):
                illustration = IllustrationPanel(notebook, data)
                notebook.AddPage(illustration, data.title, True, 4)
        else:
            self.right.SetSelection(pageIndex)

    def OnNew(self, event):
        pass

    def OnOpen(self, event):
        dlg = wx.DirDialog(
            self,
            message=u"请选择课程包目录"
        )
        if dlg.ShowModal() == wx.ID_OK:
            config = ConfigParser.RawConfigParser()
            config.read(expanduser('~/.fitness/config.ini'))
            db_cfg = {t[0]: t[1] for t in config.items('mysql')}
            db_cfg['raise_on_warnings'] = True
            mgr_cfg = {t[0]: t[1] for t in config.items('general')}
            parser = Parser(mgr_cfg, db_cfg)
            bundle = parser.parse_bundle(dlg.GetPath())
            self.loadTree(bundle)
            self.statusbar.SetStatusText(dlg.GetPath(), 2)
        dlg.Destroy()

    def OnSave(self, event):
        pass

    def OnAdd(self, event):
        treeItemId = self.tree.GetFocusedItem()
        print treeItemId.IsOk()
        if treeItemId.IsOk() and not treeItemId == self.rootId:
            data = self.tree.GetItemData(treeItemId)
            if isinstance(data, Curriculum):
                newTreeItemId = self.tree.InsertItem(
                    self.tree.GetItemParent(treeItemId),
                    treeItemId,
                    "Untitled",
                    1
                )
                c = Curriculum("abc")
                c.description = ''
                c.description = ''
                c.title = "Untitled"
                self.tree.SetItemData(newTreeItemId, c)
                self.tree.EditLabel(newTreeItemId)

    def OnRemove(self, event):
        treeItemId = self.tree.GetFocusedItem()
        if treeItemId.IsOk() and not treeItemId == self.rootId:
            data = self.tree.GetItemData(treeItemId)
            self.tree.Delete(treeItemId)
            notebook = self.right
            page = wx.FindWindowByName(data.name_for_ui(), notebook)
            if page:
                pageIndex = notebook.GetPageIndex(page)
                if pageIndex >= 0:
                    notebook.DeletePage(pageIndex)

    def OnUpload(self, event):
        # TODO: start wizard here
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
        currId = self.tree.AppendItem(rootId, u"课程", 1)
        lessonId = self.tree.AppendItem(rootId, u"子课", 2)
        exerciseId = self.tree.AppendItem(rootId, u"动作", 3)
        for c in bundle.curricula:
            treeItemId = self.tree.AppendItem(currId, text=c.ref_no, image=1)
            self.tree.SetItemData(treeItemId, c)
        for l in bundle.lessons:
            treeItemId = self.tree.AppendItem(lessonId, l.title, 2)
            self.tree.SetItemData(treeItemId, l)
            for seq, le in enumerate(l.lesson_exercises, 1):
                leItemId = self.tree.AppendItem(treeItemId, le.exercise_ref, 5)
                le.ui_ref_no = le.exercise_ref + '-' + str(seq)
                self.tree.SetItemData(leItemId, le)
        for e in bundle.exercises:
            treeItemId = self.tree.AppendItem(exerciseId, e.title, 3)
            self.tree.SetItemData(treeItemId, e)
            for seq, i in enumerate(e.illustrations, 1):
                illuItemId = self.tree.AppendItem(treeItemId, i.title, 4)
                i.ui_ref_no = e.ref_no + '-' + str(seq)
                self.tree.SetItemData(illuItemId, i)
        self.tree.ExpandAll()
        self.tree.EnsureVisible(rootId)


if __name__ == '__main__':
    app = wx.App()
    frame = FtFrame(None)
    frame.Show()
    app.MainLoop()
