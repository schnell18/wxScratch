# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview


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

