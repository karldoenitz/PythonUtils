# -*- coding: utf-8 -*-
import os
import tarfile


class CompressOperator(object):
    def __init__(self, folder_dir, compressed_file_name):
        self.folder_dir = folder_dir
        self.compress_dir = compressed_file_name

    def __get_file_name(self):
        for root, dirs, files in os.walk(self.folder_dir):
            for file_name in files:
                yield os.path.join(root, file_name)

    def compress(self):
        with tarfile.open(self.compress_dir, "w:gz") as tar:
            for file_name in self.__get_file_name():
                if "/." in file_name:
                    continue
                tar.add(file_name, arcname=file_name.replace(self.folder_dir, ""))


if __name__ == '__main__':
    c = CompressOperator("/home/karl/PycharmProjects/PythonUtils", "/home/karl/桌面/result.tar.gz")
    c.compress()
