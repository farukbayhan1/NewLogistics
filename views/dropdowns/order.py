from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class OrderDropDown(QWidget):
    def __init__(self, main_window_ref):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/order.ui", self)
        self.mainWindowRef = main_window_ref
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
        self.pushButtonAddOrder.clicked.connect(self.open_add_order_tab)
        self.pushButtonUpdateOrder.clicked.connect(self.open_update_order_tab)
        self.pushButtonReportOrder.clicked.connect(self.open_report_order_tab)


    def open_add_order_tab(self):
        self.hide()
        self.mainWindowRef.show_add_order()

    def open_update_order_tab(self):
        self.hide()
        self.mainWindowRef.show_update_order()
    
    def open_report_order_tab(self):
        self.hide()
        self.mainWindowRef.show_report_order()