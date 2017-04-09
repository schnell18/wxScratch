# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview
import wx.media
import os.path
import re
import platform
from fitness.model import CurriculumLesson
from fitness.util import validate_filename
from .images import catalog
from shutil import copy


ftEVT_PREVIEW_CELL_ADD  = wx.NewEventType()
ftEVT_PREVIEW_CELL_DEL  = wx.NewEventType()
ftEVT_FORM_DATA_CHG     = wx.NewEventType()
ftEVT_SUB_FORM_DATA_CHG = wx.NewEventType()
EVT_PREVIEW_CELL_ADD    = wx.PyEventBinder(ftEVT_PREVIEW_CELL_ADD, 1)
EVT_PREVIEW_CELL_DEL    = wx.PyEventBinder(ftEVT_PREVIEW_CELL_DEL, 1)
EVT_FORM_DATA_CHG       = wx.PyEventBinder(ftEVT_FORM_DATA_CHG, 1)
EVT_SUB_FORM_DATA_CHG   = wx.PyEventBinder(ftEVT_SUB_FORM_DATA_CHG, 1)


def MakePlaceholder(width, height):
    placeholder = wx.Image(width, height)
    placeholder.Replace(0, 0, 0, 255, 255, 255)
    return placeholder.ConvertToBitmap()


class FormDataChangeEvent(wx.CommandEvent):
    def __init__(self, evtType, id):
        wx.CommandEvent.__init__(self, evtType, id)
        self.__dataObject__ = None

    def SetDataObject(self, obj):
        self.__dataObject__ = obj

    def GetDataObject(self):
        return self.__dataObject__


class PreviewCellEvent(wx.CommandEvent):
    def __init__(self, evtType, id):
        wx.CommandEvent.__init__(self, evtType, id)


class BasePanel(wx.Panel):
    def __init__(self, parent, model, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.dirty=False
        self.model=model

        # bind all change events
        self.Bind(wx.EVT_TEXT           , self.OnFormDataChanged)
        self.Bind(wx.EVT_CHOICE         , self.OnFormDataChanged)
        self.Bind(wx.EVT_SPINCTRL       , self.OnFormDataChanged)
        self.Bind(EVT_SUB_FORM_DATA_CHG , self.OnFormDataChanged)

    def SetDirty(self, dirty):
        self.dirty=dirty

    def IsDirty(self):
        return self.dirty

    def SaveModel(self):
        # to be overrided in subclass
        pass

    def OnFormDataChanged(self, evt):
        self.SetDirty(True)
        parent = self.GetParent()
        if isinstance(parent, wx.aui.AuiNotebook):
            pageIndex = parent.GetPageIndex(self)
            if not pageIndex == wx.NOT_FOUND:
                text = parent.GetPageText(pageIndex)
                evtObj = evt.GetEventObject()
                if isinstance(evtObj, wx.TextCtrl) and evtObj.GetName() == 'title':
                    text = evtObj.GetValue()
                    # update display name of related tree node
                    self._change_tree_label(self.model[2], text)

                if not text.startswith('*'):
                    parent.SetPageText(pageIndex, '*' + text)
        self.SaveModel()
        # fire EVT_FORM_DATA_CHG
        newEvt = FormDataChangeEvent(ftEVT_FORM_DATA_CHG, self.GetId())
        newEvt.SetDataObject(self.model[0])
        self.GetEventHandler().ProcessEvent(newEvt)
        evt.Skip()

    def _change_tree_label(self, treeItemId, text):
        frame = wx.GetTopLevelParent(self)
        frame.tree.SetItemText(treeItemId, text)


class FtFileDropTarget(wx.FileDropTarget):
    def __init__(self, parent):
        wx.FileDropTarget.__init__(self)
        self.parent = parent

    def OnEnter(self, x, y, default):
        # self.parent.highlightBorder()
        # self.parent.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
        self.parent.Highlight()
        return wx.DragCopy

    def OnDragOver(self, x, y, default):
        # self.parent.SetCursor(wx.Cursor(wx.CURSOR_NO_ENTRY))
        return wx.DragCopy

    def OnLeave(self):
        # clear highlight
        self.parent.Dehighlight()

    def OnDropFiles(self, x, y, filenames):
        self.parent.Dehighlight()
        return self.parent.Accept(filenames[0])


class ImagePreviewPanel(wx.Panel):
    def __init__(self, parent, width=300, height=200, usage=None, withAddDel=False):
        wx.Panel.__init__(self, parent)

        self.innerPanel = wx.Panel(self, style=wx.NO_BORDER)
        self.innerPanel.SetBackgroundColour(wx.NullColour)
        self.width = width
        self.height = height
        self.relativePath = None
        self.usage = usage

        if withAddDel:
            self.btnPanel = self._createButtonPanel()
            self.btnPanel.Show(False)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.imgCtrl, self.captionLbl = self._create_controls()

        mainSizer.Add(self.imgCtrl, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(self.captionLbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 0)
        self.innerPanel.SetSizerAndFit(mainSizer)

        dt = FtFileDropTarget(self)
        self.SetDropTarget(dt)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        if withAddDel:
            self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnterWindow)
            self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeaveWindow)

    def Highlight(self):
        self.SetBackgroundColour('green')
        self.Refresh()

    def Dehighlight(self):
        self.SetBackgroundColour(wx.NullColour)
        self.Refresh()

    def GetRelativePath(self):
        return self.relativePath

    def Accept(self, path):
        # check if the file is of supported type
        if not re.search(r'png$|gif$|jpg$', path):
            return False

        rel_path = self._copy_file(path)
        # copy into bundle directory
        if self.LoadWithRelPath(self.baseDir, rel_path):
            newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
            self.GetEventHandler().ProcessEvent(newEvt)
        return True

    def LoadWithRelPath(self, base_dir, rel_path):
        self.baseDir = base_dir
        if rel_path and os.path.exists(base_dir):
            self.relativePath = rel_path
            fp = os.path.join(base_dir, *rel_path.split('/'))
            return self._load(fp)
        return False

    def LoadWithPlaceHolder(self, base_dir):
        self.baseDir = base_dir
        placeholder = MakePlaceholder(self.width, self.height)
        self.imgCtrl.SetBitmap(placeholder)
        txt = u"宽高 %d X %d" % (self.width, self.height)
        self.captionLbl.SetLabel(txt)
        return True

    def _load(self, path):
        if os.path.exists(path):
            bmp = wx.Bitmap(path)
            (width, height) = (bmp.GetWidth(), bmp.GetHeight())
            # scale to fit
            self.imgCtrl.SetBitmap(self._scale_to_fit(bmp))
            txt = u"宽高 %d X %d" % (width, height)
            self.captionLbl.SetLabel(txt)
            return True
        return False

    def _copy_file(self, path):
        rel_dir = 'image'
        if self.usage:
            rel_dir = '/'.join([rel_dir, self.usage])
        dest_dir = os.path.join(self.baseDir, *rel_dir.split('/'))
        if not os.path.exists(dest_dir):
           os.makedirs(dest_dir)
        filename = os.path.basename(path)
        if not validate_filename(filename):
            filename = self._get_auto_name(path)
        copy(path, os.path.join(dest_dir, filename))
        rel_path = '/'.join([rel_dir, filename])
        return rel_path

    def _get_auto_name(self, path):
        idx = path.rindex('.') + 1
        ext_name = path[idx:]
        frame = wx.GetTopLevelParent(self)
        seq = frame.autoNumber.acquire('image')
        return 'img%04d.%s' % (seq, ext_name)

    def _create_controls(self):
        # image preview area
        placeholder = MakePlaceholder(self.width, self.height)
        imgCtrl = wx.StaticBitmap(
            self.innerPanel,
            wx.ID_ANY,
            placeholder,
            style=wx.NO_BORDER
        )
        captionLbl = wx.StaticText(self.innerPanel, wx.ID_ANY, "")
        captionLbl.Wrap(-1)
        return imgCtrl, captionLbl

    def _createButtonPanel(self):
        btnPanel = wx.Panel(self, pos=(0, 0))
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        img = catalog['addimg2'].GetImage()
        img = img.Size((24, 24), (4, 4))
        bmp = img.ConvertToBitmap()
        addBtn = wx.BitmapButton(btnPanel, bitmap=bmp)
        img = catalog['delimg2'].GetImage()
        img = img.Size((24, 24), (4, 4))
        bmp = img.ConvertToBitmap()
        delBtn = wx.BitmapButton(btnPanel, bitmap=bmp)
        hSizer.Add(addBtn, 0, wx.ALL, 0)
        hSizer.Add(delBtn, 0, wx.ALL, 0)

        self.Bind(wx.EVT_BUTTON, self.OnAddBtnPressed, addBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDelBtnPressed, delBtn)
        btnPanel.SetSizer(hSizer)
        btnPanel.Fit()
        return btnPanel

    def OnSize(self, event):
        size = event.GetSize()
        self.innerPanel.SetPosition((2, 2))
        self.innerPanel.SetSize((size.x-4, size.y-4))
        event.Skip()

    def OnEnterWindow(self, event):
        self.btnPanel.Show(True)

    def OnLeaveWindow(self, event):
        self.btnPanel.Show(False)

    def OnAddBtnPressed(self, event):
        newEvt = PreviewCellEvent(ftEVT_PREVIEW_CELL_ADD, self.GetId())
        newEvt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(newEvt)
        event.Skip()

    def OnDelBtnPressed(self, event):
        newEvt = PreviewCellEvent(ftEVT_PREVIEW_CELL_DEL, self.GetId())
        newEvt.SetEventObject(self)
        self.GetEventHandler().ProcessEvent(newEvt)
        event.Skip()

    def _scale_to_fit(self, bmp):
        (width, height) = (bmp.GetWidth(), bmp.GetHeight())
        factor = max(width / self.width, height / self.height)
        if factor > 1:
            img = bmp.ConvertToImage()
            img.Rescale(width / factor, height / factor)
            bmp = wx.Bitmap(img)
        return bmp

    def __del__(self):
        pass


class AvPreviewPanel(wx.Panel):
    def __init__(self, parent, usage=None, mediaType='audio', width=300, height=200):
        wx.Panel.__init__(self, parent)

        self.width = width
        self.height = height
        self.mediaType = mediaType
        self.usage = usage
        self.relativePath = None
        self.valRegex = self._create_validation_regex(mediaType)

        self.innerPanel = wx.Panel(self, style=wx.NO_BORDER)
        self.innerPanel.SetBackgroundColour(wx.NullColour)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.mediaCtrl, self.captionLbl = self._create_controls()

        mainSizer.Add(self.mediaCtrl, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        mainSizer.Add(self.captionLbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.innerPanel.SetSizerAndFit(mainSizer)

        dt = FtFileDropTarget(self)
        self.SetDropTarget(dt)

        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        self.Bind(wx.EVT_SIZE, self.OnSize)

    def OnSize(self, event):
        size = event.GetSize()
        self.innerPanel.SetPosition((2, 2))
        self.innerPanel.SetSize((size.x-4, size.y-4))
        event.Skip()

    def Highlight(self):
        self.SetBackgroundColour('green')
        self.Refresh()

    def Dehighlight(self):
        self.SetBackgroundColour(wx.NullColour)
        self.Refresh()

    def GetRelativePath(self):
        return self.relativePath

    def Accept(self, path):
        # check if the file is of supported type
        if not self.valRegex.search(path):
            return False
        # copy into bundle directory
        rel_path = self._copy_file(path)

        if self.LoadWithRelPath(self.baseDir, rel_path):
            newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
            self.GetEventHandler().ProcessEvent(newEvt)
        return True

    def LoadWithRelPath(self, base_dir, rel_path):
        self.baseDir = base_dir
        if rel_path and os.path.exists(base_dir):
            self.relativePath = rel_path
            fp = os.path.join(base_dir, *rel_path.split('/'))
            return self._load(fp)
        return False

    def OnMediaLoaded(self, evt):
        self.mediaCtrl.Pause()
        txt = self._formatDuration(self.mediaCtrl.Length())
        self.captionLbl.SetLabel(txt)
        if platform.system() == 'Windows':
            self.mediaCtrl.ShowPlayerControls(wx.media.MEDIACTRLPLAYERCONTROLS_NONE)
        else:
            self.mediaCtrl.ShowPlayerControls(wx.media.MEDIACTRLPLAYERCONTROLS_DEFAULT)

    def _load(self, path):
        if os.path.exists(path):
            return self.mediaCtrl.Load(path)
        return False

    def _copy_file(self, path):
        rel_dir = self.mediaType
        if self.usage:
            rel_dir = '/'.join([rel_dir, self.usage])
        dest_dir = os.path.join(self.baseDir, *rel_dir.split('/'))
        if not os.path.exists(dest_dir):
           os.makedirs(dest_dir)
        filename = os.path.basename(path)
        if not validate_filename(filename):
            filename = self._get_auto_name(path)
        copy(path, os.path.join(dest_dir, filename))
        rel_path = '/'.join([rel_dir, filename])
        return rel_path

    def _get_auto_name(self, path):
        ext_name = os.path.basename(path).split(os.path.extsep)[1]
        frame = wx.GetTopLevelParent(self)
        seq = frame.autoNumber.acquire(self.mediaType)
        return '%s%04d.%s' % (
            'v' if self.mediaType == 'video' else 'a',
            seq,
            ext_name
        )

    def _create_controls(self):
        extra_args = {
            'size'  : (self.width, self.height),
            'style' : wx.SIMPLE_BORDER
        }
        if platform.system() == 'Windows':
            extra_args['szBackend'] = wx.media.MEDIABACKEND_WMP10
        mediaCtrl = wx.media.MediaCtrl(
            self.innerPanel,
            wx.ID_ANY,
            **extra_args
        )
        mediaCtrl.SetPlaybackRate(1)
        mediaCtrl.SetVolume(1)
        captionLbl = wx.StaticText(self.innerPanel, wx.ID_ANY, "")
        captionLbl.Wrap(-1)
        return (mediaCtrl, captionLbl)

    def _formatDuration(self, milli_seconds):
        seconds = milli_seconds / 1000 % 60
        mins = milli_seconds / 1000 / 60 % 60
        hours = milli_seconds / 1000 / 3600 % 60
        return u"时长 %02d:%02d:%02d" % (hours, mins, seconds)

    def _create_validation_regex(self, mediaType):
        regex = None
        if mediaType == 'audio':
            regex = re.compile(r'mp3$')
        elif mediaType == 'image':
            regex = re.compile(r'png$|jpg$|gif$')
        else:
            regex = re.compile(r'mp4$')
        return regex

    def __del__(self):
        if self.mediaCtrl and self.mediaCtrl.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.mediaCtrl.Stop()


class LessonAudioPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            id = wx.ID_ANY,
            size = (500, -1),
            style = wx.TAB_TRAVERSAL
        )

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.dvAudio = wx.dataview.DataViewListCtrl(
            self,
            wx.ID_ANY,
            style=wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES
        )
        self.dvAudio.SetMinSize((-1, 120))

        # prevent in-place editting
        render = wx.dataview.DataViewSpinRenderer(
            1,
            10000,
            mode=wx.dataview.DATAVIEW_CELL_INERT
        )
        dvPos = wx.dataview.DataViewColumn(u"位置", render, 0, width=150)
        self.colPos = self.dvAudio.AppendColumn(dvPos)
        self.colAudio = self.dvAudio.AppendTextColumn(
            label=u"音频",
            width=360,
            mode=wx.dataview.DATAVIEW_CELL_EDITABLE
        )
        mainSizer.Add(self.dvAudio, 7, wx.ALL, 5)
        self.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED,
            self.OnSelected,
            self.dvAudio
        )

        btnSizer = wx.BoxSizer(wx.VERTICAL)

        self.addBtn  = wx.Button(self, wx.ID_ANY, u"增加")
        self.delBtn  = wx.Button(self, wx.ID_ANY, u"删除")
        self.upBtn   = wx.Button( self, wx.ID_ANY, u"上移")
        self.downBtn = wx.Button( self, wx.ID_ANY, u"下移")

        self.delBtn.Enable(False)
        self.upBtn.Enable(False)
        self.downBtn.Enable(False)

        btnSizer.Add(self.addBtn,  0, wx.ALL, 5)
        btnSizer.Add(self.delBtn,  0, wx.ALL, 5)
        btnSizer.Add(self.upBtn,   0, wx.ALL, 5)
        btnSizer.Add(self.downBtn, 0, wx.ALL, 5)

        mainSizer.Add(btnSizer, 1, wx.EXPAND, 5)
        self.SetSizer(mainSizer)
        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.OnAdd,  self.addBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDel,  self.delBtn)
        self.Bind(wx.EVT_BUTTON, self.OnUp,   self.upBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDown, self.downBtn)
        self.Bind(wx.EVT_BUTTON, self.OnFormDataChanged)
        self.Bind(wx.dataview.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnFormDataChanged)

    def OnSelected(self, evt):
        self.delBtn.Enable(True)
        self.upBtn.Enable(True)
        self.downBtn.Enable(True)

    def OnFormDataChanged(self, evt):
        # fire EVT_SUB_FORM_DATA_CHG
        newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
        self.GetEventHandler().ProcessEvent(newEvt)
        evt.Skip()

    def OnAdd(self, evt):
        pos = self._get_max_position()
        self.dvAudio.AppendItem([pos + 1, u'audio/act/FIXME.mp3'])

    def OnDel(self, evt):
        row = self.dvAudio.GetSelectedRow()
        if not row == wx.NOT_FOUND:
            self.dvAudio.DeleteItem(row)

    def OnUp(self, evt):
        row = self.dvAudio.GetSelectedRow()
        if row != wx.NOT_FOUND and row > 0:
            old = [
                self.dvAudio.GetValue(row, 0),
                self.dvAudio.GetValue(row, 1)
            ]
            self.dvAudio.DeleteItem(row)
            self.dvAudio.InsertItem(row - 1, old)
            self.dvAudio.SelectRow(row - 1)

    def OnDown(self, evt):
        row = self.dvAudio.GetSelectedRow()
        if row != wx.NOT_FOUND and row < self.dvAudio.GetItemCount() - 1:
            old = self._get_row_data(row)
            self.dvAudio.DeleteItem(row)
            self.dvAudio.InsertItem(row + 1, old)
            self.dvAudio.SelectRow(row + 1)

    def AddRow(self, row):
        self.dvAudio.AppendItem(row)

    def _get_max_position(self):
        max_pos = 1
        for i in range(self.dvAudio.GetItemCount()):
            pos = int(self.dvAudio.GetValue(i, 0))
            if max_pos < pos:
               max_pos = pos
        return max_pos

    def _get_row_data(self, row):
        return [
            self.dvAudio.GetValue(row, 0),
            self.dvAudio.GetValue(row, 1)
        ]


class CurriLessonPanel(wx.Panel):
    def __init__(self, parent, width, height):
        wx.Panel.__init__(
            self,
            parent,
            id = wx.ID_ANY,
            size = (500, -1),
            style = wx.TAB_TRAVERSAL
        )

        mainSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.dvLesson = wx.dataview.DataViewListCtrl(
            self,
            wx.ID_ANY,
            style=wx.dataview.DV_ROW_LINES|wx.dataview.DV_VERT_RULES
        )
        self.dvLesson.SetMinSize((-1, 150))

        # TODO: reset choices when new lesson is added
        choices = self._get_lesson_refnos()
        # prevent in-place editting
        render = wx.dataview.DataViewChoiceRenderer(
            choices,
            mode=wx.dataview.DATAVIEW_CELL_INERT
        )
        dvCol = wx.dataview.DataViewColumn(u"编号", render, 0, width=150)
        self.colRefNo = self.dvLesson.AppendColumn(dvCol)
        self.colTitle = self.dvLesson.AppendTextColumn(
            label=u"标题",
            width=200,
            mode=wx.dataview.DATAVIEW_CELL_EDITABLE
        )
        self.colBreak = self.dvLesson.AppendToggleColumn(u"休息")
        mainSizer.Add(self.dvLesson, 7, wx.ALL, 5)
        self.Bind(
            wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED,
            self.OnSelected,
            self.dvLesson
        )

        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.AddSpacer(20)

        self.addBtn  = wx.Button(self, wx.ID_ANY, u"增加")
        self.delBtn  = wx.Button(self, wx.ID_ANY, u"删除")
        self.upBtn   = wx.Button( self, wx.ID_ANY, u"上移")
        self.downBtn = wx.Button( self, wx.ID_ANY, u"下移")

        self.delBtn.Enable(False)
        self.upBtn.Enable(False)
        self.downBtn.Enable(False)

        btnSizer.Add(self.addBtn,  0, wx.ALL, 5)
        btnSizer.Add(self.delBtn,  0, wx.ALL, 5)
        btnSizer.Add(self.upBtn,   0, wx.ALL, 5)
        btnSizer.Add(self.downBtn, 0, wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnAdd,  self.addBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDel,  self.delBtn)
        self.Bind(wx.EVT_BUTTON, self.OnUp,   self.upBtn)
        self.Bind(wx.EVT_BUTTON, self.OnDown, self.downBtn)
        self.Bind(wx.EVT_BUTTON, self.OnFormDataChanged)
        self.Bind(wx.dataview.EVT_DATAVIEW_ITEM_VALUE_CHANGED, self.OnFormDataChanged)

        mainSizer.Add(btnSizer, 1, wx.EXPAND, 5)
        self.SetSizer(mainSizer)
        self.Layout()

    def OnSelected(self, evt):
        self.delBtn.Enable(True)
        self.upBtn.Enable(True)
        self.downBtn.Enable(True)

    def OnFormDataChanged(self, evt):
        # fire EVT_SUB_FORM_DATA_CHG
        newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
        self.GetEventHandler().ProcessEvent(newEvt)
        evt.Skip()

    def UpdateLessonSource(self):
        pass

    def OnAdd(self, evt):
        ref_no = self._get_lesson_refnos()[0]
        self.dvLesson.AppendItem([ref_no, u'请输入标题', False])

    def OnDel(self, evt):
        row = self.dvLesson.GetSelectedRow()
        if not row == wx.NOT_FOUND:
            self.dvLesson.DeleteItem(row)

    def OnUp(self, evt):
        row = self.dvLesson.GetSelectedRow()
        if row != wx.NOT_FOUND and row > 0:
            old = [
                self.dvLesson.GetValue(row, 0),
                self.dvLesson.GetValue(row, 1),
                self.dvLesson.GetValue(row, 2)
            ]
            self.dvLesson.DeleteItem(row)
            self.dvLesson.InsertItem(row - 1, old)
            self.dvLesson.SelectRow(row - 1)

    def OnDown(self, evt):
        row = self.dvLesson.GetSelectedRow()
        if row != wx.NOT_FOUND and row < self.dvLesson.GetItemCount() - 1:
            old = self._get_row_data(row)
            self.dvLesson.DeleteItem(row)
            self.dvLesson.InsertItem(row + 1, old)
            self.dvLesson.SelectRow(row + 1)

    def AddRow(self, row):
        self.dvLesson.AppendItem(row)

    def GetCurriculumLessons(self):
        curri_lessons = []
        for row in range(self.dvLesson.GetItemCount()):
            curri_lessons.append(self._get_row_data(row))
        return curri_lessons

    def _get_lesson_refnos(self):
        frame = wx.GetTopLevelParent(self)
        return [l.ref_no for l in frame.get_lessons()]

    def _get_row_data(self, row):
        return [
            self.dvLesson.GetValue(row, 0),
            self.dvLesson.GetValue(row, 1),
            self.dvLesson.GetValue(row, 2)
        ]


class CurriculumPanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=str(id(model[2])))
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scrollWin.SetScrollRate(5, 5)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        biSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"基本信息"
            ),
            wx.VERTICAL
        )

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"课程编号",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.refNoLabel.Wrap(-1)

        self.refNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            name='title'
        )

        self.decriptionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.decriptionLabel.Wrap(-1)

        self.descriptionText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            size=(-1, 40),
            style=wx.TE_MULTILINE
        )

        self.cornerTypeLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"角标类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.cornerTypeLabel.Wrap(-1)

        cornerTypes = [u'无', u'新', u'推荐', u'热门']
        self.cornerTypeChoice = wx.Choice(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            cornerTypes,
            0
        )
        self.cornerTypeChoice.SetSelection(0)

        self.previewVideoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"预览视频",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.previewVideoLabel.Wrap(-1)

        self.previewVideoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.previewVideoText.Bind(wx.EVT_TEXT, self.OnVideoChanged)

        # video preview area
        extra_args = {
            'size'  : (150, 100),
            'style' : wx.SIMPLE_BORDER
        }
        if platform.system() == 'Windows':
            extra_args['szBackend'] = wx.media.MEDIABACKEND_WMP10
        self.mediaCtrl = wx.media.MediaCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            **extra_args
        )

        self.mediaCtrl.SetPlaybackRate(1)
        self.mediaCtrl.SetVolume(1)
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)

        self.coverLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"封面",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.coverLabel.Wrap(-1)

        self.coverPanel = ImagePreviewPanel(
            biSizer.GetStaticBox(),
            width=300,
            height=100
        )

        self.iconLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"图标",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.iconLabel.Wrap(-1)

        self.iconPanel = ImagePreviewPanel(
            biSizer.GetStaticBox(),
            width=150,
            height=100
        )

        bifSizer = wx.FlexGridSizer(7, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.AddGrowableRow(2)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(100, -1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.titleText, 1, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.decriptionLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.cornerTypeLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.cornerTypeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.previewVideoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.previewVideoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(self.mediaCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        bifSizer.Add(self.coverLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.coverPanel, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.iconLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.iconPanel, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        biSizer.Add(bifSizer, 0, wx.ALL | wx.EXPAND, 5)

        lessonsSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"子课编排"
            ),
            wx.VERTICAL
        )

        self.dvLessons = CurriLessonPanel(
            lessonsSizer.GetStaticBox(),
            500,
            300
        )
        lessonsSizer.Add( self.dvLessons, 1, wx.ALL|wx.EXPAND, 5)

        relatedSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"相关课程"
            ),
            wx.VERTICAL
        )

        self.dvRelated = wx.dataview.DataViewListCtrl(
            relatedSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvRelatedRefNo = self.dvRelated.AppendTextColumn(u"课程编号")
        self.dvRelatedTitle = self.dvRelated.AppendTextColumn(u"标题")
        self.dvRelatedCover = self.dvRelated.AppendTextColumn(u"封面")
        relatedSizer.Add(self.dvRelated, 0, wx.ALL|wx.EXPAND, 5)

        scrollSizer.Add(biSizer, 0, wx.ALL|wx.EXPAND, 5)
        scrollSizer.Add(lessonsSizer, 0, wx.ALL|wx.EXPAND, 5)
        scrollSizer.Add(relatedSizer, 1, wx.EXPAND|wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.LoadModel()
        self.Layout()

    def LoadModel(self):
        model = self.model[0]
        self.refNoText.ChangeValue(
            model.ref_no if model.ref_no else ''
        )
        self.titleText.ChangeValue(
            model.title if model.title else ''
        )
        self.descriptionText.ChangeValue(
            model.description if model.description else ''
        )
        self.cornerTypeChoice.SetSelection(
            model.corner_label_type if model.corner_label_type else 0
        )
        self.previewVideoText.ChangeValue(
            model.preview_video if model.preview_video else ''
        )

        # load lessons
        if model.curriculum_lessons:
            for l in model.curriculum_lessons:
                row = [l.lesson_ref, l.lesson_title, l.is_break]
                self.dvLessons.AddRow(row)

        # load related curriculum
        if model.next_curricula:
            for curr in model.next_curricula:
                row = [curr.ref_no, curr.title, curr.cover]
                self.dvRelated.AppendItem(row)

        self._loadVideo()
        frame = wx.GetTopLevelParent(self)
        base_dir = frame.bundle.path
        self.coverPanel.LoadWithRelPath(base_dir, model.cover)
        self.iconPanel.LoadWithRelPath(base_dir, model.icon)

    def SaveModel(self):
        model = self.model[0]
        model.ref_no = self.refNoText.GetValue()
        model.title = self.titleText.GetValue()
        model.description = self.descriptionText.GetValue()
        model.corner_label_type = self.cornerTypeChoice.GetSelection()
        model.preview_video = self.previewVideoText.GetValue()
        model.cover = self.coverPanel.GetRelativePath()
        model.icon = self.iconPanel.GetRelativePath()
        # assembly curriculum lessons
        model.curriculum_lessons = []
        curri_lessons = self.dvLessons.GetCurriculumLessons()
        for cl in curri_lessons:
            model.curriculum_lessons.append(
                CurriculumLesson(
                    lesson_ref=cl[0],
                    lesson_title=cl[1],
                    is_break=cl[2]
                )
            )

        # TODO: assembly next curriculua

    def UpdateLessonSource(self):
        self.dvLessons.UpdateLessonSource()

    def OnMediaLoaded(self, evt):
        self.mediaCtrl.Pause()
        if not platform.system() == 'Windows':
            self.mediaCtrl.ShowPlayerControls(wx.media.MEDIACTRLPLAYERCONTROLS_DEFAULT)

    def OnVideoChanged(self, evt):
        self._loadVideo()

    def _loadVideo(self):
        url = self.previewVideoText.GetValue()
        if re.match('^http(s)?://', url):
            self.mediaCtrl.LoadURI(url)

    def __del__(self):
        if self.mediaCtrl and self.mediaCtrl.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.mediaCtrl.Stop()


class LessonPanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=str(id(model[2])))
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        self.scrollWin.SetScrollRate(5, 5)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        biSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"基本信息"
            ),
            wx.VERTICAL
        )

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"子课编号",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.refNoLabel.Wrap(-1)

        self.refNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.typeLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.typeLabel.Wrap(-1)

        typeChoices = [u'健身', u'瑜伽']
        self.typeChoice = wx.Choice(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            typeChoices,
            0
        )
        self.typeChoice.SetSelection(0)

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            name='title'
        )

        self.descriptionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.descriptionLabel.Wrap(-1)

        self.descriptionText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, 80),
            wx.TE_MULTILINE
        )

        self.encourageLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"激励文案",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.encourageLabel.Wrap(-1)

        self.encourageText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.nextDayIntroLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"结课文案",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.nextDayIntroLabel.Wrap(-1)

        self.nextDayIntroText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.bgmMusicLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"背景音乐",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.bgmMusicLabel.Wrap(-1)

        self.prAudio = AvPreviewPanel(
            biSizer.GetStaticBox(),
            width=150,
            height=100,
            usage='bgm'
        )

        bifSizer = wx.FlexGridSizer(7, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        # bifSizer.AddGrowableRow(3)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.typeLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.typeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.titleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.descriptionLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.encourageLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.encourageText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.nextDayIntroLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.nextDayIntroText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.bgmMusicLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.prAudio, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(100, 0)

        biSizer.Add(bifSizer, 1, wx.EXPAND, 5)

        scrollSizer.Add(biSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.LoadModel()
        self.SetSizer(panelSizer)

    def LoadModel(self):
        model = self.model[0]
        self.refNoText.ChangeValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.titleText.ChangeValue(model.title)
        self.descriptionText.ChangeValue(model.description)
        self.encourageText.ChangeValue(model.encouragement)
        self.nextDayIntroText.ChangeValue(model.next_day_intro)
        frame = wx.GetTopLevelParent(self)
        self.prAudio.LoadWithRelPath(frame.bundle.path, model.bg_music)

    def SaveModel(self):
        model = self.model[0]
        model.ref_no = self.refNoText.GetValue()
        model.type = self.typeChoice.GetSelection() + 1
        model.title = self.titleText.GetValue()
        model.description = self.descriptionText.GetValue()
        model.encouragement = self.encourageText.GetValue()
        model.next_day_intro = self.nextDayIntroText.GetValue()
        model.bg_music = self.prAudio.GetRelativePath()

    def __del__(self):
        pass


class LessonExercisePanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=str(id(model[2])))
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        self.scrollWin.SetScrollRate(5, 5)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        biSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作编排"
            ),
            wx.VERTICAL
        )

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"动作编号"
        )
        self.refNoLabel.Wrap(-1)

        self.refNoText = wx.ComboBox(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            choices=self._get_exercise_nos()
        )

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            name='title'
        )

        self.repetitionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"重复"
        )
        self.repetitionLabel.Wrap(-1)

        self.repetitionSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            max=100
        )

        self.measureLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"单位",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.measureLabel.Wrap(-1)

        measureChoices = [u'次', u'秒']
        self.measureChoice = wx.Choice(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            choices=measureChoices
        )
        self.measureChoice.SetSelection(0)

        bifSizer = wx.FlexGridSizer(0, 3, hgap=4, vgap=4)
        bifSizer.AddGrowableCol(1)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(100, 0)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.titleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.repetitionLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.repetitionSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.measureLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.measureChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        biSizer.Add(bifSizer, 0, wx.EXPAND | wx.ALL, 5)

        bvSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"准备音"
            ),
            wx.VERTICAL
        )

        self.beginVoices = LessonAudioPanel(bvSizer.GetStaticBox())
        bvSizer.Add(self.beginVoices, 1, wx.ALL|wx.EXPAND, 5)

        mdSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作音"
            ),
            wx.VERTICAL
        )

        self.midVoices = LessonAudioPanel(mdSizer.GetStaticBox())
        mdSizer.Add(self.midVoices, 1, wx.ALL|wx.EXPAND, 5)

        scrollSizer.Add(biSizer, 0, wx.EXPAND | wx.ALL, 5)
        scrollSizer.Add(bvSizer, 0, wx.EXPAND | wx.ALL, 5)
        scrollSizer.Add(mdSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.LoadModel()
        self.SetSizerAndFit(panelSizer)

    def LoadModel(self):
        model = self.model[0]
        self.refNoText.ChangeValue(model.exercise_ref)
        self.titleText.ChangeValue(model.title)
        self.measureChoice.SetSelection(model.measure - 1)
        self.repetitionSpin.SetValue(model.repetition)

        # load begin voices
        if model.begin_voices:
            for bv in sorted(model.begin_voices, key=lambda e : e.position):
                row = [str(bv.position), bv.audio_name]
                self.beginVoices.AddRow(row)

        # load mid voices
        if model.mid_voices:
            for bv in model.mid_voices:
                row = [str(bv.position), bv.audio_name]
                self.midVoices.AddRow(row)

    def SaveModel(self):
        model = self.model[0]
        model.exercise_ref = self.refNoText.GetValue()
        model.title = self.titleText.GetValue()
        model.measure = self.measureChoice.GetSelection() + 1
        model.repetition = self.repetitionSpin.GetValue()

        # TODO: save begin voices

        # TODO: save mid voices

    def UpdateExerciseSource(self):
        exNos = self._get_exercise_nos()
        self.refNoText.SetItems(exNos)

    def _get_exercise_nos(self):
        frame = wx.GetTopLevelParent(self)
        return [e.ref_no for e in frame.get_exercises()]


class ExercisePanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=str(id(model[2])))
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        self.scrollWin.SetScrollRate(5, 5)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        biSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"基本信息"
            ),
            wx.VERTICAL
        )

        self.exerciseRefNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"动作编号",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.exerciseRefNoLabel.Wrap(-1)

        self.exerciseRefNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.typeLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.typeLabel.Wrap(-1)

        typeChoices = [u'练习', u'休息']
        self.typeChoice = wx.Choice(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            typeChoices,
            0
        )
        self.typeChoice.SetSelection(0)

        self.nameLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"名称",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.nameLabel.Wrap(-1)

        self.nameText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            name='title'
        )

        self.caloriesLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"卡路里",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.caloriesLabel.Wrap(-1)

        self.caloriesSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
            max=100000
        )

        self.durationLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"时长",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.durationLabel.Wrap(-1)

        self.durationSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
            max=100000
        )

        # image preview area
        self.previewImgLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"预览图",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.previewImgLabel.Wrap(-1)
        self.prImg = ImagePreviewPanel(biSizer.GetStaticBox(), usage='act')

        # video preview area
        self.videoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"视频",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.videoLabel.Wrap(-1)
        self.prVideo = AvPreviewPanel(
            biSizer.GetStaticBox(),
            usage='act',
            mediaType='video'
        )


        bifSizer = wx.FlexGridSizer(8, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        bifSizer.Add(self.exerciseRefNoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.exerciseRefNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.typeLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.typeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.nameLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.nameText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.titleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.caloriesLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.caloriesSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.durationLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.durationSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(100, 0)
        bifSizer.Add(self.previewImgLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.prImg, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        bifSizer.Add(self.videoLabel, 0, wx.ALL, 5)
        bifSizer.Add(self.prVideo, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        biSizer.Add(bifSizer, 0, wx.ALL | wx.EXPAND, 5)

        scrollSizer.Add(biSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.LoadModel()
        self.Layout()

    def LoadModel(self):
        model = self.model[0]
        self.exerciseRefNoText.ChangeValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.durationSpin.SetValue(model.duration)
        self.titleText.ChangeValue(model.title)
        if model.type == 1:
            frame = wx.GetTopLevelParent(self)
            self.nameText.ChangeValue(model.action)
            self.caloriesSpin.SetValue(model.calories)
            self.prImg.LoadWithRelPath(frame.bundle.path, model.thumbnail)
            self.prVideo.LoadWithRelPath(frame.bundle.path, model.video_name)

    def SaveModel(self):
        model = self.model[0]
        model.ref_no = self.exerciseRefNoText.GetValue()
        model.type = self.typeChoice.GetSelection() + 1
        model.duration = self.durationSpin.GetValue()
        model.title = self.titleText.GetValue()
        if model.type == 1:
            model.action = self.nameText.GetValue()
            model.calories = self.caloriesSpin.GetValue()
            model.thumbnail = self.prImg.GetRelativePath()
            model.video_name = self.prVideo.GetRelativePath()

    def __del__(self):
        pass


class IllustrationPanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=str(id(model[2])))
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        self.prImgs = []
        self.scrollWin.SetScrollRate(5, 5)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSizer = wx.BoxSizer(wx.VERTICAL)

        illuSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作详解"
            ),
            wx.VERTICAL
        )

        self.illuTitleLabel = wx.StaticText(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.illuTitleLabel.Wrap(-1)

        self.illuTitleText = wx.TextCtrl(
            illuSizer.GetStaticBox(),
            id=wx.ID_ANY,
            name='title'
        )

        self.illuDescriptionLabel = wx.StaticText(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.illuDescriptionLabel.Wrap(-1)

        self.illuDescriptionText = wx.TextCtrl(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, 160),
            wx.TE_MULTILINE
        )

        illufSizer = wx.FlexGridSizer(3, 3, 0, 0)
        illufSizer.AddGrowableCol(1)
        illufSizer.SetFlexibleDirection(wx.BOTH)
        illufSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        illufSizer.Add(self.illuTitleLabel, 0, wx.ALL, 5)
        illufSizer.Add(self.illuTitleText, 0, wx.ALL|wx.EXPAND, 5)
        illufSizer.AddSpacer(100)
        illufSizer.Add(self.illuDescriptionLabel, 0, wx.ALL, 5)
        illufSizer.Add(self.illuDescriptionText, 0, wx.ALL|wx.EXPAND, 5)
        illufSizer.AddSpacer(1)

        self.gSizer = wx.GridSizer(0, 2, hgap=4, vgap=4)
        illuSizer.Add(illufSizer, 0, wx.EXPAND, 5)
        illuSizer.Add(self.gSizer, 1, wx.EXPAND | wx.ALL, 0)

        scrollSizer.Add(illuSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.illuSizer = illuSizer
        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.LoadModel()
        self.Layout()

    def LoadModel(self):
        model = self.model[0]
        self.illuTitleText.ChangeValue(model.title)
        self.illuDescriptionText.ChangeValue(model.description)
        self._layout_images()

    def SaveModel(self):
        model = self.model[0]
        model.title = self.illuTitleText.GetValue()
        model.description = self.illuDescriptionText.GetValue()
        if self.prImgs:
            model.images = []
            for prImg in self.prImgs:
                model.images.append(prImg.GetRelativePath())

    def _layout_images(self):
        model = self.model[0]
        self.CreateAddButton()
        if model.images:
            self.gSizer.Clear(delete_windows=True)
            frame = wx.GetTopLevelParent(self)
            for path in model.images:
                self.AddCell(frame.bundle.path, path)
        else:
            self.EnableAddButton()

    def OnAddIlluImg(self, event):
        self.AddIlluImg()
        newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
        self.GetEventHandler().ProcessEvent(newEvt)

    def OnDelIlluImg(self, event):
        evtObj = event.GetEventObject()
        if isinstance(evtObj, ImagePreviewPanel):
            self.DelIlluImg(evtObj)
            newEvt = FormDataChangeEvent(ftEVT_SUB_FORM_DATA_CHG, self.GetId())
            self.GetEventHandler().ProcessEvent(newEvt)

    def AddIlluImg(self):
        frame = wx.GetTopLevelParent(self)
        self.AddCell(frame.bundle.path)
        if self.addBtn.IsShown():
            self.DisableAddButton()
        else:
            self.scrollWin.Layout()
            self.Layout()

    def AddCell(self, bundle_dir, rel_path=None):
        prImg = ImagePreviewPanel(
            self.illuSizer.GetStaticBox(),
            usage='illu',
            width=280,
            height=210,
            withAddDel=True
        )
        self.prImgs.append(prImg)
        if rel_path:
            prImg.LoadWithRelPath(bundle_dir, rel_path)
        else:
            prImg.LoadWithPlaceHolder(bundle_dir)
        self.Bind(EVT_PREVIEW_CELL_ADD, self.OnAddIlluImg)
        self.Bind(EVT_PREVIEW_CELL_DEL, self.OnDelIlluImg)
        self.gSizer.Add(prImg, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

    def DelIlluImg(self, prImg):
        count = self.prImgs.count(prImg)
        if count == 1:
            self.prImgs.remove(prImg)
            self.gSizer.Detach(prImg)
            prImg.Show(False)
            self.scrollWin.Layout()
            self.Layout()
        if not self.prImgs:
            self.EnableAddButton()

    def CreateAddButton(self):
        img = catalog['addimg'].GetImage()
        img = img.Size((100, 100), (18, 18))
        bmp = img.ConvertToBitmap()
        self.addBtn = wx.BitmapButton(self.illuSizer.GetStaticBox(), bitmap=bmp)
        self.addBtn.Show(False)
        self.Bind(wx.EVT_BUTTON, self.OnAddIlluImg, self.addBtn)

    def EnableAddButton(self):
        self.gSizer.Add(self.addBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        self.addBtn.Show(True)
        self.scrollWin.Layout()
        self.Layout()

    def DisableAddButton(self):
        self.gSizer.Detach(self.addBtn)
        self.addBtn.Show(False)
        self.scrollWin.Layout()
        self.Layout()
