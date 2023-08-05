import cgitb

from PyQt5.QtCore import Qt, QPropertyAnimation, pyqtProperty, QPoint
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
from qtawesome import icon

cgitb.enable(format='text')

class CloseButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(CloseButton, self).__init__(ico, text, p)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(255, 69, 0, 255))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(255, 69, 0, 255))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(CloseButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''background:mediumvioletred;border: 0 solid''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(CloseButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''background:orangered;border: 0 solid''')


class OtherButton(QPushButton):
    def __init__(self, ico=None, text='', p=None):
        super(OtherButton, self).__init__(ico, text, p)

        self.setStyleSheet('''background:transparent;border: 0 solid;width:40px;height:40px''')
        self._color = QColor()

        self.ani_enter = QPropertyAnimation(self, b'color')
        self.ani_enter.setDuration(150)
        self.ani_enter.setStartValue(QColor(255, 255, 255, 0))
        self.ani_enter.setEndValue(QColor(245, 245, 220, 135))

        self.ani_leave = QPropertyAnimation(self, b'color')
        self.ani_leave.setDuration(150)
        self.ani_leave.setStartValue(QColor(245, 245, 220, 135))
        self.ani_leave.setEndValue(QColor(255, 255, 255, 0))

    def get_color(self):
        return self._color

    def set_color(self, col):
        self._color = col
        self.setStyleSheet('''QPushButton{background: rgba(%s, %s, %s, %s); border: 0px solid;}''' % (
            col.red(), col.green(), col.blue(), col.alpha()))

    color = pyqtProperty(QColor, fget=get_color, fset=set_color)

    def enterEvent(self, *args, **kwargs):
        self.ani_enter.start()

    def leaveEvent(self, *args, **kwargs):
        self.ani_leave.start()

    def mousePressEvent(self, *args, **kwargs):
        super(OtherButton, self).mousePressEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(240, 255, 220, 195); border: 0px solid;}''')

    def mouseReleaseEvent(self, *args, **kwargs):
        super(OtherButton, self).mouseReleaseEvent(*args, **kwargs)
        self.setStyleSheet('''QPushButton{background-color: rgba(245, 245, 220, 135); border: 0px solid;}''')


class ShockwaveWidget(QWidget):
    def __init__(self, parent=None):
        super(ShockwaveWidget, self).__init__(parent)

        self.__startPos = None
        self.__endPos = None
        self.__isTracking = False

        self.l_bg = QLabel(self)

        self.btn_close = CloseButton(icon('fa.times', color='azure'), '', self)
        self.btn_mini = OtherButton(icon('fa.minus', color='azure'), '', self)
        self.btn_hint = OtherButton(icon('fa.chevron-down', color='azure'), '', self)

        self.__g_setting()
        self.__s_setting()
        self.__o_setting()

    def __g_setting(self):
        self.resize(500, 500)

        self.l_bg.setGeometry(0, 0, 500, 500)

    def __s_setting(self):
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.l_bg.setStyleSheet('''background:lightblue''')

    def __o_setting(self):
        self.btn_close.clicked.connect(self.close)
        # obj.btn_close.clicked.connect(lambda: systemtrayicon('shutdown -s -t 5'))
        self.btn_mini.clicked.connect(self.showMinimized)

    def geometry_setting(self):
        pass

    def style_setting(self):
        pass

    def other_setting(self):
        pass

    def closeEvent(self, e):
        self.btn_close.setStyleSheet('''background:transparent''')
        self.btn_close.repaint()
        e.accept()

    def resizeEvent(self, e):
        w = self.geometry().width()

        self.l_bg.resize(self.size())

        self.btn_close.move(w - 40, 0)
        self.btn_mini.move(w - 80, 0)
        self.btn_hint.move(w - 120, 0)

    def mouseMoveEvent(self, e):
        try:
            self.__endPos = e.pos() - self.__startPos
            self.move(self.pos() + self.__endPos)
        except TypeError:
            pass

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = True
            self.__startPos = QPoint(e.x(), e.y())

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.__isTracking = False
            self.__startPos = None
            self.__endPos = None
