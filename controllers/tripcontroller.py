from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.tripservice import TripService
import json

class TripController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = tab.username
        self.user_role = tab.user_role
        self.service = TripService()
        self.username = self.tab.username
        self.user_role = self.tab.user_role
        self.connect_signal()
        self.tab.pushButtonCreateTrip.clicked.connect(self.handle_create_trip)
        

        
    def connect_signal(self):
        pass

    def handle_create_trip(self):
        vehicle_id = self.tab.comboBoxVehicle.itemData(self.tab.comboBoxVehicle.currentIndex())
        driver_id = self.tab.comboBoxDriver.itemData(self.tab.comboBoxDriver.currentIndex())
        courier_id = self.tab.comboBoxCourier.itemData(self.tab.comboBoxCourier.currentIndex())
        username = self.username
        trip_loading_province = self.tab.comboBoxLoadingProvince.currentText()
        trip_loading_district = self.tab.comboBoxLoadingDistrict.currentText()
        trip_destination_province = self.tab.comboBoxDestinationProvince.currentText()
        trip_destination_district = self.tab.comboBoxDestinationDistrict.currentText()
        trip_explanation = self.tab.textEditExplanation.toPlainText()
        trip_status_id = "1"
        
        # Check Fields
        if not all([vehicle_id,driver_id,courier_id,username,trip_loading_province,trip_loading_district,trip_destination_province,
                    trip_destination_district]):
            return QMessageBox.warning(self.tab,"Hata","Açıklama Dışındaki Alanlar Zorunludur")
        else:
            try:
                result = self.service.create_trip({
                    "trip_loading_province":trip_loading_province,
                    "trip_loading_district":trip_loading_district,
                    "trip_destination_province":trip_destination_province,
                    "trip_destination_district":trip_destination_district,
                    "trip_explanation":trip_explanation,
                    "trip_status_id":trip_status_id,
                    "username":username,
                    "vehicle_id":vehicle_id,
                    "courier_id":courier_id,
                    "driver_id":driver_id
                })
                if "Bilgi" in result:
                    QMessageBox.information(self.tab,"Bilgi","Yeni Sefer Başarıyla Oluşturuldu")
                    return
                elif "Hata" in result:
                    hata = result[0]
                    QMessageBox.warning(self.tab, "Hata", f"Sefer Oluşturma İşleminde Bir Hata Oluştu: {str(hata)}")

            except Exception as e:
                QMessageBox.warning(self.tab,"Hata",f"Sunucu Hatası {str(e)}")
                print(str(e))
        
    def get_trips(self):
        pass

   
   
    # Update Trip Functions
    def update_trips(self):
        pass

    #