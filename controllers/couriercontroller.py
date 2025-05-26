from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidgetItem, QAbstractItemView, QProgressBar, QApplication
from PyQt5.QtCore import QEvent,QObject
from services.courierservice import CourierService

class CourierController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = tab.username
        self.user_role = tab.user_role
        self.service = CourierService()
        self.connect_signal()
    
    def connect_signal(self):
        self.tab.pushButtonCurierAdd.clicked.connect(self.handle_add_courier)
        

    def handle_add_courier(self):
        courier_tc_no = self.tab.lineEditCourierTcNo.text().strip()
        courier_name = self.tab.lineEditCourierName.text().upper().strip()
        courier_surname = self.tab.lineEditCourierSurname.text().upper().strip()
        courier_phone = self.tab.lineEditCourierPhone.text().strip()
        courier_adress = self.tab.textEditCourierAdress.toPlainText().strip()

        # Line Controls
        if not courier_tc_no or not courier_name or not courier_surname or not courier_phone:
            QMessageBox.warning(self.tab,"Uyarı","Tc No, Ad ve Soyad Zorunludur")
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
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.tab, "Hata", f"{str(hata)}")
            except Exception as e:
                QMessageBox.warning(self.tab, "Hata", f"Kurye ekleme işleminde hata oluştu:\n{str(e)}")

        