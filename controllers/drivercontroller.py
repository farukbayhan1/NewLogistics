from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.driverservice import DriverService

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
            self.tab.tableWidgetDrivers.setColumnCount(6)
            self.tab.tableWidgetDrivers.setHorizontalHeaderLabels([
                "TC No",
                "Adı",
                "Soyadı",
                "Telefon",
                "Adres",
                "Ekleyen Kullanıcı"
            ])
            
            for row_index, driver in enumerate(driver_list):
                self.tab.tableWidgetDrivers.setItem(row_index,0,QTableWidgetItem(driver["driverTcNo"]))
                self.tab.tableWidgetDrivers.setItem(row_index,1,QTableWidgetItem(driver["driverName"]))
                self.tab.tableWidgetDrivers.setItem(row_index,2,QTableWidgetItem(driver["driverSurname"]))
                self.tab.tableWidgetDrivers.setItem(row_index,3,QTableWidgetItem(driver["driverPhone"]))
                self.tab.tableWidgetDrivers.setItem(row_index,4,QTableWidgetItem(driver["driverAdress"]))
                self.tab.tableWidgetDrivers.setItem(row_index,5,QTableWidgetItem(driver["userName"]))
        except Exception as e:
            QMessageBox.warning(self.tab,"Hata","Sürücü Bilgileri Getirilirken Hata Oluştu")
            print(str(e))
        
