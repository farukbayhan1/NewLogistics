from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class ReportDropDown(QWidget):
    def __init__(self, main_window_ref):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/report.ui", self)
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

    # Buttons
        self.pushButtonEmployeeReport.clicked.connect(self.open_employee_report_tab)
        self.pushButtonOrderReport.clicked.connect(self.open_order_report_tab)
        self.pushButtonTripReport.clicked.connect(self.open_trip_report_tab)


    def open_employee_report_tab(self):
        self.hide()
        self.mainWindowRef.show_report_employee()
    def open_order_report_tab(self):
        self.hide()
        self.mainWindowRef.show_report_order()
    def open_trip_report_tab(self):
        self.hide()
        self.mainWindowRef.show_report_trip()
