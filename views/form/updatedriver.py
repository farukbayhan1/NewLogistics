from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation

class DriverUpdate(QWidget):
    def __init__(self,controller=None,driver_data=None):
        super().__init__()
        uic.loadUi("ui/templates/form/updateform/updatedriver.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setStyleSheet("background-color: rgba(242, 246, 252, 255); border-radius: 15px;")
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.controller = controller
        self.driver_data = driver_data
        self.labelDriverId.setVisible(False)
        self.load_data()

    def load_data(self):
        if not self.driver_data:
            return

        self.lineEditDriverTcNo.setText(self.driver_data.get("driverTcNo",""))
        self.lineEditDriverName.setText(self.driver_data.get("driverName",""))
        self.lineEditDriverSurname.setText(self.driver_data.get("driverSurname",""))
        self.lineEditDriverPhone.setText(self.driver_data.get("driverPhone",""))
        self.textEditDriverAdress.setText(self.driver_data.get("driverAdress",""))
