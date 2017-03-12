# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview


class CurriculumPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.Size(-1, 40),
            wx.TE_MULTILINE
        )
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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

        self.previewVideoLabel = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.previewVideoLabel, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)

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

        scrollSizer.Add(biSizer, 3, wx.ALL|wx.EXPAND, 5)

        lessonsSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"子课编排"
            ),
            wx.VERTICAL
        )

        self.dvLessons = wx.dataview.DataViewListCtrl(
            lessonsSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvLessonsSeqNo = self.dvLessons.AppendTextColumn(u"序号")
        self.dvLessonsRefNo = self.dvLessons.AppendTextColumn(u"子课编码")
        self.dvLessonsTitle = self.dvLessons.AppendTextColumn(u"子课标题")
        self.dvLessonsRest = self.dvLessons.AppendToggleColumn(u"休息")
        lessonsSizer.Add( self.dvLessons, 1, wx.ALL|wx.EXPAND, 5)

        scrollSizer.Add(lessonsSizer, 2, wx.ALL|wx.EXPAND, 5)

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

        scrollSizer.Add(relatedSizer, 1, wx.EXPAND|wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.Layout()


class LessonPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.scrollWin = wx.ScrolledWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.HSCROLL|wx.VSCROLL
        )
        self.scrollWin.SetScrollRate(5, 5)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        scrollSzier = wx.BoxSizer(wx.VERTICAL)

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
        bifSizer.AddGrowableRow(3)
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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
            wx.Size(-1, 60),
            wx.TE_MULTILINE
        )
        bifSizer.Add(self.descriptionText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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

        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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

        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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

        scrollSzier.Add(biSizer, 1, wx.EXPAND | wx.ALL, 5)

        exercisesSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作编排"
            ),
            wx.VERTICAL
        )

        self.excerises = wx.dataview.DataViewListCtrl(
            exercisesSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvColSeqNo = self.excerises.AppendTextColumn(u"序号")
        self.dvColAction = self.excerises.AppendTextColumn(u"动作")
        self.dvColRepetition = self.excerises.AppendTextColumn(u"重复")
        self.dvColMeasure = self.excerises.AppendTextColumn(u"单位")
        exercisesSizer.Add(self.excerises, 0, wx.ALL|wx.EXPAND, 5)

        scrollSzier.Add(exercisesSizer, 0, wx.EXPAND | wx.ALL, 5)

        bvSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"准备音"
            ),
            wx.VERTICAL
        )

        self.beginVoices = wx.dataview.DataViewListCtrl(
            bvSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvColAudio = self.beginVoices.AppendTextColumn(u"音频")
        self.dvColPosition = self.beginVoices.AppendTextColumn(u"位置")
        bvSizer.Add(self.beginVoices, 0, wx.ALL|wx.EXPAND, 5)
        scrollSzier.Add(bvSizer, 0, wx.EXPAND | wx.ALL, 5)

        mdSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作音"
            ),
            wx.VERTICAL
        )

        self.midVoices = wx.dataview.DataViewListCtrl(
            mdSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvColAudio2 = self.midVoices.AppendTextColumn(u"音频")
        self.dvColPosition2 = self.midVoices.AppendTextColumn(u"位置")
        mdSizer.Add(self.midVoices, 0, wx.ALL|wx.EXPAND, 5)

        scrollSzier.Add(mdSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSzier)
        self.scrollWin.Layout()
        scrollSzier.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)

class ExercisePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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

        self.caloriesText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.caloriesText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer(( 0, 0), 1, wx.EXPAND, 5)

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

        self.durationText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.durationText, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        self.thumbnail = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"预览图",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.thumbnail.Wrap(-1)
        bifSizer.Add(self.thumbnail, 0, wx.ALL, 5)

        self.thumbnailText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.thumbnailText, 0, wx.ALL|wx.EXPAND, 5)

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
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.videoText, 0, wx.ALL|wx.EXPAND, 5)

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

        scrollSizer.Add(biSizer, 1, wx.EXPAND | wx.ALL, 5)

        illuSizer = wx.StaticBoxSizer(
            wx.StaticBox(
                self.scrollWin,
                wx.ID_ANY,
                u"动作详解"
            ),
            wx.VERTICAL
        )

        self.dvIlluCtrl = wx.dataview.DataViewListCtrl(
            illuSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.dvIlluCtrlTitle = self.dvIlluCtrl.AppendTextColumn(u"标题")
        self.dvIlluCtrlDescription = self.dvIlluCtrl.AppendTextColumn(u"描述")
        self.dvIlluCtrlPic = self.dvIlluCtrl.AppendTextColumn(u"图片")
        illuSizer.Add(self.dvIlluCtrl, 0, wx.ALL|wx.EXPAND, 5)

        scrollSizer.Add(illuSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.Layout()

