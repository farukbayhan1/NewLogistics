from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation

class CourierUpdate(QWidget):
    def __init__(self,controller=None,courier_data=None):
        super().__init__()
        uic.loadUi("ui/templates/form/updateform/updatecourier.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setStyleSheet("background-color: rgba(242, 246, 252, 255); border-radius: 15px;")
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.controller = controller
        self.courier_data = courier_data
        self.labelCourierId.setVisible(False)
        self.load_data()

    def load_data(self):
        if not self.courier_data:
            return

        self.lineEditCourierTcNo.setText(self.courier_data.get("courierTcNo",""))
        self.lineEditCourierName.setText(self.courier_data.get("courierName",""))
        self.lineEditCourierSurname.setText(self.courier_data.get("courierSurname",""))
        self.lineEditCourierPhone.setText(self.courier_data.get("courierPhone",""))
        self.textEditCourierAdress.setText(self.courier_data.get("courierAdress",""))
