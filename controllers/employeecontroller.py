from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem
from services.employeeservice import AddEmployeeService
from views.form.updateemployee import EmployeeUpdate



class AddEmployeeController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.service = AddEmployeeService()
        self.username = getattr(self.tab, "username", None)
        self.user_role = getattr(self.tab, "user_role", None)

       

        self.load_employee()
        self.connect_signal()

    def connect_signal(self):
        try:
            self.tab.pushButtonAddEmployee.clicked.disconnect()
            self.tab.tableWidgetEmployee.cellDoubleClicked.disconnect()
        except TypeError:
            pass
        self.tab.pushButtonAddEmployee.clicked.connect(self.handle_add_employee)
        self.tab.tableWidgetEmployee.cellDoubleClicked.connect(self.handle_double_click)

    def load_employee(self):
        try:
            employee_list = self.service.get_employees()
            self.tab.tableWidgetEmployee.setRowCount(len(employee_list))
            self.tab.tableWidgetEmployee.setColumnCount(9)
            self.tab.tableWidgetEmployee.setHorizontalHeaderLabels([
                "Müşteri Id",
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
                self.tab.tableWidgetEmployee.setItem(row_index, 0, QTableWidgetItem(str(employee["employeeId"])))
                self.tab.tableWidgetEmployee.setItem(row_index, 1, QTableWidgetItem(employee["employeeName"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 2, QTableWidgetItem(employee["employeePhone"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 3, QTableWidgetItem(employee["employeePhone2"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 4, QTableWidgetItem(employee["employeeAuthority"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 5, QTableWidgetItem(employee["employeeAuthorityPhone"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 6, QTableWidgetItem(employee["employeeAuthorityPhone2"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 7, QTableWidgetItem(employee["employeeAdress"]))
                self.tab.tableWidgetEmployee.setItem(row_index, 8, QTableWidgetItem(employee["userName"]))
            self.tab.tableWidgetEmployee.setColumnHidden(0, True) 

        except Exception as e:
            return QMessageBox.warning(self.tab, "Hata", "Müşteri Bilgileri Getirilirken Hata Oluştu")
           
    def handle_add_employee(self):
        
        employee_name = self.tab.lineEditEmployeeName.text().upper().strip()
        employee_phone = self.tab.lineEditEmployeePhone.text().strip()
        employee_phone2 = self.tab.lineEditEmployeePhone2.text().strip()
        employee_authority = self.tab.lineEditEmployeeAuthority.text().upper().strip()
        employee_authority_phone = self.tab.lineEditAuthorityPhone.text().strip()
        employee_authority_phone2 = self.tab.lineEditAuthorityPhone2.text().strip()
        employee_adress = self.tab.textEditEmployeeAdress.toPlainText().upper().strip()

      
        if not employee_name:
            QMessageBox.warning(self.tab, "Uyarı", "Müşteri Ünvanı Zorunludur.")
            return

        phone_fields = [employee_phone, employee_phone2, employee_authority_phone, employee_authority_phone2]
        if not all(phone.isdigit() for phone in phone_fields):
            QMessageBox.warning(self.tab, "Hata", "Telefon Numaraları Zorunludur ve Yalnızca Rakamlardan Oluşabilir")
            return

        if any(len(phone) != 10 for phone in phone_fields):
            QMessageBox.warning(self.tab, "Hata", "Telefon Numaraları Yalnızca 10 Haneli Olmalıdır")
            return

        try:
            result = self.service.add_employee({
                "employee_name": employee_name,
                "employee_phone": employee_phone,
                "employee_phone2": employee_phone2,
                "employee_authority": employee_authority,
                "employee_authority_phone": employee_authority_phone,
                "employee_authority_phone2": employee_authority_phone2,
                "employee_adress": employee_adress,
                "username": self.username
            })

            if "Bilgi" in result:
                self.load_employee()
                QMessageBox.information(self.tab, "Bilgi", "Müşteri Ekleme İşlemi Başarıyla Gerçekleştirildi")
                self.clear_form()
            elif "Hata" in result:
                hata = result.get("Hata")
                QMessageBox.warning(self.tab, "Hata", f"Müşteri Ekleme İşleminde Hata Oluştu:\n{hata}")

        except Exception as e:
            QMessageBox.warning(self.tab, "Hata", f"Bir Hata Oluştu: {e}")

    def clear_form(self):
        self.tab.lineEditEmployeeName.clear()
        self.tab.lineEditEmployeePhone.clear()
        self.tab.lineEditEmployeePhone2.clear()
        self.tab.lineEditEmployeeAuthority.clear()
        self.tab.lineEditAuthorityPhone.clear()
        self.tab.lineEditAuthorityPhone2.clear()
        self.tab.textEditEmployeeAdress.clear()

    def handle_double_click(self, row, column):
        employee_data = {
            "employeeId": self.tab.tableWidgetEmployee.item(row, 0).text(),
            "employeeName": self.tab.tableWidgetEmployee.item(row, 1).text(),
            "employeePhone": self.tab.tableWidgetEmployee.item(row, 2).text(),
            "employeePhone2": self.tab.tableWidgetEmployee.item(row, 3).text(),
            "employeeAuthority": self.tab.tableWidgetEmployee.item(row, 4).text(),
            "employeeAuthorityPhone": self.tab.tableWidgetEmployee.item(row, 5).text(),
            "employeeAuthorityPhone2": self.tab.tableWidgetEmployee.item(row, 6).text(),
            "employeeAdress": self.tab.tableWidgetEmployee.item(row, 7).text()
        }
        self.open_update_form(employee_data)

    def open_update_form(self, employee_data):
        self.form = EmployeeUpdate(controller=self, employee_data=employee_data)
        self.form.show()
        self.form.animation.start()
        self.form.labelEmployeeId.setText(employee_data["employeeId"])
        self.form.pushButtonUpdateEmployee.clicked.connect(self.handle_employee_update)

    def handle_employee_update(self):
        employee_id_text = self.form.labelEmployeeId.text().strip()

        if not employee_id_text or not employee_id_text.isdigit():
            QMessageBox.warning(self.form, "Hata", "Geçersiz Müşteri ID")
            return

        employee_id = int(employee_id_text)

        employee_name = self.form.lineEditEmployeeName.text().upper().strip()
        employee_phone = self.form.lineEditEmployeePhone.text().strip()
        employee_phone2 = self.form.lineEditEmployeePhone2.text().strip()
        employee_authority = self.form.lineEditEmployeeAuthority.text().upper().strip()
        employee_authority_phone = self.form.lineEditAuthorityPhone.text().strip()
        employee_authority_phone2 = self.form.lineEditAuthorityPhone2.text().strip()
        employee_adress = self.form.textEditEmployeeAdress.toPlainText().upper().strip()

       
        if not employee_name:
            return QMessageBox.warning(self.form, "Hata", "Müşteri İsmi Boş Olamaz")

        phone_fields = [employee_phone, employee_phone2, employee_authority_phone, employee_authority_phone2]
        if not all(phone.isdigit() for phone in phone_fields):
            return QMessageBox.warning(self.form, "Hata", "Telefon Numaraları Zorunludur ve Yalnızca Rakamlardan Oluşabilir")
            
        if any(len(phone) != 10 for phone in phone_fields):
            return QMessageBox.warning(self.form, "Hata", "Telefon Numaraları Yalnızca 10 Haneli Olmalıdır")
            
        try:
            result = self.service.update_employee({
                "employee_id": employee_id,
                "employee_name": employee_name,
                "employee_phone": employee_phone,
                "employee_phone2": employee_phone2,
                "employee_authority": employee_authority,
                "employee_authority_phone": employee_authority_phone,
                "employee_authority_phone2": employee_authority_phone2,
                "employee_adress": employee_adress
            })

            if "Bilgi" in result:
                return QMessageBox.information(self.form, "Bilgi", "Müşteri Bilgileri Başarıyla Güncellendi")
                self.load_employee()
            elif "Hata" in result:
                hata = result.get("Hata")
                return QMessageBox.warning(self.form, "Hata", f"Müşteri Bilgileri Güncelleme İşleminde Hata Oluştu: {hata}")

        except Exception as e:
            return QMessageBox.warning(self.form, "Hata", f"Sunucu Hatası: {e}")
