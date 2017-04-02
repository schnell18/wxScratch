#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import wx
import wx.aui
import wx.html
from fitness.uilib import BasePanel
from fitness.uilib import IllustrationPanel
from fitness.uilib import ExercisePanel
from fitness.uilib import LessonPanel
from fitness.uilib import LessonExercisePanel
from fitness.uilib import CurriculumPanel
from fitness.uilib import EVT_FORM_DATA_CHG
from fitness.imp import ImpDialog
from fitness.parser import Parser
from fitness.model import Bundle
from fitness.model import Curriculum
from fitness.model import Lesson
from fitness.model import LessonExercise
from fitness.model import Exercise
from fitness.model import Illustration
from os.path import expanduser
from os.path import basename
from os.path import join
from shutil import copy
from datetime import datetime

class AboutDialog(wx.Dialog):
    text = '''
<html>
   <body bgcolor="#ACAA60">
   <center><table bgcolor="#455481" width="100%" cellspacing="0"
   cellpadding="0" border="1">
   <tr>
       <td align="center"><h1>FT课程编辑器</h1></td>
   </tr>
   </table>
   </center>
   <p><b>FT课程编辑器</b>是帮助运营快速编排健身课程的可视化工具,
包括但不限于:
   <ul>
    <li>课程展示, 图片，音频视频预览</li>
    <li>课程、子课、动作编辑</li>
    <li>课程、子课、动作上传</li>
    <li>课程二维码生成</li>
   </ul>
   欲知更多详情请移步至:
   <a href="http://doc.pajk-ent.com/pages/viewpage.action?pageId=39035283">Fitness主页</a>
   </p>
   <p>FT课程编辑器由<a href="mailto:zhangfeng@hys-inc.cn?cc=57432307@qq.com&subject=WellDone">峰哥</a>倾情打造</p>
   </body>
</html>
'''

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, -1, u'关于FT课程编辑器', size=(440, 400))
        html = wx.html.HtmlWindow(self)
        html.SetPage(self.text)
        button = wx.Button(self, wx.ID_OK, u"确定")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(html, 1, wx.EXPAND|wx.ALL, 5)
        sizer.Add(button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.SetSizer(sizer)
        self.Layout()
        self.Centre()


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

        self.imageList = wx.ImageList(24, 24, True)
        for img in [
            'bundle', 'curriculum', 'lesson',
            'exercise', 'illustration', 'segment']:
            bmp = wx.Bitmap(img + '.png', wx.BITMAP_TYPE_PNG)
            self.imageList.Add(bmp)

        self.sp = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        self.left = self.createTreePanel(self.sp)
        self.right = self.createNotbook(self.sp)
        self.sp.SplitVertically(self.left, self.right, 300)

        # manage bundle change status
        self.__dirty__ = False
        self.__drag_item__ = None
        self.Bind(EVT_FORM_DATA_CHG, self.OnFormDataChanged)

        self.Layout()
        self.Centre()

    def __del__(self):
        pass

    def createStatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(2)
        self.statusbar.SetStatusWidths([-3, -1])

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
                ("&New"  , u"新建"  , self.OnNew)  ,
                ("&Open" , u"打开课程包" , self.OnOpen) ,
                ("&Close" , u"关闭课程包" , self.OnClose) ,
                ("&Save" , u"保存课程包" , self.OnSave) ,
                ("", "", ""),
                ("&Quit", u"退出", self.OnCloseWindow),
                ("&About", u"关于", self.OnAbout)
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
        self.tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.OnTreeBeginDrag)
        self.tree.Bind(wx.EVT_TREE_END_DRAG, self.OnTreeEndDrag)

        self.tree.AssignImageList(self.imageList)
        self.treeRootId = self.tree.AddRoot(u"课程包", 0)
        rootId = self.treeRootId
        self.treeCurrId = self.tree.AppendItem(rootId, u"课程", 1)
        self.treeLessonId = self.tree.AppendItem(rootId, u"子课", 2)
        self.treeExerciseId = self.tree.AppendItem(rootId, u"动作", 3)

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

        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose, notebook)
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
        return (
            (u"新建", "new.png", u"创建新的课程包", self.OnNew),
            (u"打开", "open.png", u"打开课程包", self.OnOpen),
            (u"关闭", "close.png", u"关闭课程包", self.OnClose),
            (u"保存", "save.png", u"保存课程包", self.OnSave),
            ("", "", "", ""),
            (u"增加", "add.png", u"新增", self.OnAdd),
            (u"删除", "remove.png", u"删除", self.OnRemove),
            ("", "", "", ""),
            (u"导入", "upload.png", u"导入课程包", self.OnImport),
        )

    def createToolBar(self):
        self.toolbar = self.CreateToolBar(wx.TB_TEXT)
        for each in self.toolbarData():
            self.createSimpleTool(*each)
        self.toolbar.Realize()

    def OnTreeBeginDrag(self, event):
        if self.canDrag(event.GetItem()):
            self.__dragItem__ = event.GetItem()
            event.Allow()
        else:
            event.Veto()

    def OnTreeEndDrag(self, event):
        newItem = event.GetItem()
        oldItem = self.__dragItem__
        if not (newItem and oldItem):
            return

        parentItem = self.tree.GetItemParent(newItem)
        if not parentItem:
            return
        oldParentItem = self.tree.GetItemParent(oldItem)
        # unless drop onto the sibling
        if not oldParentItem == parentItem:
            return
        oldData = self.tree.GetItemData(oldItem)
        oldLabel = self.tree.GetItemText(oldItem)
        oldImage = self.tree.GetItemImage(oldItem)
        self.tree.Delete(oldItem)
        self.tree.InsertItem(
            parentItem,
            newItem,
            oldLabel,
            image=oldImage,
            data=oldData
        )
        # update parent data and mark bundle dirty
        parentData = self.tree.GetItemData(parentItem)
        if isinstance(parentData, Lesson):
            parentData.lesson_exercises = self.get_lesson_exercises(parentItem)
            self._mark_bundle_dirty()

    def canDrag(self, treeItemId):
        if treeItemId:
            data = self.tree.GetItemData(treeItemId)
            return isinstance(data, LessonExercise)
        return False

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
                notebook.AddPage(le, data.title, True, 5)
            elif isinstance(data, Exercise):
                exercise = ExercisePanel(notebook, data)
                notebook.AddPage(exercise, data.title, True, 3)
            elif isinstance(data, Illustration):
                illustration = IllustrationPanel(notebook, data)
                notebook.AddPage(illustration, data.title, True, 4)
        else:
            self.right.SetSelection(pageIndex)

    def OnFormDataChanged(self, event):
        self._mark_bundle_dirty()

    def _mark_bundle_dirty(self):
        self.__dirty__ = True
        text = self.GetTitle()
        if not text.startswith('*'):
            self.SetTitle('* ' + text)
        self.statusbar.SetStatusText(u'课程包已修改, 请注意保存', 0)

    def OnTabClose(self, event):
        notebook = self.right
        pageIndex = event.GetSelection()
        if not pageIndex == wx.NOT_FOUND:
            panel = notebook.GetPage(pageIndex)
            if isinstance(panel, BasePanel) and panel.IsDirty():
                panel.SaveModel()
        event.Allow()

    def OnNew(self, event):
        self._close()

    def OnOpen(self, event):
        self._close()

        dlg = wx.DirDialog(
            self,
            message=u"请选择课程包目录"
        )
        if dlg.ShowModal() == wx.ID_OK:
            parser = self.getParser()
            self.bundle = parser.parse_bundle(dlg.GetPath())
            self.loadTree(self.bundle)
            self.statusbar.SetStatusText('', 1)
            self.SetTitle(u'课程包: [%s]' % dlg.GetPath())
            dest_dir = self._backup_meta_data()
            self.statusbar.SetStatusText(u'课程包定义已备份至: ' + dest_dir, 0)
        dlg.Destroy()

    def OnClose(self, event):
        self._close()

    def OnImport(self, event):
        # save current bundle if it is modified
        if self.__dirty__ and self.bundle:
            dlg = wx.MessageDialog(
                self,
                u'课程包已修改，是否保存后再导入?',
                u'确认',
                wx.YES_NO | wx.ICON_QUESTION
            )
            if dlg.ShowModal() == wx.ID_YES:
                self._save()
            dlg.Destroy()

        dlg = ImpDialog(self, self.bundle)
        dlg.ShowModal()
        dlg.Destroy()

    def OnSave(self, event):
        self._save()
        self.__dirty__ = False

    def _close(self):
        # save current bundle if it is modified
        if self.__dirty__ and self.bundle:
            dlg = wx.MessageDialog(
                self,
                u'课程包已修改，是否保存?',
                u'确认',
                wx.YES_NO | wx.ICON_QUESTION
            )
            result = dlg.ShowModal()
            if result == wx.ID_YES:
                self._save()
            dlg.Destroy()

        notebook = self.right
        notebook.DeleteAllPages()
        self.tree.DeleteChildren(self.treeCurrId)
        self.tree.DeleteChildren(self.treeLessonId)
        self.tree.DeleteChildren(self.treeExerciseId)
        self.bundle = None
        self.__dirty__ == False
        self.SetTitle('')
        self.statusbar.SetStatusText('', 0)
        self.statusbar.SetStatusText('', 1)

    def _backup_meta_data(self):
        # copy bundle yml files to ~/.fitness/backup/<bundle>/META-INF
        path = self.bundle.path
        dest_dir = join(
            expanduser('~/.fitness'),
            'backup',
            basename(path),
            'META-INF',
        )
        if not os.path.exists(dest_dir):
           os.makedirs(dest_dir)
        meta_dir = os.path.join(path, 'META-INF')
        def_files = [
            os.path.join(meta_dir, f) for f in os.listdir(meta_dir)
            if os.path.isfile(os.path.join(meta_dir, f)) and f.endswith(".yml")
        ]
        for df in def_files:
            copy(df, dest_dir)
        return dest_dir

    def _save(self):
        notebook = self.right
        # walk through all dirty pages and save
        for i in range(notebook.GetPageCount()):
            panel = notebook.GetPage(i)
            if isinstance(panel, BasePanel) and panel.IsDirty():
                panel.SaveModel()
                panel.SetDirty(False)
                text = notebook.GetPageText(i)
                if text.startswith('*'):
                    notebook.SetPageText(i, text[1:])

        bundle = Bundle(path=self.bundle.path, data=None)
        # walk through tree and save yml files
        bundle.curricula = self.get_curricula()
        bundle.lessons = self.get_lessons()
        bundle.exercises = self.get_exercises()
        parser = self.getParser()
        parser.save_bundle(bundle)
        self.statusbar.SetStatusText(u"课程包已保存", 0)
        self.statusbar.SetStatusText(u"最近一次保存于" + self.getTimestamp(), 1)
        self._clear_dirty_indicator()

    def _clear_dirty_indicator(self):
        # clear dirty indicator
        title = self.GetTitle()
        if title and title.startswith('*'):
            self.SetTitle(title[1:])

    def getTimestamp(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_curricula(self):
        return self._getChildren(self.tree, self.treeCurrId)

    def get_lessons(self):
        return self._getChildren(self.tree, self.treeLessonId)

    def get_lesson_exercises(self, lessonItemId):
        return self._getChildren(self.tree, lessonItemId)

    def get_exercises(self):
        return self._getChildren(self.tree, self.treeExerciseId)

    def _getChildren(self, tree, parent):
          result = []
          item, cookie = tree.GetFirstChild(parent)
          while item:
              result.append(tree.GetItemData(item))
              item, cookie = tree.GetNextChild(parent, cookie)
          return result

    def getParser(self):
        config = ConfigParser.RawConfigParser()
        config.read(expanduser('~/.fitness/config.ini'))
        db_cfg = {t[0]: t[1] for t in config.items('mysql')}
        db_cfg['raise_on_warnings'] = True
        mgr_cfg = {t[0]: t[1] for t in config.items('general')}
        return Parser(mgr_cfg, db_cfg)

    def OnAdd(self, event):
        treeItemId = self.tree.GetFocusedItem()
        print treeItemId.IsOk()
        if treeItemId.IsOk() and not treeItemId == self.treeRootId:
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

    def OnAbout(self, event):
        dlg = AboutDialog(self)
        dlg.ShowModal()
        dlg.Destroy()

    def OnCloseWindow(self, event):
        # TODO: prompt save if content is dirty
        self.Close()

    def OnRemove(self, event):
        treeItemId = self.tree.GetFocusedItem()
        if self.CanDelete(treeItemId):
            data = self.tree.GetItemData(treeItemId)
            self.tree.Delete(treeItemId)
            notebook = self.right
            page = wx.FindWindowByName(data.name_for_ui(), notebook)
            if page:
                pageIndex = notebook.GetPageIndex(page)
                if pageIndex >= 0:
                    notebook.DeletePage(pageIndex)

    def CanDelete(self, treeItemId):
        return treeItemId.IsOk() and treeItemId != self.treeRootId and treeItemId != self.treeCurrId and treeItemId != self.treeLessonId and treeItemId != self.treeExerciseId

    def loadTree(self, bundle):
        rootId = self.treeRootId
        currId = self.treeCurrId
        lessonId = self.treeLessonId
        exerciseId = self.treeExerciseId
        for c in bundle.curricula:
            treeItemId = self.tree.AppendItem(currId, text=c.title, image=1)
            self.tree.SetItemData(treeItemId, c)
        for l in bundle.lessons:
            treeItemId = self.tree.AppendItem(lessonId, l.title, 2)
            self.tree.SetItemData(treeItemId, l)
            for seq, le in enumerate(l.lesson_exercises, 1):
                leItemId = self.tree.AppendItem(treeItemId, le.title, 5)
                le.ui_ref_no = 'le-' + le.exercise_ref + '-' + str(seq)
                self.tree.SetItemData(leItemId, le)
        for e in bundle.exercises:
            treeItemId = self.tree.AppendItem(exerciseId, e.title, 3)
            self.tree.SetItemData(treeItemId, e)
            for seq, i in enumerate(e.illustrations, 1):
                illuItemId = self.tree.AppendItem(treeItemId, i.title, 4)
                i.ui_ref_no = 'il-' + e.ref_no + '-' + str(seq)
                self.tree.SetItemData(illuItemId, i)
        self.tree.Expand(rootId)
        self.tree.Expand(currId)
        self.tree.Expand(lessonId)
        self.tree.Expand(exerciseId)
        self.tree.EnsureVisible(rootId)


if __name__ == '__main__':
    app = wx.App()
    frame = FtFrame(None)
    frame.Show()
    app.MainLoop()
