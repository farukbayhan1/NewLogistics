from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.driverservice import DriverService
from views.form.updatedriver import DriverUpdate


class DriverController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = tab.username
        self.user_role = tab.user_role
        self.service = DriverService()
        self.connect_signal()
        self.load_drivers()
        

    
    def connect_signal(self):
        self.tab.pushButtonDriverAdd.clicked.connect(self.handle_add_driver)
        self.tab.tableWidgetDrivers.cellDoubleClicked.connect(self.handle_double_click)
        
    
    
    def handle_add_driver(self):
        driver_tc_no = self.tab.lineEditDriverTcNo.text().strip()
        driver_name = self.tab.lineEditDriverName.text().upper().strip()
        driver_surname = self.tab.lineEditDriverSurname.text().upper().strip()
        driver_phone = self.tab.lineEditDriverPhone.text().strip()
        driver_adress = self.tab.textEditDriverAdress.toPlainText().upper().strip()

        # Line Controls
        if not driver_tc_no or not driver_name or not driver_surname:
            QMessageBox.warning(self.tab,"Uyarı", "TC No, Ad ve Soyad Zorunludur")
            return
        elif len(driver_tc_no) != 11 or not driver_tc_no.isdigit():
            QMessageBox.warning(self.tab,"Uyarı","TC No 11 Haneli ve Sadece Rakamlardan Oluşmalıdır")
            return
        elif len(driver_phone) != 10 or not driver_phone.isdigit():
            QMessageBox.warning(self.tab,"Uyarı","Telefon Numarası 10 Haneli ve Sadece Rakamlardan Oluşmalıdır")
            return
        else:

        # Service
            try:
                result = self.service.add_driver({
                    "driver_tc_no":driver_tc_no,
                    "driver_name": driver_name,
                    "driver_surname": driver_surname,
                    "driver_phone": driver_phone,
                    "driver_adress": driver_adress,
                    "username":self.username,
                })
                
                if "Bilgi" in result:
                    bilgi = result.get("Bilgi")
                    self.load_drivers()
                    QMessageBox.information(self.tab, "Başarılı",f"{bilgi}")
                    
                    # Clear
                    self.tab.lineEditDriverTcNo.clear()
                    self.tab.lineEditDriverName.clear()
                    self.tab.lineEditDriverSurname.clear()
                    self.tab.lineEditDriverPhone.clear()
                    self.tab.textEditDriverAdress.clear()
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.tab, "Hata", f"{str(hata)}")

            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Sürücü Ekleme İşleminde Hata Oluştu:\n{str(e)}")
                

    def load_drivers(self):
        try:
            driver_list = self.service.get_drivers()
            self.tab.tableWidgetDrivers.setRowCount(len(driver_list))
            self.tab.tableWidgetDrivers.setColumnCount(7)
            self.tab.tableWidgetDrivers.setHorizontalHeaderLabels([
                "Sürücü Id",
                "TC No",
                "Adı",
                "Soyadı",
                "Telefon",
                "Adres",
                "Ekleyen Kullanıcı"
            ])
            
            for row_index, driver in enumerate(driver_list):
                self.tab.tableWidgetDrivers.setItem(row_index,0,QTableWidgetItem(str(driver["driverId"])))
                self.tab.tableWidgetDrivers.setItem(row_index,1,QTableWidgetItem(driver["driverTcNo"]))
                self.tab.tableWidgetDrivers.setItem(row_index,2,QTableWidgetItem(driver["driverName"]))
                self.tab.tableWidgetDrivers.setItem(row_index,3,QTableWidgetItem(driver["driverSurname"]))
                self.tab.tableWidgetDrivers.setItem(row_index,4,QTableWidgetItem(driver["driverPhone"]))
                self.tab.tableWidgetDrivers.setItem(row_index,5,QTableWidgetItem(driver["driverAdress"]))
                self.tab.tableWidgetDrivers.setItem(row_index,6,QTableWidgetItem(driver["userName"]))
            self.tab.tableWidgetDrivers.setColumnHidden(0, True)
                
        except Exception as e:
            QMessageBox.warning(self.tab,"Hata","Sürücü Bilgileri Getirilirken Hata Oluştu")
            print(str(e))
    
    # UPDATE
    def open_update_form(self,driver_data):
        self.form = DriverUpdate(controller=self,driver_data=driver_data)
        self.form.show()  
        self.form.animation.start()  
        self.form.labelDriverId.setText(driver_data["driverId"])
        self.form.pushButtonUpdateDriver.clicked.connect(self.handle_update_driver)
     

    def calendar_show(self):
        self.calendar.show()
        self.calendar.animation.start()

    
    def handle_update_driver(self):
        driver_id = self.form.labelDriverId.text()
        driver_tc_no = self.form.labelDriverTcNo.text()
        driver_name = self.form.lineEditDriverName.text().strip().upper()
        driver_surname = self.form.lineEditDriverSurname.text().strip().upper()
        driver_phone = self.form.lineEditDriverPhone.text().strip()
        driver_adress = self.form.textEditDriverAdress.toPlainText().upper()

        # Check Fields
        if not all([driver_tc_no,driver_name,driver_surname,driver_phone]):
            QMessageBox.warning(self.form,"Hata","İsim Soyisim ve Telefon Zorunlu Alandır")
            return
        
        elif not driver_phone.isdigit() or len(driver_phone) != 10:
            QMessageBox.warning(self.form,"Hata","Telefon Numarası Yalnızca On Haneli ve Rakamlardan Oluşmalıdır")
            return
        else:
            try:
                result = self.service.update_driver({
                    "driver_id":driver_id,
                    "driver_tc_no":driver_tc_no,
                    "driver_name":driver_name,
                    "driver_surname":driver_surname,
                    "driver_phone":driver_phone,
                    "driver_adress":driver_adress
                })

                if "Bilgi" in result:
                    self.load_drivers()
                    return QMessageBox.information(self.form,"Bilgi","Sürücü Bilgileri Başarıyla Güncellendi")

                elif "Hata" in result:
                    hata = result.get("Hata")
                    return QMessageBox.warning(self.form,"Hata",f"Sürücü Bilgileri Güncellenirken Hata Oluştu {str(hata)}")
            except Exception as e:
                return QMessageBox.warning(self.form,"Hata",f"Sürücü Bilgileri Güncellenirken Hata Oluştu {str(e)}")
                
    def handle_double_click(self,row,column):

        driver_data = {
            "driverId": self.tab.tableWidgetDrivers.item(row,0).text(),
            "driverTcNo": self.tab.tableWidgetDrivers.item(row, 1).text(),
            "driverName": self.tab.tableWidgetDrivers.item(row, 2).text(),
            "driverSurname": self.tab.tableWidgetDrivers.item(row, 3).text(),
            "driverPhone": self.tab.tableWidgetDrivers.item(row, 4).text(),
            "driverAdress": self.tab.tableWidgetDrivers.item(row, 5).text()
        }
        self.open_update_form(driver_data)
        
