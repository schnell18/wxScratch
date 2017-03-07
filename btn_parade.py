#!/usr/bin/env python

import wx
import re
import wx.lib.buttons as buttons

def make_btn(id, parent):
    bmp = wx.ArtProvider.GetBitmap(getattr(wx, id), wx.ART_OTHER, (16, 16))
    btn = buttons.GenBitmapToggleButton(parent, -1, bmp)
    print("icon %s ok" % id)
    return btn

class MyFrame(wx.MiniFrame):
    def __init__(self, parent, title):

        wx.MiniFrame.__init__(
            self,
            parent,
            wx.ID_ANY,
            title,
            style=wx.CAPTION | wx.CLOSE_BOX,
            size=(270, 280)
        )
        self.SetMinSize((270, 280))
        panel = wx.Panel(self)
        box_sizer = wx.BoxSizer(wx.HORIZONTAL)

        grid_sizer = wx.FlexGridSizer(cols=8, vgap=2, hgap=2)
        # grid_sizer = wx.GridSizer(cols=8, vgap=2, hgap=2)
        icons = [
            'ART_ADD_BOOKMARK', 'ART_CDROM',
            'ART_CLOSE',  'ART_COPY',
            'ART_CROSS_MARK', 'ART_CUT', 'ART_DELETE',
            'ART_DEL_BOOKMARK', 'ART_ERROR', 'ART_EXECUTABLE_FILE',
            'ART_FILE_OPEN', 'ART_FILE_SAVE', 'ART_FILE_SAVE_AS',
            'ART_FIND', 'ART_FIND_AND_REPLACE', 'ART_FLOPPY',
            'ART_FOLDER', 'ART_FOLDER_OPEN',
            'ART_GOTO_FIRST', 'ART_GOTO_LAST', 'ART_GO_BACK',
            'ART_GO_DIR_UP', 'ART_GO_DOWN', 'ART_GO_FORWARD',
            'ART_GO_HOME', 'ART_GO_TO_PARENT', 'ART_GO_UP',
            'ART_HARDDISK', 'ART_HELP', 'ART_HELP_BOOK',
            'ART_HELP_FOLDER', 'ART_HELP_PAGE',
            'ART_HELP_SETTINGS', 'ART_HELP_SIDE_PANEL', 'ART_INFORMATION',
            'ART_LIST_VIEW',
            'ART_MINUS', 'ART_MISSING_IMAGE',
            'ART_NEW', 'ART_NEW_DIR', 'ART_NORMAL_FILE',
            'ART_PASTE', 'ART_PLUS',
            'ART_PRINT', 'ART_QUESTION', 'ART_QUIT',
            'ART_REDO', 'ART_REMOVABLE', 'ART_REPORT_VIEW',
            'ART_TICK_MARK', 'ART_TIP',
            'ART_UNDO', 'ART_WARNING'
        ]

        for x in icons:
            grid_sizer.Add(make_btn(x, panel), 0)

        box_sizer.Add(grid_sizer, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(box_sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'Button parade')
    frame.Show()
    app.MainLoop()
