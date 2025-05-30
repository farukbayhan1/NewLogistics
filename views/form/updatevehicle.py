from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation

class VehicleUpdate(QWidget):
    def __init__(self,controller=None,vehicle_data=None):
        super().__init__()
        uic.loadUi("ui/templates/form/updateform/updatevehicle.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setStyleSheet("background-color: rgba(242, 246, 252, 255); border-radius: 15px;")
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.controller = controller
        self.vehicle_data = vehicle_data
        self.labelVehicleId.setVisible(False)
        self.load_data()

    def load_data(self):
        if not self.vehicle_data:
            return
        self.lineEditNumberPlate.setText(self.vehicle_data.get("vehicleNumberPlate", ""))
        self.lineEditBrand.setText(self.vehicle_data.get("vehicleBrand", ""))
        self.lineEditModel.setText(self.vehicle_data.get("vehicleModel", ""))
        self.lineEditModelYear.setText(self.vehicle_data.get("vehicleModelYear", ""))
        self.lineEditType.setText(self.vehicle_data.get("vehicleType", ""))
        self.lineEditLoadCapacity.setText(self.vehicle_data.get("vehicleLoadCapacity", ""))
       