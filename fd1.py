#!/usr/bin/env python
# -*- coding: utf-8 -*-


import wx
import wx.lib.agw.aui
import wx.dataview

from wx.lib.agw.aui import AuiNotebook
from wx.lib.agw.aui import AUI_NB_DEFAULT_STYLE

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 668,494 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        # self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.m_statusBar1 = self.CreateStatusBar( 1, id= wx.ID_ANY )
        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem1 )

        self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"Export", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem2 )

        self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem3 )

        self.m_menubar1.Append( self.m_menu1, u"File" )

        self.m_menu2 = wx.Menu()
        self.m_menubar1.Append( self.m_menu2, u"Help" )

        self.SetMenuBar( self.m_menubar1 )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow1.SetScrollRate( 5, 5 )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_treeCtrl1 = wx.TreeCtrl( self.m_scrolledWindow1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        bSizer3.Add( self.m_treeCtrl1, 3, wx.EXPAND|wx.RIGHT, 5 )


        self.m_scrolledWindow1.SetSizer( bSizer3 )
        self.m_scrolledWindow1.Layout()
        bSizer3.Fit( self.m_scrolledWindow1 )
        bSizer1.Add( self.m_scrolledWindow1, 1, wx.EXPAND |wx.ALL, 0 )

        self.m_auinotebook2 = AuiNotebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, AUI_NB_DEFAULT_STYLE )
        self.m_scrolledWindow2 = wx.ScrolledWindow( self.m_auinotebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow2.SetScrollRate( 5, 5 )
        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow2, wx.ID_ANY, u"基本信息" ), wx.VERTICAL )

        fgSizer1 = wx.FlexGridSizer( 7, 2, 0, 0 )
        fgSizer1.AddGrowableCol( 1 )
        fgSizer1.AddGrowableRow( 2 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"识别编号", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )

        self.m_textCtrl1 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText3 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"标题", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.m_textCtrl2 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl2, 1, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText4 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"描述", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        fgSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )

        self.m_textCtrl4 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE )
        fgSizer1.Add( self.m_textCtrl4, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText5 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"角标类型", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        fgSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

        m_choice1Choices = []
        self.m_choice1 = wx.Choice( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        fgSizer1.Add( self.m_choice1, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText7 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"预览视频", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        fgSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.m_textCtrl5 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl5, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText9 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"封面", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        fgSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )

        self.m_textCtrl6 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl6, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_staticText10 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"图标", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        fgSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )

        self.m_textCtrl7 = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        fgSizer1.Add( self.m_textCtrl7, 0, wx.ALL|wx.EXPAND, 5 )


        sbSizer1.Add( fgSizer1, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( sbSizer1, 3, wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow2, wx.ID_ANY, u"子课编排" ), wx.VERTICAL )

        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_dataViewListCtrl3 = wx.dataview.DataViewListCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_dataViewListColumn2 = self.m_dataViewListCtrl3.AppendTextColumn( u"序号" )
        self.m_dataViewListColumn3 = self.m_dataViewListCtrl3.AppendTextColumn( u"子课编码" )
        self.m_dataViewListColumn4 = self.m_dataViewListCtrl3.AppendTextColumn( u"子课标题" )
        self.m_dataViewListColumn5 = self.m_dataViewListCtrl3.AppendToggleColumn( u"休息" )
        bSizer5.Add( self.m_dataViewListCtrl3, 1, wx.ALL|wx.EXPAND, 5 )


        sbSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )


        bSizer4.Add( sbSizer2, 2, wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_scrolledWindow2, wx.ID_ANY, u"相关课程" ), wx.VERTICAL )

        self.m_dataViewListCtrl4 = wx.dataview.DataViewListCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_dataViewListColumn6 = self.m_dataViewListCtrl4.AppendTextColumn( u"课程编号" )
        self.m_dataViewListColumn7 = self.m_dataViewListCtrl4.AppendTextColumn( u"标题" )
        self.m_dataViewListColumn8 = self.m_dataViewListCtrl4.AppendTextColumn( u"封面" )
        sbSizer3.Add( self.m_dataViewListCtrl4, 0, wx.ALL|wx.EXPAND, 5 )


        bSizer4.Add( sbSizer3, 1, wx.EXPAND, 5 )


        self.m_scrolledWindow2.SetSizer( bSizer4 )
        self.m_scrolledWindow2.Layout()
        bSizer4.Fit( self.m_scrolledWindow2 )
        self.m_auinotebook2.AddPage( self.m_scrolledWindow2, u"a page", False, wx.NullBitmap )
        self.m_scrolledWindow3 = wx.ScrolledWindow( self.m_auinotebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.m_scrolledWindow3.SetScrollRate( 5, 5 )
        self.m_auinotebook2.AddPage( self.m_scrolledWindow3, u"a page", False, wx.NullBitmap )

        bSizer1.Add( self.m_auinotebook2, 3, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( bSizer1 )
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
