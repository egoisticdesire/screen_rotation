from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QMenu


class RoundedCornersQMenu(QMenu):
    def __init__(self, radius=10):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        self.radius = radius

    def resizeEvent(self, event):
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect()).adjusted(.5, .5, -1.1, -1.1)
        path.addRoundedRect(rect, self.radius, self.radius)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
