from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QEvent,QObject
from services.courierservice import CourierService
from views.form.updatecourier import CourierUpdate

class CourierController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = tab.username
        self.user_role = tab.user_role
        self.service = CourierService()
        self.connect_signal()
        self.load_couriers()
    
    def connect_signal(self):
        self.tab.pushButtonCourierAdd.clicked.connect(self.handle_add_courier)
        self.tab.tableWidgetCouriers.cellDoubleClicked.connect(self.handle_double_click)
        

    def handle_add_courier(self):
        courier_tc_no = self.tab.lineEditCourierTcNo.text().strip()
        courier_name = self.tab.lineEditCourierName.text().upper().strip()
        courier_surname = self.tab.lineEditCourierSurname.text().upper().strip()
        courier_phone = self.tab.lineEditCourierPhone.text().strip()
        courier_adress = self.tab.textEditCourierAdress.toPlainText().strip()

        # Line Controls
        if not courier_tc_no or not courier_name or not courier_surname or not courier_phone:
            QMessageBox.warning(self.tab,"Uyarı","Tc No, Ad, Soyad ve Telefon Numarası Zorunludur")
            return
        elif len(courier_tc_no) != 11 or not courier_tc_no.isdigit():
            QMessageBox.warning(self.tab,"Uyarı","TC No 11 Haneli ve Sadece Rakamlardan Oluşmalıdır")
            return
        elif len(courier_phone) != 10 or not courier_phone.isdigit():
            QMessageBox.warning(self.tab,"Uyarı","Telefon Numarası 10 Haneli ve Sadece Rakamlardan Oluşmalıdır")
            return
        else:
        
        # Service
            try:
                result = self.service.add_courier({
                     "courier_tc_no":courier_tc_no,
                     "courier_name":courier_name,
                     "courier_surname":courier_surname,
                     "courier_phone":courier_phone,
                     "courier_adress":courier_adress,
                     "username":self.username
                 })

                if "Bilgi" in result:
                    bilgi = result.get("Bilgi")
                    QMessageBox.information(self.tab, "Başarılı",f"{bilgi}")
                    self.load_couriers()
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.tab, "Hata", f"{str(hata)}")
            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Kurye ekleme işleminde hata oluştu:\n{str(e)}")

    def load_couriers(self):
        try:
            courier_list = self.service.get_couriers()
            self.tab.tableWidgetCouriers.setRowCount(len(courier_list))
            self.tab.tableWidgetCouriers.setColumnCount(7)
            self.tab.tableWidgetCouriers.setHorizontalHeaderLabels([
                "Courier Id",
                "TC No",
                "Adı",
                "Soyadı",
                "Telefon",
                "Adres",
                "Ekleyen Kullanıcı"
            ])
            for row_index, courier in enumerate(courier_list):
                self.tab.tableWidgetCouriers.setItem(row_index,0,QTableWidgetItem(str(courier["courierId"])))
                self.tab.tableWidgetCouriers.setItem(row_index,1,QTableWidgetItem(courier["courierTcNo"]))
                self.tab.tableWidgetCouriers.setItem(row_index,2,QTableWidgetItem(courier["courierName"]))
                self.tab.tableWidgetCouriers.setItem(row_index,3,QTableWidgetItem(courier["courierSurname"]))
                self.tab.tableWidgetCouriers.setItem(row_index,4,QTableWidgetItem(courier["courierPhone"]))
                self.tab.tableWidgetCouriers.setItem(row_index,5,QTableWidgetItem(courier["courierAdress"]))
                self.tab.tableWidgetCouriers.setItem(row_index,6,QTableWidgetItem(courier["userName"]))
            self.tab.tableWidgetCouriers.setColumnHidden(0, True)
        except Exception as e:
            return QMessageBox.warning(self.tab,"Hata","Kurye Bilgileri Getirilirken Hata Oluştu")
            print(str(e))  

    # UPDATE

    def open_update_form(self,courier_data):
        self.form = CourierUpdate(controller=self,courier_data = courier_data)
        self.form.show()  
        self.form.animation.start()  
        self.form.labelCourierId.setText(courier_data["courierId"])
        self.form.pushButtonUpdateCourier.clicked.connect(self.handle_update_courier)
        pass

    def handle_double_click(self,row,column):

        courier_data = {
            "courierId": self.tab.tableWidgetCouriers.item(row,0).text(),
            "courierTcNo": self.tab.tableWidgetCouriers.item(row, 1).text(),
            "courierName": self.tab.tableWidgetCouriers.item(row, 2).text(),
            "courierSurname": self.tab.tableWidgetCouriers.item(row, 3).text(),
            "courierPhone": self.tab.tableWidgetCouriers.item(row, 4).text(),
            "courierAdress": self.tab.tableWidgetCouriers.item(row, 5).text()
        }
        self.open_update_form(courier_data)
        


    def handle_update_courier(self):
        courier_id = self.form.labelCourierId.text()
        courier_tc_no = self.form.labelCourierTcNo.text()
        courier_name = self.form.lineEditCourierName.text().strip().upper()
        courier_surname = self.form.lineEditCourierSurname.text().strip().upper()
        courier_phone = self.form.lineEditCourierPhone.text().strip()
        courier_adress = self.form.textEditCourierAdress.toPlainText().upper()

        # Check Fields
        if not all([courier_name,courier_surname,courier_phone]):
            return QMessageBox.warning(self.form,"Hata","Kurye Adı Soyadı ve Telefon Zorunludur")
        elif not courier_phone.isdigit() or len(courier_phone) != 10:
            return QMessageBox.warning(self.form,"Hata","Telefon Numarası Yalnızca 10 Haneli ve Rakamlardan Oluşabilir")
        else:
            try:
                result = self.service.update_courier({
                    "courier_id":courier_id,
                    "courier_tc_no":courier_tc_no,
                    "courier_name":courier_name,
                    "courier_surname":courier_surname,
                    "courier_phone":courier_phone,
                    "courier_adress":courier_adress
                })

                if "Bilgi" in result:
                    self.load_couriers()
                    return QMessageBox.information(self.form,"Bilgi","Kurye Bilgileri Başarıyla Güncellendi")
                elif "Hata" in result:
                    hata = result.get("Hata")
                    print(hata)
                    return QMessageBox.warning(self.form,"Hata",f"Kurye Bilgileri Güncellenirken Hata Oluştu: {str(hata)}")
                
            except Exception as e:
                return QMessageBox.warning(self.form,"Hata",f"Sunucu Hatası: {str(e)}")
    
