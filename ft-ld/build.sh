#!/usr/bin/env bash

zip ft_load.zip           \
    fitness/__init__.py   \
    fitness/app.py        \
    fitness/ftp.py        \
    fitness/model.py      \
    fitness/repo.py       \
    fitness/tfs.py        \
    fitness/util.py       \
    load_common_res.py    \
    load_curriculum.py    \
    load_curriculum_qr.py \
    config.ini.sample     \
    requirements.txt      \
    README.md

mkdir -p /tmp/fitness
GIT_REV=$(git rev-parse --short HEAD)
OLD_DIR=$(pwd)
sed -e "s/%TOKEN%/$GIT_REV/" fitness/version.py > /tmp/fitness/version.py
cd /tmp
zip -u $OLD_DIR/ft_load.zip fitness/version.py
cd $OLD_DIR
