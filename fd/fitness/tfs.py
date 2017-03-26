# coding=utf-8
import requests
from time import sleep

class TFSClient:

    def __init__(self, cfg):
        self.config = cfg

    def upload(self, path):
        r = requests.post(url=self.config['base_url'], data=open(path, 'rb'))
        return r.json()['TFS_FILE_NAME']


class MockTFSClient:

    def __init__(self, cfg):
        self.config = cfg

    def upload(self, path):
        sleep(0.1)
        return 'Txafsdfff'
