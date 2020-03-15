#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import qrcode
from qrcode.constants import ERROR_CORRECT_L
from qrcode.constants import ERROR_CORRECT_M
from qrcode.constants import ERROR_CORRECT_Q
from qrcode.constants import ERROR_CORRECT_H

__ec_levels__ = [
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H
]

class QRCodePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            style=wx.TAB_TRAVERSAL
        )

        self.contentLabel = wx.StaticText(self, wx.ID_ANY, u"内容")
        self.contentLabel.Wrap(-1)
        self.contentText = wx.TextCtrl(
            self,
            id=wx.ID_ANY,
            size=(-1, 80),
            style=wx.TE_MULTILINE
        )

        self.autoPasteCheck = wx.CheckBox(
            self,
            id=wx.ID_ANY,
            label=u"Auto Paste from clipboard"
        )
        self.autoPasteCheck.SetValue(True)

        self.ecLabel = wx.StaticText(self, wx.ID_ANY, u"容错级别")
        self.ecLabel.Wrap(-1)

        choices = [u"低", u"中", u"准高", u"高"]
        self.ecRadioBox = wx.RadioBox(
            self,
            id=wx.ID_ANY,
            label="",
            choices=choices,
            style=wx.RA_SPECIFY_COLS
        )
        self.ecRadioBox.SetSelection(3)

        self.borderLabel = wx.StaticText(self, wx.ID_ANY, u"留白")
        self.borderLabel.Wrap(-1)

        self.borderSpin = wx.SpinCtrl(
            self,
            id=wx.ID_ANY,
            value="3",
            style=wx.SP_ARROW_KEYS,
            min=1,
            max=10
        )

        self.blockPixelLabel = wx.StaticText(self, wx.ID_ANY, u"方块像素")
        self.blockPixelLabel.Wrap(-1)

        self.blockPixelSpin = wx.SpinCtrl(
            self,
            id=wx.ID_ANY,
            value="4",
            style=wx.SP_ARROW_KEYS,
            min=1,
            max=10
        )

        self.qrcodeImg = wx.StaticBitmap(
            self,
            id=wx.ID_ANY
        )

        fgSizer = wx.FlexGridSizer(0, 4, 4, 4)
        fgSizer.AddGrowableCol(2)
        fgSizer.SetFlexibleDirection(wx.BOTH)
        fgSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        fgSizer.Add(10, 10)
        fgSizer.Add(10, 10)
        fgSizer.Add(10, 10)
        fgSizer.Add(10, 10)
        fgSizer.Add(10, 0)
        fgSizer.Add(self.contentLabel, 0, wx.ALL, 0)
        fgSizer.Add(self.contentText, 0, wx.ALL|wx.EXPAND, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(self.autoPasteCheck, 0, wx.ALL|wx.EXPAND, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(self.ecLabel, 0, wx.ALL, 0)
        fgSizer.Add(self.ecRadioBox, 1, wx.ALIGN_LEFT, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(self.borderLabel, 0, wx.ALL, 0)
        fgSizer.Add(self.borderSpin, 0, wx.ALL|wx.EXPAND, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(10, 0)
        fgSizer.Add(self.blockPixelLabel, 0, wx.ALL, 0)
        fgSizer.Add(self.blockPixelSpin, 0, wx.ALL|wx.EXPAND, 0)
        fgSizer.Add(10, 0)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(fgSizer, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(
            self.qrcodeImg,
            1,
            wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )

        self.SetSizer(mainSizer)
        self.Layout()

        # Connect Events
        self.contentText.Bind(wx.EVT_TEXT, self.OnTextChanged)
        self.Bind(wx.EVT_SPINCTRL, self.OnNumberChanged)
        self.Bind(wx.EVT_RADIOBOX, self.OnEcLevelChanged)
        self.Bind(wx.EVT_CHILD_FOCUS, self.OnFocused)

    def gen_qr_bitmap_for(self, text, ecLevel=2, boxSize=3, border=4):
        qr = qrcode.QRCode(
            version=1,
            error_correction=__ec_levels__[ecLevel],
            box_size=boxSize,
            border=border
        )
        qr.add_data(text)
        qr.make(fit=True)
        x = qr.make_image()
        pil = x.get_image()
        img = wx.Image(pil.width, pil.height)
        img.SetData(pil.convert('RGB').tobytes())
        return img.ConvertToBitmap()

    def __del__(self):
        pass

    def OnTextChanged(self, event):
        self._regenerate()

    def OnNumberChanged(self, event):
        self._regenerate()

    def OnEcLevelChanged(self, event):
        self._regenerate()

    def OnFocused(self, event):
        success = False
        data = wx.TextDataObject()
        if self.autoPasteCheck.IsChecked() and wx.TheClipboard.Open():
            success = wx.TheClipboard.GetData(data)
            wx.TheClipboard.Close()
        if success:
            self.contentText.SetValue(data.GetText())
        event.Skip()

    def _regenerate(self):
        boxSize = self.blockPixelSpin.GetValue()
        border = self.borderSpin.GetValue()
        ecLevel = self.ecRadioBox.GetSelection()
        img = self.gen_qr_bitmap_for(
            self.contentText.GetValue(),
            ecLevel=ecLevel,
            boxSize=boxSize,
            border=border
        )
        self.qrcodeImg.SetBitmap(img)
        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, parent, size=(450, 500)):
        wx.Frame.__init__(self, parent, title=u'二维码生成器', size=size)
        panel = QRCodePanel(self)

    def __del__(self):
        pass


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
