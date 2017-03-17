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
    t1 = time()
    print("Elapse: %d seconds" % int(t1 - t0))
