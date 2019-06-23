# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSlot, QLocale, QTranslator, QCoreApplication
from PyQt5.QtWidgets import QApplication

from Utils.Common import Setting, AppLog
from Utils.ThemeManager import ThemeManager
from Widgets.ToolTip import ToolTip
import pyqtgraph as pg
import numpy as np


class MainWindowBase:

    def _initUi(self):
        """初始UI"""
        self.setupUi(self)

        # 隐藏还原按钮
        self.buttonNormal.setVisible(False)
        # 加载鼠标样式
        ThemeManager.loadCursor(self.widgetMain)
        ThemeManager.setPointerCursors([
            self.buttonHead,  # 主界面头像
            self.buttonGithub,  # Github按钮
            self.buttonQQ,  # QQ按钮
            self.buttonGroup,  # 群按钮
            self.buttonBackToUp,  # 返回顶部按钮
            self.buttonHome  # 显示主页readme
        ])
        # 安装事件过滤器用于还原鼠标样式
        self.widgetMain.installEventFilter(self)
        # 绑定返回顶部提示框
        ToolTip.bind(self.buttonBackToUp)
        ToolTip.bind(self.buttonHome)
        # 头像提示控件
        ToolTip.bind(self.buttonHead)
        # 加载主题
        colourful = Setting.value('colourful')
        picture = Setting.value('picture', 'Resources/Images/Wallpaper/t014d05b7c3e1708b2d.jpg', str)
        AppLog.debug('colourful: %s', str(colourful))
        AppLog.debug('picture: %s', picture)
        if picture:
            ThemeManager.loadFont()
            ThemeManager.loadPictureTheme(picture)

        self._initMyMplCanvas()


    def _initMyMplCanvas(self):
        pg.setConfigOption('background', '#f0f0f090')  # 设置背景为灰色
        pg.setConfigOption('foreground', 'd')  # 设置前景（包括坐标轴，线条，文本等等）为黑色。
        pg.setConfigOptions(antialias=True)
        print("canvas")

    def _initSignals(self):
        """初始化信号槽"""
        print("initsigals")



    def _initCatalog(self):
        # 更新目录
        self._showNotice(QCoreApplication.translate(
            'MainWindow', 'Update Example Started'))
        # CloneThread.start()

    def _showNotice(self, message, timeout=2000):
        """底部显示提示
        :param message:        提示消息
        """
        if hasattr(self, '_tip'):
            self._tip._hideTimer.stop()
            self._tip.close()
            self._tip.deleteLater()
            del self._tip
        self._tip = ToolTip()
        self._tip.setText(message)
        self._tip.show()
        self._tip.move(
            self.pos().x() + int((self.width() - self._tip.width()) / 2),
            self.pos().y() + self.height() - 60,
        )
        self._tip._hideTimer.timeout.connect(self._tip.close)
        self._tip._hideTimer.start(timeout)


    def _initLanguage(self):
        """加载国际化翻译
        """
        if QLocale.system().language() in (QLocale.China, QLocale.Chinese, QLocale.Taiwan, QLocale.HongKong):
            # 加载中文
            translator = QTranslator(self)
            translator.load('Resources/pyqtclient_zh_CN.qm')
            QApplication.instance().installTranslator(translator)
            AppLog.info('install local language')

    @pyqtSlot()
    def on_buttonClose_clicked(self):
        """关闭
        """
        self.close()

    @pyqtSlot()
    def on_buttonMinimum_clicked(self):
        """最小化
        """
        self.showMinimized()

    @pyqtSlot()
    def on_buttonMaximum_clicked(self):
        """最大化
        """
        self.showMaximized()

    @pyqtSlot()
    def on_buttonNormal_clicked(self):
        """还原
        """
        self.showNormal()

    # @pyqtSlot()
    # def on_buttonBackToUp_clicked(self):
    #     """点击返回按钮
    #     """
    #     self._runJs('backToUp();')

    @pyqtSlot()
    def on_buttonGithub_clicked(self):
        """点击项目按钮
        """
        self.web.show()
        self.tetris.hide()
        self.snake.hide()
        # webbrowser.open_new_tab(Constants.UrlProject)

    @pyqtSlot()
    def on_buttonQQ_clicked(self):
        """点击QQ按钮
        """
        self.web.hide()
        self.tetris.show()
        self.snake.hide()
        # webbrowser.open(Constants.UrlQQ)

    @pyqtSlot()
    def on_buttonGroup_clicked(self):
        """点击群按钮
        """
        self.web.hide()
        self.tetris.hide()
        self.snake.show()
        # self.mpl.start_dynamic_plot()
        # webbrowser.open(Constants.UrlGroup)
        self.pyqtgraph1.clear()
        '''第一种绘图方式'''
        # self.pyqtgraph1.addPlot(title="绘图单条线", y=np.random.normal(size=100), pen=pg.mkPen(color='b', width=2))
        '''第二种绘图方式'''
        plt2 = self.pyqtgraph1.addPlot(title='绘制多条线')
        plt2.plot(np.random.normal(size=150), pen=pg.mkPen(color='r', width=2),
                  name="Red curve")  # pg.mkPen的使用方法，设置线条颜色为红色，宽度为2。
        plt2.plot(np.random.normal(size=110) + 5, pen=(0, 255, 0), name="Green curve")
        plt2.plot(np.random.normal(size=120) + 10, pen=(0, 0, 255), name="Blue curve")

        try:
            self.first_plot_flag # 检测是否进行过第一次绘图。
        except:

            plt = self.pyqtgraph2.addPlot(title='绘制条状图')
            x = np.arange(10)
            y1 = np.sin(x)
            y2 = 1.1 * np.sin(x + 1)
            y3 = 1.2 * np.sin(x + 2)

            bg1 = pg.BarGraphItem(x=x, height=y1, width=0.3, brush='r')
            bg2 = pg.BarGraphItem(x=x + 0.33, height=y2, width=0.3, brush='g')
            bg3 = pg.BarGraphItem(x=x + 0.66, height=y3, width=0.3, brush='b')

            plt.addItem(bg1)
            plt.addItem(bg2)
            plt.addItem(bg3)

            self.pyqtgraph2.nextRow()

            p4 = self.pyqtgraph2.addPlot(title="参数图+显示网格")
            x = np.cos(np.linspace(0, 2 * np.pi, 1000))
            y = np.sin(np.linspace(0, 4 * np.pi, 1000))
            p4.plot(x, y, pen=pg.mkPen(color='d', width=2))
            p4.showGrid(x=True, y=True) # 显示网格

            self.first_plot_flag = True # 第一次绘图后进行标记


    @pyqtSlot()
    def on_buttonBackToUp_clicked(self):
        """点击返回按钮
        """
        # self._runJs('backToUp();')

    @pyqtSlot()
    def on_buttonHome_clicked(self):
        """主页readme
        """
        # self.renderReadme()