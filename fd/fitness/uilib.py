# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview
import wx.media
import os.path
import re
import platform


ftEVT_FORM_DATA_CHG = wx.NewEventType()
EVT_FORM_DATA_CHG = wx.PyEventBinder(ftEVT_FORM_DATA_CHG, 1)


class FormDataChangeEvent(wx.CommandEvent):
    def __init__(self, evtType, id):
        wx.CommandEvent.__init__(self, evtType, id)


class BasePanel(wx.Panel):
    def __init__(self, parent, model, **kwargs):
        wx.Panel.__init__(self, parent, **kwargs)
        self.dirty=False
        self.model=model

        # bind all change events
        self.Bind(wx.EVT_TEXT, self.OnFormDataChanged)
        self.Bind(wx.EVT_CHOICE, self.OnFormDataChanged)
        self.Bind(wx.EVT_SPINCTRL, self.OnFormDataChanged)

    def SetDirty(self, dirty):
        self.dirty=dirty
        # fire EVT_FORM_DATA_CHG
        if dirty:
            evt = FormDataChangeEvent(ftEVT_FORM_DATA_CHG, self.GetId())
            self.GetEventHandler().ProcessEvent(evt)

    def IsDirty(self):
        return self.dirty

    def SaveModel(self):
        # to be override in subclass
        pass

    def OnFormDataChanged(self, evt):
        parent = self.GetParent()
        if isinstance(parent, wx.aui.AuiNotebook):
            pageIndex = parent.GetPageIndex(self)
            if not pageIndex == wx.NOT_FOUND:
                text = parent.GetPageText(pageIndex)
                if not text.startswith('*'):
                    parent.SetPageText(pageIndex, '*' + text)
        self.SetDirty(True)
        evt.Skip()


class ImagePreviewPanel(wx.Panel):
    def __init__(self, parent, width=300, height=200):
        wx.Panel.__init__(self, parent)

        self.width = width
        self.height = height
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        # image preview area
        placeholder = wx.Image(width, height)
        placeholder.Replace(0, 0, 0, 255, 255, 255)
        self.imgCtrl = wx.StaticBitmap(
            self,
            wx.ID_ANY,
            placeholder.ConvertToBitmap()
        )

        mainSizer.Add(self.imgCtrl, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.captionLbl = wx.StaticText(self, wx.ID_ANY, "")
        self.captionLbl.Wrap(-1)
        mainSizer.Add(self.captionLbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizerAndFit(mainSizer)

    def Load(self, path):
        if os.path.exists(path):
            bmp = wx.Bitmap(path)
            (width, height) = (bmp.GetWidth(), bmp.GetHeight())
            # scale to fit
            self.imgCtrl.SetBitmap(self._scale_to_fit(bmp))
            txt = u"宽高 %d X %d" % (width, height)
            self.captionLbl.SetLabel(txt)

    def _scale_to_fit(self, bmp):
        (width, height) = (bmp.GetWidth(), bmp.GetHeight())
        factor = max(width / self.width, height / self.height)
        if factor > 1:
            img = bmp.ConvertToImage()
            img.Rescale(self.width / factor, self.height / factor)
            bmp = wx.Bitmap(img)
        return bmp

    def __del__(self):
        pass


class AvPreviewPanel(wx.Panel):
    def __init__(self, parent, width=300, height=200):
        wx.Panel.__init__(self, parent)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        extra_args = {
            'size'  : (width, height),
            'style' : wx.SIMPLE_BORDER
        }
        if platform.system() == 'Windows':
            extra_args['szBackend'] = wx.media.MEDIABACKEND_WMP10
        self.mediaCtrl = wx.media.MediaCtrl(
            self,
            wx.ID_ANY,
            **extra_args
        )
        self.mediaCtrl.SetPlaybackRate(1)
        self.mediaCtrl.SetVolume(1)
        self.Bind(wx.media.EVT_MEDIA_LOADED, self.OnMediaLoaded)
        mainSizer.Add(self.mediaCtrl, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.captionLbl = wx.StaticText(self, wx.ID_ANY, "")
        self.captionLbl.Wrap(-1)
        mainSizer.Add(self.captionLbl, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizerAndFit(mainSizer)

    def Load(self, path):
        if os.path.exists(path):
            self.mediaCtrl.Load(path)

    def OnMediaLoaded(self, evt):
        self.mediaCtrl.Pause()
        txt = self._formatDuration(self.mediaCtrl.Length())
        self.captionLbl.SetLabel(txt)
        self.mediaCtrl.ShowPlayerControls(wx.media.MEDIACTRLPLAYERCONTROLS_DEFAULT)

    def _formatDuration(self, milli_seconds):
        seconds = milli_seconds / 1000 % 60
        mins = milli_seconds / 1000 / 60 % 60
        hours = milli_seconds / 1000 / 3600 % 60
        return u"时长 %02d:%02d:%02d" % (hours, mins, seconds)

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

        self.colPos = self.dvAudio.AppendTextColumn(
            label=u"位置",
            width=50
        )
        self.colAudio = self.dvAudio.AppendTextColumn(
            label=u"音频",
            width=200
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

        self.addBtn.Enable(False)
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

    def OnSelected(self, evt):
        self.addBtn.Enable(True)
        self.delBtn.Enable(True)
        self.upBtn.Enable(True)
        self.downBtn.Enable(True)


    def AddRow(self, row):
        self.dvAudio.AppendItem(row)


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

        self.colRefNo = self.dvLesson.AppendTextColumn(
            label=u"编码",
            width=150
        )
        self.colTitle = self.dvLesson.AppendTextColumn(
            label=u"标题",
            width=200
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

        self.addBtn.Enable(False)
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

    def OnSelected(self, evt):
        self.addBtn.Enable(True)
        self.delBtn.Enable(True)
        self.upBtn.Enable(True)
        self.downBtn.Enable(True)


    def AddRow(self, row):
        self.dvLesson.AppendItem(row)


class CurriculumPanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=model.name_for_ui())
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

        bifSizer = wx.FlexGridSizer(7, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.AddGrowableRow(2)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"课程编号",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.refNoLabel.Wrap(-1)
        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)

        self.refNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.titleText, 1, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.decriptionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.decriptionLabel.Wrap(-1)
        bifSizer.Add(self.decriptionLabel, 0, wx.ALL, 5)

        self.descriptionText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            size=(-1, 40),
            style=wx.TE_MULTILINE
        )
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.cornerTypeLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"角标类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.cornerTypeLabel.Wrap(-1)
        bifSizer.Add(self.cornerTypeLabel, 0, wx.ALL, 5)

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
        bifSizer.Add(self.cornerTypeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.previewVideoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"预览视频",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.previewVideoLabel.Wrap(-1)
        bifSizer.Add(self.previewVideoLabel, 0, wx.ALL, 5)

        self.previewVideoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.previewVideoText, 0, wx.ALL|wx.EXPAND, 5)
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
        bifSizer.Add(self.mediaCtrl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.coverLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"封面",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.coverLabel.Wrap(-1)
        bifSizer.Add(self.coverLabel, 0, wx.ALL, 5)

        self.coverText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.coverText, 0, wx.ALL|wx.EXPAND, 5)

        self.coverBtn = wx.Button(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"浏览",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.coverBtn, 0, wx.ALL, 5)

        self.iconLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"图标",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.iconLabel.Wrap(-1)
        bifSizer.Add(self.iconLabel, 0, wx.ALL, 5)

        self.iconText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.iconText, 0, wx.ALL|wx.EXPAND, 5)

        self.iconBtn = wx.Button(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"浏览",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.iconBtn, 0, wx.ALL, 5)
        biSizer.Add(bifSizer, 1, wx.ALL|wx.EXPAND, 5)


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
        model = self.model
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
        self.coverText.ChangeValue(
            model.cover if model.cover else ''
        )
        self.iconText.ChangeValue(
            model.icon if model.icon else ''
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

    def SaveModel(self):
        model = self.model
        model.ref_no = self.refNoText.GetValue()
        model.title = self.titleText.GetValue()
        model.description = self.descriptionText.GetValue()
        model.corner_label_type = self.cornerTypeChoice.GetSelection()
        model.preview_video = self.previewVideoText.GetValue()
        model.cover = self.coverText.GetValue()
        model.icon = self.iconText.GetValue()
        # TODO: assembly curriculum lessons
        # TODO: assembly next curriculua

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
        BasePanel.__init__(self, parent, model, name=model.name_for_ui())
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

        bifSizer = wx.FlexGridSizer(7, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        # bifSizer.AddGrowableRow(3)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"子课编码",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.refNoLabel.Wrap(-1)
        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)

        self.refNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.TextLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.TextLabel.Wrap(-1)
        bifSizer.Add(self.TextLabel, 0, wx.ALL, 5)

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
        bifSizer.Add(self.typeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.titleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.descriptionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.descriptionLabel.Wrap(-1)
        bifSizer.Add(self.descriptionLabel, 0, wx.ALL, 5)

        self.descriptionText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, 80),
            wx.TE_MULTILINE
        )
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.encourageLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"激励文案",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.encourageLabel.Wrap(-1)
        bifSizer.Add(self.encourageLabel, 0, wx.ALL, 5)

        self.encourageText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.encourageText, 0, wx.ALL|wx.EXPAND, 5)

        bifSizer.AddSpacer(1)

        self.nextDayIntroLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"结课文案",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.nextDayIntroLabel.Wrap(-1)
        bifSizer.Add(self.nextDayIntroLabel, 0, wx.ALL, 5)

        self.nextDayIntroText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.nextDayIntroText, 0, wx.ALL|wx.EXPAND, 5)

        bifSizer.AddSpacer(1)

        self.bgmMusicLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"背景音乐",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.bgmMusicLabel.Wrap(-1)
        bifSizer.Add(self.bgmMusicLabel, 0, wx.ALL, 5)

        self.bgmMusicText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.bgmMusicText, 0, wx.ALL|wx.EXPAND, 5)
        self.bgmMusicText.Bind(wx.EVT_TEXT, self.OnBgmChanged)

        self.bmgMusicBtn = wx.Button(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"浏览",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.bmgMusicBtn, 0, wx.ALL, 5)
        biSizer.Add(bifSizer, 1, wx.EXPAND, 5)

        prSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"预览"
            ),
            wx.HORIZONTAL
        )

        vSizer = wx.BoxSizer(wx.VERTICAL)
        # audio preview area
        self.prAudio = AvPreviewPanel(prSizer.GetStaticBox())
        vSizer.Add(self.prAudio, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        prSizer.Add(vSizer, 0, wx.ALL, 5)

        scrollSizer.Add(biSizer, 0, wx.EXPAND | wx.ALL, 5)
        scrollSizer.Add(prSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.LoadModel()
        self.SetSizer(panelSizer)

    def LoadModel(self):
        model = self.model
        self.refNoText.ChangeValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.titleText.ChangeValue(model.title)
        self.descriptionText.ChangeValue(model.description)
        self.encourageText.ChangeValue(model.encouragement)
        self.nextDayIntroText.ChangeValue(model.next_day_intro)
        self.bgmMusicText.ChangeValue(model.bg_music)
        self._loadAudio()

    def SaveModel(self):
        model = self.model
        model.ref_no = self.refNoText.GetValue()
        model.type = self.typeChoice.GetSelection() + 1
        model.title = self.titleText.GetValue()
        model.description = self.descriptionText.GetValue()
        model.encouragement = self.encourageText.GetValue()
        model.next_day_intro = self.nextDayIntroText.GetValue()
        model.bg_music = self.bgmMusicText.GetValue()

    def OnBgmChanged(self, evt):
        self._loadAudio()

    def _loadAudio(self):
        path = self.bgmMusicText.GetValue()
        frame = wx.GetTopLevelParent(self)
        fp = os.path.join(frame.bundle.path, *path.split('/'))
        self.prAudio.Load(fp)

    def __del__(self):
        pass


class LessonExercisePanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=model.name_for_ui())
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

        bifSizer = wx.FlexGridSizer(0, 3, hgap=4, vgap=4)
        bifSizer.AddGrowableCol(1)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"动作编码"
        )
        self.refNoLabel.Wrap(-1)
        bifSizer.Add(self.refNoLabel, 0, wx.ALL, 5)

        self.refNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY
        )
        bifSizer.Add(self.refNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.Add(100, 0)

        self.repetitionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"重复"
        )
        self.repetitionLabel.Wrap(-1)
        bifSizer.Add(self.repetitionLabel, 0, wx.ALL, 5)

        self.repetitionSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY,
            max=100
        )
        bifSizer.Add(self.repetitionSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.measureLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"单位",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.measureLabel.Wrap(-1)
        bifSizer.Add(self.measureLabel, 0, wx.ALL, 5)

        measureChoices = [u'次', u'秒']
        self.measureChoice = wx.Choice(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            measureChoices,
            0
        )
        self.measureChoice.SetSelection(0)
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
        self.SetSizer(panelSizer)

    def LoadModel(self):
        model = self.model
        self.refNoText.ChangeValue(model.exercise_ref)
        self.measureChoice.SetSelection(model.measure - 1)
        self.repetitionSpin.SetValue(model.repetition)

        # load begin voices
        for bv in sorted(model.begin_voices, key=lambda e : e.position):
            row = [str(bv.position), bv.audio_name]
            self.beginVoices.AddRow(row)

        # load mid voices
        for bv in model.mid_voices:
            row = [str(bv.position), bv.audio_name]
            self.midVoices.AddRow(row)

    def SaveModel(self):
        model = self.model
        model.exercise_ref = self.refNoText.GetValue()
        model.measure = self.measureChoice.GetSelection() + 1
        model.repetition = self.repetitionSpin.GetValue()

        # TODO: save begin voices

        # TODO: save mid voices


class ExercisePanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=model.name_for_ui())
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

        bifSizer = wx.FlexGridSizer(8, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.exerciseRefNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"动作编号",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.exerciseRefNoLabel.Wrap(-1)
        bifSizer.Add(self.exerciseRefNoLabel, 0, wx.ALL, 5)

        self.exerciseRefNoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.exerciseRefNoText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.typeLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"类型",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.typeLabel.Wrap(-1)
        bifSizer.Add(self.typeLabel, 0, wx.ALL, 5)

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
        bifSizer.Add(self.typeChoice, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.nameLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"名称",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.nameLabel.Wrap(-1)
        bifSizer.Add(self.nameLabel, 0, wx.ALL, 5)

        self.nameText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.nameText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.titleLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.titleLabel.Wrap(-1)
        bifSizer.Add(self.titleLabel, 0, wx.ALL, 5)

        self.titleText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.titleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.caloriesLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"卡路里",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.caloriesLabel.Wrap(-1)
        bifSizer.Add(self.caloriesLabel, 0, wx.ALL, 5)

        self.caloriesSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
            max=100000
        )
        bifSizer.Add(self.caloriesSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.durationLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"时长",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.durationLabel.Wrap(-1)
        bifSizer.Add(self.durationLabel, 0, wx.ALL, 5)

        self.durationSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
            max=100000
        )
        bifSizer.Add(self.durationSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)

        self.thumbnailLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"预览图",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.thumbnailLabel.Wrap(-1)
        bifSizer.Add(self.thumbnailLabel, 0, wx.ALL, 5)

        self.thumbnailText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.thumbnailText, 0, wx.ALL|wx.EXPAND, 5)
        self.thumbnailText.Bind(wx.EVT_TEXT, self.OnThumbnailChanged)

        self.thumbnailBtn = wx.Button(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"浏览",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.thumbnailBtn, 0, wx.ALL, 5)

        self.videoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"视频",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.videoLabel.Wrap(-1)
        bifSizer.Add(self.videoLabel, 0, wx.ALL, 5)

        self.videoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            id=wx.ID_ANY
        )
        bifSizer.Add(self.videoText, 0, wx.ALL|wx.EXPAND, 5)
        self.videoText.Bind(wx.EVT_TEXT, self.OnVideoChanged)

        self.videoBtn = wx.Button(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"浏览",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.videoBtn, 0, wx.ALL, 5)
        biSizer.Add(bifSizer, 1, wx.EXPAND, 5)

        prSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"预览"
            ),
            wx.HORIZONTAL
        )

        gSizer = wx.GridSizer(1, 2, hgap=4, vgap=4)
        # image preview area
        self.prImg = ImagePreviewPanel(prSizer.GetStaticBox())
        gSizer.Add(self.prImg, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        # video preview area
        self.prVideo = AvPreviewPanel(prSizer.GetStaticBox())
        gSizer.Add(self.prVideo, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

        prSizer.Add(gSizer, 0, wx.ALL, 5)

        scrollSizer.Add(biSizer, 0, wx.EXPAND | wx.ALL, 5)
        scrollSizer.Add(prSizer, 1, wx.EXPAND | wx.ALL, 5)
        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.LoadModel()
        self.Layout()

    def LoadModel(self):
        model = self.model
        self.exerciseRefNoText.ChangeValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.durationSpin.SetValue(model.duration)
        self.titleText.ChangeValue(model.title)
        if model.type == 1:
            self.nameText.ChangeValue(model.action)
            self.caloriesSpin.SetValue(model.calories)
            self.thumbnailText.ChangeValue(model.thumbnail)
            self.videoText.ChangeValue(model.video_name)
            self._loadPreview()

    def SaveModel(self):
        model = self.model
        model.ref_no = self.exerciseRefNoText.GetValue()
        model.type = self.typeChoice.GetSelection() + 1
        model.duration = self.durationSpin.GetValue()
        model.title = self.titleText.GetValue()
        if model.type == 1:
            model.action = self.nameText.GetValue()
            model.calories = self.caloriesSpin.GetValue()
            model.thumbnail = self.thumbnailText.GetValue()
            model.video_name = self.videoText.GetValue()

    def OnThumbnailChanged(self, evt):
        self._loadThumbnail()

    def OnVideoChanged(self, evt):
        self._loadVideo()

    def _loadPreview(self):
        self._loadThumbnail()
        self._loadVideo()

    def _loadThumbnail(self):
        path = self.thumbnailText.GetValue()
        frame = wx.GetTopLevelParent(self)
        fp = os.path.join(frame.bundle.path, *path.split('/'))
        self.prImg.Load(fp)

    def _loadVideo(self):
        path = self.videoText.GetValue()
        frame = wx.GetTopLevelParent(self)
        fp = os.path.join(frame.bundle.path, *path.split('/'))
        self.prVideo.Load(fp)

    def __del__(self):
        pass


class IllustrationPanel(BasePanel):
    def __init__(self, parent, model):
        BasePanel.__init__(self, parent, model, name=model.name_for_ui())
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

        illuSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作详解"
            ),
            wx.VERTICAL
        )

        bifSizer = wx.FlexGridSizer(3, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.illuTitleLabel = wx.StaticText(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            u"标题",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.illuTitleLabel.Wrap(-1)
        bifSizer.Add(self.illuTitleLabel, 0, wx.ALL, 5)

        self.illuTitleText = wx.TextCtrl(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.illuTitleText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(100)

        self.illuDescriptionLabel = wx.StaticText(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            u"描述",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.illuDescriptionLabel.Wrap(-1)
        bifSizer.Add(self.illuDescriptionLabel, 0, wx.ALL, 5)

        self.illuDescriptionText = wx.TextCtrl(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, 160),
            wx.TE_MULTILINE
        )
        bifSizer.Add(self.illuDescriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(1)
        illuSizer.Add(bifSizer, 1, wx.EXPAND, 5)

        self.prSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"详解图预览"
            ),
            wx.VERTICAL
        )

        self.gSizer = wx.GridSizer(1, 4, hgap=4, vgap=4)

        scrollSizer.Add(illuSizer, 0, wx.EXPAND | wx.ALL, 5)
        scrollSizer.Add(self.prSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.LoadModel()
        self.Layout()

    def LoadModel(self):
        model = self.model
        self.illuTitleText.ChangeValue(model.title)
        self.illuDescriptionText.ChangeValue(model.description)
        self._layout_images()

    def SaveModel(self):
        model = self.model
        model.title = self.illuTitleText.GetValue()
        model.description = self.illuDescriptionText.GetValue()
        # TODO: save images

    def _layout_images(self):
        if self.model.images:
            self.gSizer.Clear(delete_windows=True)
            frame = wx.GetTopLevelParent(self)
            for path in self.model.images:
                fp = os.path.join(frame.bundle.path, *path.split('/'))
                if os.path.exists(fp):
                    prImage = ImagePreviewPanel(
                        self.prSizer.GetStaticBox(),
                        width=500,
                        height=300
                    )
                    prImage.Load(fp)
                    self.gSizer.Add(prImage, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)


