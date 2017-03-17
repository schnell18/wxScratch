# coding=utf-8
import hashlib


def md5sum(filename, blocksize=65536):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            md5.update(block)
    return md5.hexdigest()
