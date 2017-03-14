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
        self.model = None
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
        self.Layout()

    def SetModel(self, model):
        self.model = model
        self.refNoText.SetValue(model.ref_no)
        self.titleText.SetValue(model.title)
        self.descriptionText.SetValue(model.description)
        self.cornerTypeChoice.SetValue(model.corner_label)
        self.previewVideoText.SetValue(model.preview_video)
        self.coverText.SetValue(model.cover)
        self.iconText.SetValue(model.icon)

        # load lessons
        for seq, lesson in enumerate(model.curriculum_lesson):
            row = [seq, lesson.ref_no, lesson.title, lesson.rest]
            self.dvLessons.AppendItem(row)

        # load related curriculum
        for curr in model.next_curriculum:
            row = [curr.ref_no, curr.title, curr.cover]
            self.dvRelated.AppendItem(row)

