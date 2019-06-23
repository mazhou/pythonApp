#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from PyQt5.QtCore import QSettings, QTextCodec, QObject, pyqtSignal
from Utils.Constants import (LogFormatterDebug, LogFormatter, LogName,ConfigFile)

AppLog = logging.getLogger(LogName)


def initLog(name, file=None, level=logging.DEBUG, formatter=None):
    """初始化日志记录配置
    """

    formatter = formatter or logging.Formatter(
        LogFormatterDebug if level == logging.DEBUG else LogFormatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if file != None:
        file = os.path.abspath(str(file))
        file_handler = logging.FileHandler(file, mode='w', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

class Setting:
    _Setting = None

    @classmethod
    def init(cls, parent=None):
        """初始化配置实例
        :param cls:
        :param parent:
        """
        if not cls._Setting:
            cls._Setting = QSettings(ConfigFile, QSettings.IniFormat, parent)
            cls._Setting.setIniCodec(QTextCodec.codecForName('utf-8'))

    @classmethod
    def value(cls, key, default=None, typ=None):
        """获取配置中的值
        :param cls:
        :param key:        键名
        :param default:    默认值
        :param typ:        类型
        """
        cls.init()
        if default != None and typ != None:
            return cls._Setting.value(key, default, typ)
        if default != None:
            return cls._Setting.value(key, default)
        return cls._Setting.value(key)

    @classmethod
    def setValue(cls, key, value):
        """更新配置中的值
        :param cls:
        :param key:        键名
        :param value:      键值
        """
        cls.init()
        cls._Setting.setValue(key, value)
        cls._Setting.sync()