from PyQt5.QtWidgets import QMessageBox, QWidget
from services.employeeservice import AddEmployeeService


class AddEmployeeController:
    def __init__(self, tab:QWidget):
        self.tab = tab
        self.connect_signal()
        self.tab.lineEditEmployeeName.focusInEvent = lambda event: print(self.tab.lineEditEmployeeName.text())
        self.service = AddEmployeeService()

    def connect_signal(self):
        self.tab.pushButtonAddEmployee.clicked.connect(self.handle_add_employee)

    def load_employee(self):
        pass

    def handle_add_employee(self):

        # Get Data 
        employee_name = self.tab.lineEditEmployeeName.text().strip()
        employee_phone = self.tab.lineEditEmployeePhone.text().strip()
        employee_phone2 = self.tab.lineEditEmployeePhone2.text().strip()
        employee_authority = self.tab.lineEditEmployeeAuthority.text().strip()
        employee_authority_phone = self.tab.lineEditAuthorityPhone.text().strip()
        employee_authority_phone2 = self.tab.lineEditAuthorityPhone2.text().strip()
        employee_adress = self.tab.textEditEmployeeAdress.toPlainText().strip()

        # Employee Name Validation
        if not employee_name:
            QMessageBox.warning(self.tab, "Uyarı", "Müşteri Ünvanı Zorunludur.")
            return

        try:
            result = self.service.add_employee({
                "employee_name": employee_name,
                "employee_phone": employee_phone,
                "employee_phone2": employee_phone2,
                "employee_authority": employee_authority,
                "employee_authority_phone": employee_authority_phone,
                "employee_authority_phone2": employee_authority_phone2,
                "employee_adress": employee_adress
            })

        except Exception as e:
            QMessageBox.warning(self.tab, "Hata", f"Bir hata oluştu: {str(e)}")
            return

    #def handle_get_employee_list(self):
        