from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QApplication,QDialog
from PyQt5.QtCore import Qt, QPropertyAnimation
from services.employeeservice import AddEmployeeService
from views.progressbar.progressbar import LoadingDialog


class CreateOrder(QDialog): 
    def __init__(self, controller=None):
        super().__init__()
        uic.loadUi("ui/templates/form/order/createorder.ui", self)

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

        self.controller = controller
        self.load_employee()
        
    def load_employee(self):
        self.comboBoxEmployee.clear()
        service = AddEmployeeService()
        employee_list = service.get_employees()
        for employee in employee_list:
            employee_name = employee['employeeName']
            self.comboBoxEmployee.addItem(employee_name,employee.get('employeeId'))
        print(employee_list)
    
    

    

   