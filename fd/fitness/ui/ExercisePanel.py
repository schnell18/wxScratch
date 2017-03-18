# -*- coding: utf-8 -*-

import wx
import wx.aui
import wx.dataview

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

