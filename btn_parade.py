#!/usr/bin/env python

import wx
import re
import wx.lib.buttons as buttons

def make_btn(id, parent):
    bmp = wx.ArtProvider.GetBitmap(getattr(wx, id), wx.ART_OTHER, (16, 16))
    btn = buttons.GenBitmapToggleButton(parent, -1, bmp)
    print("icon %s ok" % id)
    return btn

class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(400, 300))
        panel = wx.Panel(self)

        grid_sizer = wx.GridSizer(cols=8, vgap=2, hgap=2)
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

        panel.SetSizer(grid_sizer)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, 'Button parade')
    frame.Show()
    app.MainLoop()
