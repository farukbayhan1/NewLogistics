from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class ReportDropDown(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/report.ui", self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)