# -*- coding: utf-8 -*-
"""

operator
~~~~~~~~

introduction
use this module to compress folder to *.tar.gz *.tar *.zip.
or compile py file to pyc file and then compress the files to *.tar.gz *.tar *.zip.

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
import zipfile


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
        """compress files

        :param without: list type, without files
        :return: None

        """
        if self.compress_dir.endswith(".tar") or self.compress_dir.endswith(".tar.gz"):
            self.compress_tar(without=without)
        elif self.compress_dir.endswith(".zip"):
            self.compress_zip(without=without)
        else:
            print u"Invalid archive extension"
            print u"无效的压缩文件后缀名"

    def compress_tar(self, without):
        """compress to tar file

        :param without: list type, without files
        :return: None

        """
        with tarfile.open(self.compress_dir, "w:gz") as tar:
            for file_name in self.__get_file_name():
                if self.__is_without(without, file_name):
                    continue
                tar.add(file_name, arcname=file_name.replace(self.folder_dir, ""))

    def compress_zip(self, without):
        """compress to zip file

        :param without: list type, without files
        :return: None

        """
        with zipfile.ZipFile(self.compress_dir, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for file_name in self.__get_file_name():
                if self.__is_without(without, file_name):
                    continue
                zip_file.write(file_name, arcname=file_name.replace(self.folder_dir, ""))

    def package_pyc(self, without):
        """compile py to pyc and compress file

        :param without: list type, without files
        :return: None

        """
        if self.compress_dir.endswith(".tar") or self.compress_dir.endswith(".tar.gz"):
            self.package_tar(without=without)
        elif self.compress_dir.endswith(".zip"):
            self.package_zip(without=without)
        else:
            print u"Invalid archive extension"
            print u"无效的压缩文件后缀名"

    def package_tar(self, without):
        """compile py to pyc and compress tar file

        :param without: list type, without files
        :return: None

        """
        with tarfile.open(self.compress_dir, "w:gz") as tar:
            added_pyc = []
            file_list = [file_name for file_name in self.__get_file_name()]
            for file_name in file_list:
                if self.__is_without(without, file_name):
                    continue
                if file_name.endswith(".py"):
                    pyc_name = file_name + "c"
                    if pyc_name in added_pyc:
                        continue
                    py_compile.compile(
                        file=file_name,
                        cfile=pyc_name
                    )
                    tar.add(pyc_name, arcname=pyc_name.replace(self.folder_dir, ""))
                    added_pyc.append(pyc_name)
                else:
                    if file_name in added_pyc:
                        continue
                    tar.add(file_name, arcname=file_name.replace(self.folder_dir, ""))
                    added_pyc.append(file_name)

    def package_zip(self, without):
        """compile py to pyc and compress zip file

        :param without: list type, without files
        :return: None

        """
        with zipfile.ZipFile(self.compress_dir, "w") as zip_file:
            added_pyc = []
            file_list = [file_name for file_name in self.__get_file_name()]
            for file_name in file_list:
                if self.__is_without(without, file_name):
                    continue
                if file_name.endswith(".py"):
                    pyc_name = file_name + "c"
                    if pyc_name in added_pyc:
                        continue
                    py_compile.compile(
                        file=file_name,
                        cfile=pyc_name
                    )
                    zip_file.write(pyc_name, arcname=pyc_name.replace(self.folder_dir, ""))
                    added_pyc.append(pyc_name)
                else:
                    if file_name in added_pyc:
                        continue
                    zip_file.write(file_name, arcname=file_name.replace(self.folder_dir, ""))
                    added_pyc.append(file_name)


if __name__ == '__main__':
    c = CompressOperator("/home/karl/PycharmProjects/PythonUtils", "/home/karl/桌面/result.tar.gz")
    c.compress(without=["/.", ".pyc"])
    # c.package_pyc(without=["/."])
