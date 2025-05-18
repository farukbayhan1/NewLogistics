from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class PersonelDropdown(QWidget):
    def __init__(self, main_window_ref):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/personel.ui", self)
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
        self.pushButtonDriverOperation.clicked.connect(self.open_driver_operation_tab)
        self.pushButtonCourierOperation.clicked.connect(self.open_courier_operation_tab)
        self.pushButtonUserOperation.clicked.connect(self.open_user_operation_tab)


    def open_driver_operation_tab(self):
        self.hide()
        self.mainWindowRef.show_driver_operations()
    
    def open_courier_operation_tab(self):
        self.hide()
        self.mainWindowRef.show_courier_operations()

    def open_user_operation_tab(self):
        self.hide()
        self.mainWindowRef.show_user_operations()