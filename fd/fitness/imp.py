# -*- coding: utf-8 -*-

import wx
import configparser
import qrcode
import os.path
from threading         import Thread
from wx.lib.pubsub     import pub
from os.path           import expanduser
from fitness.loader    import Loader
from fitness.ftp       import FtpClient
from fitness.repo      import CompositeRepo
from fitness.tfs       import TFSClient
from fitness.exception import UserAbortError

# constant definitions
EVENT_TOTAL_CALCULATED   = 10
EVENT_NUM_CONVERTED      = 20
EVENT_EXCEPTION_OCCURRED = 30
EVENT_COMPLETED          = 40

SCORE_FTP_AUDIO          = 2
SCORE_FTP_VIDEO          = 3
SCORE_TFS_IMAGE          = 2
SCORE_DB_OPER            = 1

class ImpThread(Thread):
    def __init__(self, bundle, launcher):
        Thread.__init__(self)
        self.bundle = bundle
        self.launcher = launcher
        self._aborted = False

    def get_topic(self):
        # to prevent message duplication on second (or greater) run
        return 'imp_progress_topic-%d' % self.ident

    def abort(self):
        self._aborted = True

    def run(self):
        try:
            parser = configparser.ConfigParser()
            parser.read(expanduser('~/.fitness/config.ini'))
            ftp_cfg = {t[0]: t[1] for t in parser.items('ftp.resource')}
            db_cfg = {t[0]: t[1] for t in parser.items('mysql')}
            db_cfg['raise_on_warnings'] = True
            tfs_cfg = {t[0]: t[1] for t in parser.items('tfs')}
            mgr_cfg = {t[0]: t[1] for t in parser.items('general')}

            repo = CompositeRepo(db_cfg)
            ftp = FtpClient(ftp_cfg)
            tfs = TFSClient(tfs_cfg)
            loader = Loader(mgr_cfg, repo, ftp, tfs)
            self.ticks = 0
            estimated_ticks = self.calc_ticks(self.bundle)
            wx.CallAfter(
                pub.sendMessage,
                self.get_topic(),
                msg=(
                    EVENT_TOTAL_CALCULATED,
                    self.launcher,
                    estimated_ticks,
                    u'开始导入'
                )
            )
            loader.load(self.bundle, self)
            # make sure the progress is completed
            wx.CallAfter(
                pub.sendMessage,
                self.get_topic(),
                msg=(
                    EVENT_COMPLETED,
                    self.launcher,
                    estimated_ticks,
                    u'导入完成'
                )
            )
        except (Exception) as e:
            wx.CallAfter(
                pub.sendMessage,
                self.get_topic(),
                msg=(EVENT_EXCEPTION_OCCURRED, self.launcher, e, '')
            )

    def update_progress(self, txt, delta):
        if self._aborted:
            raise UserAbortError
        self.ticks += delta
        wx.CallAfter(
            pub.sendMessage,
            self.get_topic(),
            msg=(EVENT_NUM_CONVERTED, self.launcher, self.ticks, txt)
        )

    def calc_ticks(self, bundle):
        ticks = 0

        # calculate TFS scores
        for curriculum in bundle.curricula:
            ticks += SCORE_TFS_IMAGE * 2
        for exercise in bundle.exercises:
            if exercise.thumbnail:
                ticks += SCORE_TFS_IMAGE
            if exercise.illustrations:
                for i in exercise.illustrations:
                    if i.images:
                        for img in i.images:
                            ticks += SCORE_TFS_IMAGE

        # calculate FTP scores
        for lesson in bundle.lessons:
            if lesson.bg_music:
                ticks += SCORE_FTP_AUDIO
            lesson_exercises = lesson.lesson_exercises
            if lesson_exercises:
                for le in lesson_exercises:
                    begin_voices = le.begin_voices
                    if begin_voices:
                        for bv in begin_voices:
                            ticks += SCORE_FTP_AUDIO
                    mid_voices = le.mid_voices
                    if mid_voices:
                        for bv in mid_voices:
                            ticks += SCORE_FTP_AUDIO
        for exercise in bundle.exercises:
            if exercise.type != 1:
                continue
            ticks += SCORE_FTP_VIDEO

        # calcualte scores for DB persistence operations
        for exercise in bundle.exercises:
            ticks += SCORE_DB_OPER

        # save or update all lessons
        for lesson in bundle.lessons:
            ticks += SCORE_DB_OPER

        # save or update all curricula
        for curriculum in bundle.curricula:
            ticks += SCORE_DB_OPER * 2

        return ticks


class ImpDialog(wx.Dialog):

    def __init__(self, parent, bundle):
        wx.Dialog.__init__ (
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            size=wx.Size(580, 300),
            style=wx.DEFAULT_DIALOG_STYLE
        )
        self.bundle = bundle
        self.createUI()
        self.Layout()
        self.Centre(wx.BOTH)
        # launcher import process
        self.thread = ImpThread(bundle, self)
        self.thread.start()
        # self.progressBar.SetRange(100)
        # self.progressBar.SetValue(8)
        pub.subscribe(self.OnUpdateProgress, self.thread.get_topic())

    def OnUpdateProgress(self, msg):
        launcher = msg[1]
        if not self == launcher:
            return
        msg_type, data, txt = msg[0], msg[2], msg[3]
        if msg_type == EVENT_TOTAL_CALCULATED:
            self.statLbl.SetLabel(txt)
            self.progressBar.SetRange(int(data))
        elif msg_type == EVENT_NUM_CONVERTED:
            self.statLbl.SetLabel(txt)
            self.progressBar.SetValue(int(data))
        elif msg_type == EVENT_COMPLETED:
            self.statLbl.SetLabel(txt)
            self.cancelBtn.SetLabel(u"关闭")
            self.progressBar.SetValue(int(data))
            # display qrcode image for curricula
            for i, curri in enumerate(self.bundle.curricula):
                bmp = self.gen_qr_bitmap_for(curri)
                self.qrImages[i].SetBitmap(bmp)
        elif msg_type == EVENT_EXCEPTION_OCCURRED:
            e = data
            if not isinstance(e, UserAbortError):
                wx.MessageBox(
                    u'导入出现异常: ' + str(e),
                    u'异常',
                    wx.OK | wx.ICON_WARNING
                )
            else:
                self.Close(True)

    def createUI(self):
        bundle = self.bundle
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # status text
        self.statLbl = wx.StaticText(
            self,
            wx.ID_ANY,
            '',
            wx.DefaultPosition,
            wx.DefaultSize,
            0
        )
        mainSizer.Add(self.statLbl, 0, wx.EXPAND|wx.TOP|wx.LEFT, 30)

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
            u"取消",
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
        self.Bind(wx.EVT_BUTTON, self.OnCancelClicked, self.cancelBtn)

        mainSizer.Add(progressSizer, 1, wx.EXPAND, 5)
        curriculumNum = len(bundle.curricula)
        rows = curriculumNum / 4
        if not curriculumNum % 4 == 0:
           rows = rows + 1
        qrSizer = wx.GridSizer(rows, 4, vgap=5, hgap=10)

        self.qrImages = []
        for curri in bundle.curricula:
            placeholder = self._load(os.path.join(bundle.path, curri.icon))
            imgSizer = wx.BoxSizer(wx.VERTICAL)
            img = wx.StaticBitmap(
                self,
                wx.ID_ANY,
                placeholder,
                wx.DefaultPosition,
                wx.DefaultSize,
                0
            )
            imgLbl = wx.StaticText(
                self,
                id=wx.ID_ANY,
                label=curri.title,
                style=wx.ALIGN_CENTRE_HORIZONTAL
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

    def OnCancelClicked(self, event):
        if self.thread and self.thread.isAlive():
            self.thread.abort()
        else:
            self.Close(True)

    def __del__(self):
        pass

    def gen_qr_bitmap_for(self, curriculum):
        text = 'pajk://consult_fitnessmainpage_jump?content={"curriculumId":"%s","index":"1"}' % (curriculum.id if curriculum.id else 0,)
        qr = qrcode.QRCode(version=1, box_size=3, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        x = qr.make_image()
        pil = x.get_image()
        img = wx.Image(pil.width, pil.height)
        img.SetData(pil.convert('RGB').tobytes())
        return img.ConvertToBitmap()

    def _load(self, path):
        # scale to fit
        return self._scale_to_fit(wx.Bitmap(path))

    def _scale_to_fit(self, bmp):
        boundw, boundh = 135, 135
        img = bmp.ConvertToImage()
        img.Rescale(boundw, boundh)
        bmp = wx.Bitmap(img)
        return bmp

