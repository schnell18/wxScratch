#!/usr/bin/env python
import wx
import os

import wx
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        grid_sizer = wx.GridBagSizer(hgap=5, vgap=5)
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.quote = wx.StaticText(self, label="Your quote :")

        self.logger = wx.TextCtrl(
            self,
            size=(600, 300),
            style=wx.TE_MULTILINE | wx.TE_READONLY
        )

        # A button
        self.button =wx.Button(self, label="Save")

        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Your name :")
        self.editname = wx.TextCtrl(
            self,
            value="Enter here your name",
            size=(140,-1)
        )

        # the combobox Control
        self.sampleList = [
            'friends',
            'advertising',
            'web search',
            'Yellow Pages'
        ]
        self.lblhear = wx.StaticText(
            self,
            label="How did you hear from us ?"
        )
        self.edithear = wx.ComboBox(
            self,
            size=(95, -1),
            choices=self.sampleList,
            style=wx.CB_DROPDOWN
        )


        # Checkbox
        self.insure = wx.CheckBox(
            self,
            label="Do you want Insured Shipment ?"
        )

        # Radio Boxes
        radioList = [
            'blue'  , 'red'    , 'yellow'    , 'orange' ,
            'green' , 'purple' , 'navy blue' , 'black'  ,
            'gray'
        ]
        rb = wx.RadioBox(
            self,
            label="What color would you like ?",
            choices=radioList,
            majorDimension=3,
            style=wx.RA_SPECIFY_COLS
        )

        # layout elements
        grid_sizer.Add(self.quote, pos=(0, 0))
        grid_sizer.Add(self.lblname, pos=(1, 0))
        grid_sizer.Add(self.editname, pos=(1, 1))
        grid_sizer.Add(self.lblhear, pos=(3, 0))
        grid_sizer.Add(self.edithear, pos=(3, 1))
        grid_sizer.Add(20, 80, pos=(2, 0))
        grid_sizer.Add(self.insure, pos=(4, 0), span=(1, 2), flag=wx.BOTTOM, border=5)
        grid_sizer.Add(rb, pos=(5, 0), span=(1, 2))

        # wire event handlers
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.button)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtText, self.edithear)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)

        h_sizer.Add(grid_sizer, 0, wx.ALL, 5)
        h_sizer.Add(self.logger, 2, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(h_sizer, 0, wx.ALL, 5)

        main_sizer.Add(self.button, 0,  wx.CENTER)
        self.SetSizerAndFit(main_sizer)


    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())

    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())

    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())

    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())

    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()

    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.IsChecked())

if __name__ == '__main__':
    app = wx.App(False)
    frame = wx.Frame(None, size=(600, 400))
    panel = ExamplePanel(frame)
    frame.Show()
    app.MainLoop()
