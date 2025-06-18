from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation

class EmployeeUpdate(QWidget):
    def __init__(self,controller=None,employee_data=None):
        super().__init__()
        uic.loadUi("ui/templates/form/updateform/updateemployee.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setStyleSheet("background-color: rgba(242, 246, 252, 255); border-radius: 15px;")
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.controller = controller
        self.employee_data = employee_data
        self.labelEmployeeId.setVisible(False)
        self.load_data()

    def load_data(self):
        if not self.employee_data:
            return
      
        self.lineEditEmployeeName.setText(self.employee_data.get("employeeName",""))
        self.lineEditEmployeePhone.setText(self.employee_data.get("employeePhone",""))
        self.lineEditEmployeePhone2.setText(self.employee_data.get("employeePhone2",""))
        self.lineEditEmployeeAuthority.setText(self.employee_data.get("employeeAuthority",""))
        self.lineEditAuthorityPhone.setText(self.employee_data.get("employeeAuthorityPhone"))
        self.lineEditAuthorityPhone2.setText(self.employee_data.get("employeeAuthorityPhone2"))
        self.textEditEmployeeAdress.setText(self.employee_data.get("employeeAdress"))
