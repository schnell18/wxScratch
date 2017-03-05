#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import wx.xrc

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):

        def __init__( self, parent ):
                wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

                # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

                self.m_statusBar1 = self.CreateStatusBar(1, id=wx.ID_ANY)
                self.m_menubar1 = wx.MenuBar( 0 )
                self.m_menu1 = wx.Menu()
                self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
                self.m_menu1.Append( self.m_menuItem1 )

                self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Export", wx.EmptyString, wx.ITEM_NORMAL )
                self.m_menu1.Append( self.m_menuItem2 )

                self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
                self.m_menu1.Append( self.m_menuItem3 )

                self.m_menubar1.Append( self.m_menu1, u"File" )

                self.m_menu2 = wx.Menu()
                self.m_menubar1.Append( self.m_menu2, u"Help" )

                self.SetMenuBar( self.m_menubar1 )

                bSizer2 = wx.BoxSizer( wx.VERTICAL )


                self.SetSizer( bSizer2 )
                self.Layout()

                self.Centre( wx.BOTH )

        def __del__( self ):
                pass


if __name__ == '__main__':
    app = wx.App(False)
    # A Frame is a top-level window.
    frame = MyFrame2(None)
    # Show the frame.
    frame.Show(True)
    app.MainLoop()
