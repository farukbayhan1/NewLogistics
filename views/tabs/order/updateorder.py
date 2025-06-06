from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation


class UpdateOrderTab(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/templates/tabs/order/updateorder.ui", self)
        # Sekme olarak kullanılacağı için pencere efekti kaldırıldı
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

