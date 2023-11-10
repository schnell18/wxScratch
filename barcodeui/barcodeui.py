#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import qrcode
import barcode
from qrcode.constants import ERROR_CORRECT_L
from qrcode.constants import ERROR_CORRECT_M
from qrcode.constants import ERROR_CORRECT_Q
from qrcode.constants import ERROR_CORRECT_H
from barcode.writer import ImageWriter

__ec_levels__ = [
    ERROR_CORRECT_L,
    ERROR_CORRECT_M,
    ERROR_CORRECT_Q,
    ERROR_CORRECT_H
]

class BarcodePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(
            self,
            parent,
            style=wx.TAB_TRAVERSAL
        )

        self.contentLabel = wx.StaticText(self, wx.ID_ANY, u"Content")
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
            label=u"Paste content from system clipboard automatically"
        )
        self.autoPasteCheck.SetValue(True)

        self.ecLabel = wx.StaticText(self, wx.ID_ANY, u"Error Correction Levels")
        self.ecLabel.Wrap(-1)

        choices = [u"Low", u"Medium", u"Quasi", u"High"]
        self.ecRadioBox = wx.RadioBox(
            self,
            id=wx.ID_ANY,
            label="",
            choices=choices,
            style=wx.RA_SPECIFY_COLS
        )
        self.ecRadioBox.SetSelection(3)

        self.borderLabel = wx.StaticText(self, wx.ID_ANY, u"Whitespace")
        self.borderLabel.Wrap(-1)

        self.borderSpin = wx.SpinCtrl(
            self,
            id=wx.ID_ANY,
            value="3",
            style=wx.SP_ARROW_KEYS,
            min=1,
            max=10
        )

        self.blockPixelLabel = wx.StaticText(self, wx.ID_ANY, u"Pixel Squares")
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

        self.barcodeImg = wx.StaticBitmap(
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
            2,
            wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )
        mainSizer.Add(
            self.barcodeImg,
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

    def gen_barcode_bitmap_for(self, text, ecLevel=2, boxSize=3, border=4):
        code128 = barcode.get(
            "code128",
            text, 
            writer = ImageWriter()
        )
        pil = code128.render(
            writer_options=dict(module_height=8.0, text_distance=6.0)
        )
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
        if self.autoPasteCheck.IsChecked():
            success = False
            data = wx.TextDataObject()
            if wx.TheClipboard.Open():
                success = wx.TheClipboard.GetData(data)
                wx.TheClipboard.Close()
            if success:
                clipboardText = data.GetText() 
                if clipboardText != self.contentText.GetValue():
                    self.contentText.SetValue(clipboardText)
        if event:
            event.Skip()

    def _regenerate(self):
        content = self.contentText.GetValue()
        boxSize = self.blockPixelSpin.GetValue()
        border = self.borderSpin.GetValue()
        ecLevel = self.ecRadioBox.GetSelection()
        img = self.gen_qr_bitmap_for(
            content,
            ecLevel=ecLevel,
            boxSize=boxSize,
            border=border
        )
        self.qrcodeImg.SetBitmap(img)

        # protect the python-barcode library from error like
        # IndexError: list index out of range
        if len(content) > 2:
            img = self.gen_barcode_bitmap_for(
                content,
                ecLevel=ecLevel,
                boxSize=boxSize,
                border=border
            )
            self.barcodeImg.SetBitmap(img)

        self.Layout()


class MyFrame(wx.Frame):
    def __init__(self, parent, size=(800, 600)):
        wx.Frame.__init__(self, parent, title=u"Barcode Generator", size=size)
        self.panel = BarcodePanel(self)

    def OnFocused(self, event):
        self.panel.OnFocused(event)

    def __del__(self):
        pass


if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None)
    app.Bind(wx.EVT_ACTIVATE_APP, frame.OnFocused)
    frame.Show()
    frame.OnFocused(None)
    app.MainLoop()
