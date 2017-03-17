# coding=utf-8
import ftplib
import sys

from os.path import basename


class FtpClient:

    def __init__(self, cfg):
        self.config = cfg
        self.__ftp = None

    def upload(self, local_file, dest_dir):
        old_dir = None
        try:
            # copy local file identified by src to dest
            base_file = basename(local_file)
            target_dir = self.config['root_dir'] + '/' + dest_dir
            old_dir = self.__ftp.pwd()
            self._chdir(target_dir)
            self.__ftp.storbinary('STOR ' + base_file, open(local_file, 'rb'), 1024)
        except Exception as x:
            sys.stderr.write("Fail to upload due to: " + str(x))
            raise
        finally:
            if old_dir:
                self.__ftp.cwd(old_dir)

    def connect(self):
        if not self.__ftp:
            self.__ftp = ftplib.FTP()
            self.__ftp.connect(
                self.config['host'],
                self.config['port']
            )
            self.__ftp.login(
                self.config['user'],
                self.config['password']
            )
        return self.__ftp

    def disconnect(self):
        if self.__ftp:
            self.__ftp.quit()
            self.__ftp = None

    def _chdir(self, directory):
        if directory.endswith('/'):
            directory = directory[:-1]
        self._ch_dir_rec(directory.split('/'))

    # Check if directory exists (in current location)
    def _exists(self, directory):
        filelist = []
        self.__ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == directory and f.upper().startswith('D'):
                return True
        return False

    def _ch_dir_rec(self, path_list):
        if len(path_list) == 0:
            return

        ancestor_dir = path_list.pop(0)

        if not self._exists(ancestor_dir):
            self.__ftp.mkd(ancestor_dir)
        self.__ftp.cwd(ancestor_dir)
        self._ch_dir_rec(path_list)