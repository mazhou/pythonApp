# -*- coding: utf-8 -*-

import os
import sys

import logging
from PyQt5 import (QtCore)
from PyQt5.QtCore import QEvent, QTimer,QUrl, QLibraryInfo
from Utils import Constants
from Utils.Common import  Setting
from Utils.Application import QSingleApplication
from PyQt5.QtGui import QIcon
from ui.MainWindowUI import Ui_FormMainWindow
from Widgets.FramelessWindow import FramelessWindow
from Widgets.MainWindowBase import MainWindowBase
from models.Weather import Weather
from models.MarqueeLabel import MarqueeLabel
from tetris.tetris import Board
from PyQt5.QtWebEngineWidgets import *
import requests

log = logging.getLogger(__name__)


class MainWindow(FramelessWindow, MainWindowBase, Ui_FormMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Setting.init(self)
        self._initLanguage()
        self._initUi()
        # 加载窗口大小并恢复
        geometry = Setting.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)

        # 200毫秒后显示登录对话框
        # QTimer.singleShot(200, self._initCatalog)

        self.buttonMaximum.setVisible(False)
        self.buttonNormal.setVisible(False)
        self.buttonSkin.setVisible(False)
        self.buttonIssues.setVisible(False)
        self.snake.setVisible(False)
        self.tetris.setVisible(False)
        self.loadBeijing()
        self._init_marquee()
        self._tetris()

        self.browser = QWebEngineView(self.web)
        self._initweb()
        self._loadbasemsg()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.signal_timeout)  # 开启定时任务
        self.timer.start(1000*10)


    def signal_timeout(self):
        print('signal_timeout')
        try:
            self._loadbasemsg()
            self._initweb()
            self.loadweather()
        except Exception:
            pass
    # self.timer.stop()

    def _loadbasemsg(self):
        # http://123.56.243.117:
        try:
            self.basemsgld = requests.get('http://127.0.0.1:9090/static/basic.html')
            self.basemsgld.encoding = 'utf-8'
            self.basicmsg.setText(self.basemsgld.text)
        except Exception:
            pass


    def _initweb(self):
        try:
            url = 'http://127.0.0.1:9090/static/resume.html'
            self.browser.load(QUrl(url))
        except ValueError:
            pass



    def _tetris(self):
        self.tboard = Board(self.frame)
        self.tboard.resize(180, 380)
        self.tboard.start()
        self.tboard.pause()
        self.tboard.show()


    def _init_marquee(self):
        # 最下边滚动文字 demo 数据以后可以从服务器获取
        self.marqueeLabel = MarqueeLabel(self.tips_wg)
        self.marqueeLabel.setFixedWidth(600)
        self.weather = Weather()
        # self.marqueeLabel.setText(self.weather.get_messages())
        # self.marqueeLabel.setStyleSheet("""padding-top: 10px;""")

    def loadweather(self):
        self.weather.load();
        self.marqueeLabel.setText(self.weather.get_messages())

    def loadBeijing(self):
        # TODO
        # print('weather.get_messages(',weather.get_messages())
        self.basicmsg.setText('')
        self.basicmsg.setStyleSheet("""
                font-size: 20px;
                """)

    def changeEvent(self, event):
        # 窗口改变事件
        FramelessWindow.changeEvent(self, event)
        if event.type() == QEvent.WindowStateChange:  # 窗口状态改变
            state = self.windowState()
            # if state == (state | Qt.WindowMaximized):
            #     # 最大化状态,显示还原按钮
            #     self.buttonMaximum.setVisible(False)
            #     self.buttonNormal.setVisible(True)
            # else:
            #     # 隐藏还原按钮
            #     self.buttonMaximum.setVisible(True)
            #     self.buttonNormal.setVisible(False)


def main():

    if int(QtCore.PYQT_VERSION_STR.split('.')[1]) > 5:
        # for > Qt 5.5
        os.putenv('QT_AUTO_SCREEN_SCALE_FACTOR', '1')
    else:
        # for Qt 5.5
        os.putenv('QT_DEVICE_PIXEL_RATIO', 'auto')
    if os.name == 'nt':
        os.environ['PATH'] = QLibraryInfo.location(
            QLibraryInfo.BinariesPath) + os.pathsep + os.environ['PATH']

    os.makedirs(Constants.DirErrors, exist_ok=True)
    # os.makedirs(Constants.DirProject, exist_ok=True)
    # os.makedirs(os.path.dirname(Constants.UpgradeFile), exist_ok=True)
    # 异常捕捉
    # sys.excepthook = cgitb.Hook(1, Constants.DirErrors, 5, sys.stderr, '')
    # 初始化日志
    # initLog(Constants.LogName, Constants.LogFile)
    # 运行app
    app = QSingleApplication('mzstudio', sys.argv)
    if app.isRunning():
        # 激活窗口
        app.sendMessage('show', 1000)
    else:
        app.setQuitOnLastWindowClosed(True)
        app.setWindowIcon(QIcon('Resources/Images/app.ico'))
        # 第一次运行
        w = MainWindow()
        app.setActivationWindow(w)
        w.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    os.chdir('../')
    main()
