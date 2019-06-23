#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

LogName = 'matthewLog'
LogFile = 'Resources/Data/app.log'

LogFormatter = '[%(asctime)s %(name)s] %(levelname)-8s %(message)s'
ConfigFile = 'Resources/Data/Config.ini'
LogFormatterDebug = '[%(asctime)s %(name)s %(module)s:%(funcName)s:%(lineno)s] %(levelname)-8s %(message)s'
DirErrors = 'Resources/Data/Errors'  # 错误日志目录


InfoOutline = '''<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">
<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">
p, li {  margin-top: 0px;  white-space: pre-wrap; line-height:1;}
</style>
</head>
<body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:200; font-style:normal;line-height:1;\">
%s
</body>
</html>
'''

P_Black = """<p  style=\"color:#000000; margin-top:0px; margin-left:0px;margin-bottom:0px; -qt-block-indent:0; text-indent:0px;\">
<font size=0px>
%s
</font>
</p>
"""


class Color(Enum):
    Black = 1
    # RED = 2
    # BLUE = 3