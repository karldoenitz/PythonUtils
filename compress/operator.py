# -*- coding: utf-8 -*-
"""

operator
~~~~~~~~

introduction
use this module to compress folder to *.tar.gz.

Usage
=====
>>> from compress import CompressOperator
>>> compress_operator = CompressOperator("/home/karl/PycharmProjects/PythonUtils", "/home/karl/桌面/result.tar.gz")
>>> compress_operator.compress(without=["/."])
>>> compress_operator.package_pyc(without=["/."])

"""
import os
import py_compile
import tarfile


class CompressOperator(object):
    def __init__(self, folder_dir, compressed_file_name):
        self.folder_dir = folder_dir
        self.compress_dir = compressed_file_name

    def __get_file_name(self):
        for root, dirs, files in os.walk(self.folder_dir):
            for file_name in files:
                yield os.path.join(root, file_name)

    @classmethod
    def __is_without(cls, without, file_name):
        """whether without

        :param without: list type, without files
        :param file_name: file's name
        :return: boolean

        """
        for w in without:
            if w in file_name:
                return True
        return False

    def compress(self, without):
        """compress to file

        :param without: list type, without files
        :return: None

        """
        with tarfile.open(self.compress_dir, "w:gz") as tar:
            for file_name in self.__get_file_name():
                if self.__is_without(without, file_name):
                    continue
                tar.add(file_name, arcname=file_name.replace(self.folder_dir, ""))

    def package_pyc(self, without):
        """compile py to pyc and compress file

        :param without: list type, without files
        :return: None

        """
        with tarfile.open(self.compress_dir, "w:gz") as tar:
            file_list = [file_name for file_name in self.__get_file_name()]
            for file_name in file_list:
                if self.__is_without(without, file_name):
                    continue
                if file_name.endswith(".py"):
                    pyc_name = file_name + "c"
                    py_compile.compile(
                        file=file_name,
                        cfile=pyc_name
                    )
                    tar.add(pyc_name, arcname=pyc_name.replace(self.folder_dir, ""))
                else:
                    tar.add(file_name, arcname=file_name.replace(self.folder_dir, ""))


if __name__ == '__main__':
    c = CompressOperator("/home/karl/PycharmProjects/PythonUtils", "/home/karl/桌面/result.tar.gz")
    # c.compress(without=["/."])
    c.package_pyc(without=["/."])
