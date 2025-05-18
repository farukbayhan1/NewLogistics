from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class EmployeeDropDown(QWidget):
    def __init__(self, main_window_ref):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/employee.ui", self)
        self.mainWindowRef = main_window_ref
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None)  # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self)  # Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.pushButtonAddEmployee.clicked.connect(self.open_add_employee_tab)
        self.pushButtonUpdateEmployee.clicked.connect(self.open_update_employee_tab)
        self.pushButtonReportEmployee.clicked.connect(self.open_report_employee_tab)


    def open_add_employee_tab(self):
        self.hide()
        self.mainWindowRef.show_add_employee() 

    def open_update_employee_tab(self):
        self.hide()
        self.mainWindowRef.show_update_employee()
    
    def open_report_employee_tab(self):
        self.hide()
        self.mainWindowRef.show_report_employee()

