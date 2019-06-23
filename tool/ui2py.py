#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import os.path

# UI文件所在的路径
dir_soure = './../designer/'
dir_target = './../ui/'


# 列出目录下的所有ui文件
def listUiFile():
    list = []
    files = os.listdir(dir_soure)
    for filename in files:
        # print( dir + os.sep   )
        # print(filename)
        if os.path.splitext(filename)[1] == '.ui':
            list.append(filename)

    return list


# 把后缀为ui的文件改成后缀为py的文件名
def transPyFile(filename):
    return os.path.splitext(filename)[0] + '.py'


# 调用系统命令把ui转换成py
def runMain():
    list = listUiFile()
    for uifile in list:
        pyfile = transPyFile(uifile)
        # print(uifile,pyfile)
        cmd = 'pyuic5 -o {dir_target}{pyfile} {dir_soure}{uifile}'.format(dir_target=dir_target, dir_soure=dir_soure,
                                                                          pyfile=pyfile, uifile=uifile)
        print(cmd)
        os.system(cmd)


###### 程序的主入口
if __name__ == "__main__":
    runMain()
