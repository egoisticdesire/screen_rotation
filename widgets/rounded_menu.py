from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMenu


class RoundedCornersQMenu(QMenu):
    def __init__(self, radius=8):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self._radius = radius
        self.setStyleSheet(
            f'''
                QMenu{{
                    font-size: 16px;
                    background-color: rgb(26, 26, 26);
                    color: rgb(200, 200, 200);
                    border: 1px solid rgb(86, 86, 86);
                    border-radius: {self._radius}px;
                }}
                QMenu::item {{
                    border-radius: 6px;
                    padding: 4px 10px;
                    margin: 4px;
                    padding-left: 20px;
                }}
                QMenu::icon {{
                    padding: 5px 10px;
                }}
                QMenu::item:selected {{
                    background-color: rgb(46, 46, 46);
                }}
                QMenu::item:pressed {{
                    background-color: rgb(36, 36, 36);
                }}
                QMenu::item:disabled {{
                    color: rgb(96, 96, 96);
                    background-color: rgb(36, 36, 36);
                }}
                QMenu::separator {{
                    height: 1px;
                    background-color: rgb(46, 46, 46);
                }}
            '''
        )

    def resizeEvent(self, event):
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect()).adjusted(-.5, -.5, -.01, -.01)
        path.addRoundedRect(rect, self._radius, self._radius)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)
