from Utils.Constants import (Color, P_Black, InfoOutline)
import requests

class Weather(object):
    _p_list = []
    _cityCode = '101010100' #'北京'
    _recordNum = 20
    _rep = None

    def __init__(self):
        self.load()

        # self.add_message(msg1, Color.Black)
        # self.add_message(msg2, Color.Black)
        # self.add_message(msg3, Color.Black)
        # self.add_message(msg4, Color.Black)
        # self.add_message(msg5, Color.Black)


    def load(self):
        try:
            self._rep = requests.get('http://www.weather.com.cn/data/sk/' + self._cityCode + '.html')
            self._rep.encoding = 'utf-8'
        except ValueError:
            pass

    def add_newLine(self ):
        self._p_list.append('<br>')
        if len(self._p_list) > self.recordNum:
            self._p_list.pop(0)

    def add_message(self, msg, color):
        if color == Color.Black:
            self._p_list.append(P_Black % msg)

        if len(self._p_list) > self.recordNum:
            self._p_list.pop(0)

    def get_messages(self):
        try:
            msg1 = '%s' % self._rep.json()['weatherinfo']['city']
            msg2 = '    风向: %s' % self._rep.json()['weatherinfo']['WD']
            msg3 = '    温度: %s' % self._rep.json()['weatherinfo']['temp'] + ' 度'
            msg4 = '    风力: %s' % self._rep.json()['weatherinfo']['WS']
            msg5 = '    湿度: %s' % self._rep.json()['weatherinfo']['SD']
            return msg1+msg2+msg3+msg4+msg5
        except ValueError:
            pass
        return ''