#!/usr/bin/env python

"""
This script generates images.py to make it easy to build frozen binary
"""
import os
from wx.tools import img2py

cmd_lines = [
    '   -F -n add          -c images/add.png fitness/images.py',
    '-a -F -n addimg       -c images/addimg.png fitness/images.py',
    '-a -F -n addimg2      -c images/addimg2.png fitness/images.py',
    '-a -F -n bundle       -c images/bundle.png fitness/images.py',
    '-a -F -n close        -c images/close.png fitness/images.py',
    '-a -F -n curriculum   -c images/curriculum.png fitness/images.py',
    '-a -F -n delimg2      -c images/delimg2.png fitness/images.py',
    '-a -F -n exercise     -c images/exercise.png fitness/images.py',
    '-a -F -n illustration -c images/illustration.png fitness/images.py',
    '-a -F -n lesson       -c images/lesson.png fitness/images.py',
    '-a -F -n new          -c images/new.png fitness/images.py',
    '-a -F -n open         -c images/open.png fitness/images.py',
    '-a -F -n remove       -c images/remove.png fitness/images.py',
    '-a -F -n save         -c images/save.png fitness/images.py',
    '-a -F -n segment      -c images/segment.png fitness/images.py',
    '-a -F -n upload       -c images/upload.png fitness/images.py'
]

if __name__ == '__main__':
    for line in cmd_lines:
        args = line.split()
        img2py.main(args)
