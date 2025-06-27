from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication,QDialog
from PyQt5.QtCore import Qt, QPropertyAnimation
from services.employeeservice import AddEmployeeService



class GetFilteredOrder(QDialog): 
    def __init__(self, controller=None):
        super().__init__()
        uic.loadUi("ui/templates/form/filter/getorder.ui", self)

        self.setStyleSheet("""
            QDialog {
                background-color: #f2f6fc;
                border-radius: 15px;
            }
        """)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()


    

   