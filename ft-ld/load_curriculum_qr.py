#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import ConfigParser
import sys

from os.path import expanduser
from fitness.app import FitnessResourceManager
from fitness.ftp import FtpClient
from fitness.repo import CompositeRepo
from fitness.tfs import TFSClient
from fitness.version import version_text
from time import time
from qrcodegen import QrCode


def generate_qr_code(curriculum):
    text = 'pajk://consult_fitnessmainpage_jump?content={"curriculumId":"%s","index":"1"}' % (curriculum.id,)
    qr0 = QrCode.encode_text(text, QrCode.Ecc.MEDIUM)
    svg = '%s.svg' % (curriculum.ref_no,)
    with open(svg, 'w') as f:
        f.write(qr0.to_svg_str(4))
    return svg


if __name__ == '__main__':
    t0 = time()
    print("Fitness curriculum loader (%s)" % (version_text,))
    bundle_dir = sys.argv[1]
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
    mgr = FitnessResourceManager(mgr_cfg, repo, ftp, tfs)
    t = mgr.process_curriculum_bundle(bundle_dir)
    print("Start generate QR code...")
    for c in t[0].values():
        svg = generate_qr_code(c)
        print("Generated QR code file %s" % (svg,))
    t1 = time()
    print("Elapse: %d seconds" % int(t1 - t0))
