# -*- coding: utf-8 -*-

import wx
import ConfigParser
import qrcode
from threading import Thread
from wx.lib.pubsub import pub
from os.path import expanduser
from fitness.loader import Loader
from fitness.ftp import FtpClient
from fitness.repo import CompositeRepo
from fitness.tfs import TFSClient

# constant definitions
EVENT_NUM_CONVERTED      = 20
EVENT_EXCEPTION_OCCURRED = 30
EVENT_COMPLETED          = 40

class ImpThread(Thread):
    def __init__(self, bundle, launcher):
        Thread.__init__(self)
        self.bundle = bundle
        self.launcher = launcher

    def run(self):
        try:
            config = ConfigParser.RawConfigParser()
            config.read(expanduser('~/.fitness/config.ini'))
            ftp_cfg = {t[0]: t[1] for t in config.items('ftp.resource')}
            db_cfg = {t[0]: t[1] for t in config.items('mysql')}
            db_cfg['raise_on_warnings'] = True
            tfs_cfg = {t[0]: t[1] for t in config.items('tfs')}
            mgr_cfg = {t[0]: t[1] for t in config.items('general')}

            repo = CompositeRepo(db_cfg)
            ftp = FtpClient(ftp_cfg)
            tfs = TFSClient(tfs_cfg)
            loader = Loader(mgr_cfg, repo, ftp, tfs)
            loader.load(self.bundle, self)
        except (IOError, IndexError) as e:
            wx.CallAfter(
                pub.sendMessage,
                'updateProgress',
                msg=(EVENT_EXCEPTION_OCCURRED, self.launcher, e)
            )
            return

    def update_progress(self, msg, pct):
        if pct == 100:
            wx.CallAfter(
                pub.sendMessage,
                'updateProgress',
                msg=(EVENT_COMPLETED, self.launcher, pct)
            )
        else:
            wx.CallAfter(
                pub.sendMessage,
                'updateProgress',
                msg=(EVENT_NUM_CONVERTED, self.launcher, pct)
            )


class ImpDialog(wx.Dialog):

    def __init__(self, parent, bundle):
        wx.Dialog.__init__ (
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            size=wx.Size(450, 300),
            style=wx.DEFAULT_DIALOG_STYLE
        )
        self.bundle = bundle
        self.createUI()
        self.Layout()
        self.Centre(wx.BOTH)
        # launcher import process
        thread = ImpThread(bundle, self)
        thread.start()
        self.progressBar.SetRange(100)
        self.progressBar.SetValue(8)
        pub.subscribe(self.onUpdateProgress, 'updateProgress')

    def onUpdateProgress(self, msg):
        launcher = msg[1]
        if not self == launcher:
            return
        msg_type, data = msg[0], msg[2]
        if msg_type == EVENT_NUM_CONVERTED:
            self.progressBar.SetValue(int(data))
        elif msg_type == EVENT_COMPLETED:
            # display qrcode image for curricula
            for i, curri in enumerate(self.bundle.curricula):
                self.qrImages[i].SetBitmap(self.gen_qr_bitmap_for(curri))
        elif msg_type == EVENT_EXCEPTION_OCCURRED:
            e = data
            self.progressBar.SetRange(100)
            self.progressBar.SetValue(0)
            self.filePicker.Enable(True)
            if isinstance(e, IOError):
                wx.MessageBox(
                    u'导入出现异常: ' + str(e),
                    u'异常',
                    wx.OK | wx.ICON_WARNING
                )

    def createUI(self):
        bundle = self.bundle
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        progressSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.progressBar = wx.Gauge(
            self,
            wx.ID_ANY,
            100,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.GA_HORIZONTAL
        )
        self.progressBar.SetValue(0)
        progressSizer.Add(
            self.progressBar,
            3,
            wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )

        self.cancelBtn = wx.Button(
            self,
            wx.ID_ANY,
            u"Canel",
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        progressSizer.Add(
            self.cancelBtn,
            0,
            wx.ALIGN_CENTER_VERTICAL|wx.ALL,
            5
        )

        mainSizer.Add(progressSizer, 1, wx.EXPAND, 5)
        curriculumNum = len(bundle.curricula)
        rows = curriculumNum / 4
        if not curriculumNum % 4 == 0:
           rows = rows + 1
        qrSizer = wx.GridSizer(rows, 4, vgap=0, hgap=10)

        self.qrImages = []
        bmp = wx.Image('qrholder.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        for curri in bundle.curricula:
            imgSizer = wx.BoxSizer(wx.VERTICAL)
            img = wx.StaticBitmap(
                self,
                wx.ID_ANY,
                bmp,
                wx.DefaultPosition,
                wx.DefaultSize,
                0
            )
            imgLbl = wx.StaticText(
                self,
                wx.ID_ANY,
                curri.title,
                wx.DefaultPosition,
                wx.DefaultSize,
                0
            )
            imgSizer.Add(
                img,
                4,
                wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                2
            )
            imgSizer.Add(
                imgLbl,
                1,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                2
            )
            qrSizer.Add(
                imgSizer,
                0,
                wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_VERTICAL|wx.ALL,
                2
            )
            self.qrImages.append(img)

        mainSizer.Add(qrSizer, 2, wx.EXPAND, 5)
        self.SetSizer(mainSizer)

    def __del__(self):
        pass

    def gen_qr_bitmap_for(self, curriculum):
        text = 'pajk://consult_fitnessmainpage_jump?content={"curriculumId":"%s","index":"1"}' % (curriculum.id,)
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        x = qr.make_image()

        qr_file = "c%s.png" % curriculum.id
        with open(qr_file, 'wb') as fh:
            x.save(img_file, 'PNG')

        return wx.Bitmap(qr_file, wx.BITMAP_TYPE_PNG)
