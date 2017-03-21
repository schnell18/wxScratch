# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview


class CurriculumPanel(wx.Panel):
    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent, name=model.name_for_ui())
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

        self.previewVideoText = wx.TextCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        bifSizer.Add(self.previewVideoText, 0, wx.ALL|wx.EXPAND, 5)
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
        self.SetModel(model)
        self.Layout()

    def SetModel(self, model):
        self.model = model
        self.refNoText.SetValue(model.ref_no)
        self.titleText.SetValue(model.title)
        self.descriptionText.SetValue(model.description)
        self.cornerTypeChoice.SetSelection(model.corner_label_type)
        self.previewVideoText.SetValue(model.preview_video)
        self.coverText.SetValue(model.cover)
        self.iconText.SetValue(model.icon)

        # load lessons
        if model.curriculum_lessons:
            for seq, l in enumerate(model.curriculum_lessons, 1):
                row = [seq, l.lesson_ref, l.lesson_title, l.is_break]
                self.dvLessons.AppendItem(row)

        # load related curriculum
        if model.next_curricula:
            for curr in model.next_curricula:
                row = [curr.ref_no, curr.title, curr.cover]
                self.dvRelated.AppendItem(row)


class LessonPanel(wx.Panel):
    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent, name=model.name_for_ui())
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

        self.scrollWin.SetSizer(scrollSzier)
        self.scrollWin.Layout()
        scrollSzier.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetModel(model)
        self.SetSizer(panelSizer)

    def SetModel(self, model):
        self.model = model
        self.refNoText.SetValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.titleText.SetValue(model.title)
        self.descriptionText.SetValue(model.description)
        self.encourageText.SetValue(model.encouragement)
        self.nextDayIntroText.SetValue(model.next_day_intro)
        self.bgmMusicText.SetValue(model.bg_music)


class LessonExercisePanel(wx.Panel):
    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent, name=model.name_for_ui())
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
                u"动作编排"
            ),
            wx.VERTICAL
        )

        bifSizer = wx.FlexGridSizer(5, 3, 0, 0)
        bifSizer.AddGrowableCol(1)
        bifSizer.AddGrowableRow(3)
        bifSizer.SetFlexibleDirection(wx.BOTH)
        bifSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.refNoLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"动作编码",
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

        self.repetitionLabel = wx.StaticText(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            u"重复",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        self.repetitionLabel.Wrap(-1)
        bifSizer.Add(self.repetitionLabel, 0, wx.ALL, 5)

        self.repetitionSpin = wx.SpinCtrl(
            biSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
            max=100
        )
        bifSizer.Add(self.repetitionSpin, 0, wx.ALL|wx.EXPAND, 5)
        bifSizer.AddSpacer((100, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        biSizer.Add(bifSizer, 1, wx.EXPAND | wx.ALL, 5)
        scrollSzier.Add(biSizer, 0, wx.EXPAND | wx.ALL, 5)

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
        self.beginVoices.AppendTextColumn(u"音频")
        bvSizer.Add(self.beginVoices, 1, wx.ALL|wx.EXPAND, 5)
        scrollSzier.Add(bvSizer, 1, wx.EXPAND | wx.ALL, 5)

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
        self.midVoices.AppendTextColumn(u"位置")
        self.midVoices.AppendTextColumn(u"音频")
        mdSizer.Add(self.midVoices, 1, wx.ALL|wx.EXPAND, 5)

        scrollSzier.Add(mdSizer, 1, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSzier)
        self.scrollWin.Layout()
        scrollSzier.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetModel(model)
        self.SetSizer(panelSizer)

    def SetModel(self, model):
        self.model = model
        self.refNoText.SetValue(model.exercise_ref)
        self.measureChoice.SetSelection(model.measure - 1)
        self.repetitionSpin.SetValue(model.repetition)

        # load begin voices
        for bv in sorted(model.begin_voices, key=lambda e : e.position):
            row = [bv.audio_name]
            self.beginVoices.AppendItem(row)

        # load mid voices
        for bv in model.mid_voices:
            row = [bv.position, bv.audio_name]
            self.midVoices.AppendItem(row)



class ExercisePanel(wx.Panel):
    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent, name=model.name_for_ui())
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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)

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
        scrollSizer.Add(biSizer, 0, wx.EXPAND | wx.ALL, 5)
        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.SetModel(model)
        self.Layout()

    def SetModel(self, model):
        self.model = model
        self.exerciseRefNoText.SetValue(model.ref_no)
        self.typeChoice.SetSelection(model.type - 1)
        self.nameText.SetValue(model.action)
        self.titleText.SetValue(model.title)
        self.caloriesSpin.SetValue(model.calories)
        self.durationSpin.SetValue(model.duration)
        self.thumbnailText.SetValue(model.thumbnail)
        self.videoText.SetValue(model.video_name)


class IllustrationPanel(wx.Panel):
    def __init__(self, parent, model):
        wx.Panel.__init__(self, parent, name=model.name_for_ui())
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
        bifSizer.AddSpacer((100, 0), 1, wx.EXPAND, 5)

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
        bifSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        illuSizer.Add(bifSizer, 1, wx.EXPAND, 5)
        scrollSizer.Add(illuSizer, 0, wx.EXPAND | wx.ALL, 5)

        self.scrollWin.SetSizer(scrollSizer)
        self.scrollWin.Layout()
        scrollSizer.Fit(self.scrollWin)
        panelSizer.Add(self.scrollWin, 1, wx.EXPAND)
        self.SetSizer(panelSizer)
        self.SetModel(model)
        self.Layout()

    def SetModel(self, model):
        self.model = model
        self.illuTitleText.SetValue(model.title)
        self.illuDescriptionText.SetValue(model.description)
