from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.employeeservice import AddEmployeeService


class AddEmployeeController:
    def __init__(self, tab:QWidget):
        self.tab = tab
        self.service = AddEmployeeService()
        self.username = self.tab.username
        self.user_role = self.tab.user_role
        self.load_employee()
        self.connect_signal()
        

    def connect_signal(self):
        try:
            self.tab.pushButtonAddEmployee.clicked.disconnect()
        except TypeError:
            pass  
        self.tab.pushButtonAddEmployee.clicked.connect(self.handle_add_employee)

    def load_employee(self):
        try:
            employee_list = self.service.get_employees()
            self.tab.tableWidgetEmployee.setRowCount(len(employee_list))
            self.tab.tableWidgetEmployee.setColumnCount(8)
            self.tab.tableWidgetEmployee.setHorizontalHeaderLabels([
                "Müşteri Adı",
                "Telefon",
                "Telefon 2",
                "Yetkili",
                "Yetkili Telefon",
                "Yetkili Telefon 2",
                "Müşteri Adres",
                "Ekleyen Kullanıcı"
            ])
            for row_index, employee in enumerate(employee_list):
                self.tab.tableWidgetEmployee.setItem(row_index,0,QTableWidgetItem(employee["employeeName"]))
                self.tab.tableWidgetEmployee.setItem(row_index,1,QTableWidgetItem(employee["employeePhone"]))
                self.tab.tableWidgetEmployee.setItem(row_index,2,QTableWidgetItem(employee["employeePhone2"]))
                self.tab.tableWidgetEmployee.setItem(row_index,3,QTableWidgetItem(employee["employeeAuthority"]))
                self.tab.tableWidgetEmployee.setItem(row_index,4,QTableWidgetItem(employee["employeeAuthorityPhone"]))
                self.tab.tableWidgetEmployee.setItem(row_index,5,QTableWidgetItem(employee["employeeAuthorityPhone2"]))
                self.tab.tableWidgetEmployee.setItem(row_index,6,QTableWidgetItem(employee["employeeAdress"]))
                self.tab.tableWidgetEmployee.setItem(row_index,7,QTableWidgetItem(employee["userName"]))

                

        except Exception as e:
            QMessageBox.warning(self.tab,"Hata","Müşteri Bilgileri Getirilirken Hata Oluştu")
            print(str(e))

    def handle_add_employee(self):

        # Get Data 
        employee_name = self.tab.lineEditEmployeeName.text().upper().strip()
        employee_phone = self.tab.lineEditEmployeePhone.text().strip()
        employee_phone2 = self.tab.lineEditEmployeePhone2.text().strip()
        employee_authority = self.tab.lineEditEmployeeAuthority.text().upper().strip()
        employee_authority_phone = self.tab.lineEditAuthorityPhone.text().strip()
        employee_authority_phone2 = self.tab.lineEditAuthorityPhone2.text().strip()
        employee_adress = self.tab.textEditEmployeeAdress.toPlainText().upper().strip()

        # Employee Name Validation
        if not employee_name:
            QMessageBox.warning(self.tab, "Uyarı", "Müşteri Ünvanı Zorunludur.")
            return
        if not all(phone.isdigit() for phone in [employee_phone, employee_phone2, employee_authority_phone, employee_authority_phone2]):
            QMessageBox.warning(self.tab,"Hata", "Telefon Numaraları Zorunludur ve Yalnızca Rakamlardan Oluşabilir")
            return
        if len(employee_phone) != 10 or len(employee_phone2) != 10 or len(employee_authority_phone) != 10 or len(employee_authority_phone2) != 10: 
            QMessageBox.warning(self.tab,"Hata","Telefon Numaraları Yalnızca 10 Haneli Olmalıdır")
            return
        else:
            try:
                result = self.service.add_employee({
                    "employee_name": employee_name,
                    "employee_phone": employee_phone,
                    "employee_phone2": employee_phone2,
                    "employee_authority": employee_authority,
                    "employee_authority_phone": employee_authority_phone,
                    "employee_authority_phone2": employee_authority_phone2,
                    "employee_adress": employee_adress,
                    "username":self.username
                })
                if "Bilgi" in result:
                    self.load_employee()
                    QMessageBox.information(self.tab,"Bilgi","Müşteri Ekleme İşlemi Başarıyla Gerçekleştirildi")

                    self.tab.lineEditEmployeeName.clear()
                    self.tab.lineEditEmployeePhone.clear()
                    self.tab.lineEditEmployeePhone2.clear()
                    self.tab.lineEditEmployeeAuthority.clear()
                    self.tab.lineEditAuthorityPhone.clear()
                    self.tab.lineEditAuthorityPhone2.clear()
                    self.tab.textEditEmployeeAdress.clear()
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.tab,"Hata",f"Müşteri Ekleme İşleminde Hata Oluştu:\n{str(hata)}")

            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Bir Hata Oluştu: {str(e)}")
                return

        