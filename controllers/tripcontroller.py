from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.tripservice import TripService
from services.orderservice import OrderService
from datetime import datetime
from views.form.updatetrip import TripUpdate
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
        self.get_trips()

        
    def connect_signal(self):
        self.tab.pushButtonCreateTrip.clicked.connect(self.handle_create_trip)
        self.tab.tableWidgetTrips.itemDoubleClicked.connect(self.handle_double_click)
        
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
                    self.tab.textEditExplanation.clear()
                    self.get_trips()
                    QMessageBox.information(self.tab,"Bilgi","Yeni Sefer Başarıyla Oluşturuldu")
                    return
                elif "Hata" in result:
                    hata = result[0]
                    QMessageBox.warning(self.tab, "Hata", f"Sefer Oluşturma İşleminde Bir Hata Oluştu: {str(hata)}")

            except Exception as e:
                QMessageBox.warning(self.tab,"Hata",f"Sunucu Hatası {str(e)}")
                print(str(e))
        
    def get_trips(self):
        trip_list =self.service.get_trips()
        self.tab.tableWidgetTrips.setRowCount(len(trip_list))
        self.tab.tableWidgetTrips.setColumnCount(10)
        self.tab.tableWidgetTrips.setHorizontalHeaderLabels([
            "Sefer Numarası",
            "Plaka",
            "Sürücü",
            "Kurye",
            "Yükleme İl",
            "Yükleme İlçe",
            "Boşaltma İl",
            "Boşaltma İlçe",
            "Oluşturulma Tarihi",
            "Oluşturan Kullanıcı"
        ])
        
        for row_index, i in enumerate(trip_list):
            raw_date = i["tripStartTime"]
            datetime_obj = datetime.strptime(raw_date, "%a, %d %b %Y %H:%M:%S %Z")
            formatted_date = datetime_obj.strftime("%d.%m.%Y %H:%M")
            self.tab.tableWidgetTrips.setItem(row_index,0,QTableWidgetItem(i["tripCode"]))
            self.tab.tableWidgetTrips.setItem(row_index,1,QTableWidgetItem(i["vehicleNumberPlate"]))
            self.tab.tableWidgetTrips.setItem(row_index,2,QTableWidgetItem(f"{i['driverName']} {i['driverSurname']}"))
            self.tab.tableWidgetTrips.setItem(row_index,3,QTableWidgetItem(f"{i['courierName']} {i['courierSurname']}"))
            self.tab.tableWidgetTrips.setItem(row_index,4,QTableWidgetItem(i["tripLoadingProvince"]))
            self.tab.tableWidgetTrips.setItem(row_index,5,QTableWidgetItem(i["tripLoadingDistrict"]))
            self.tab.tableWidgetTrips.setItem(row_index,6,QTableWidgetItem(i["tripDestinationProvince"]))
            self.tab.tableWidgetTrips.setItem(row_index,7,QTableWidgetItem(i["tripDestinationDistrict"]))
            self.tab.tableWidgetTrips.setItem(row_index,8,QTableWidgetItem(formatted_date))
            self.tab.tableWidgetTrips.setItem(row_index,9,QTableWidgetItem(i["userName"]))
        
    # Update Trip Functions
    def open_update_form(self):
        self.update_form.show()
        self.update_form.animation.start()
        self.update_form.pushButtonLoad.clicked.connect(self.handle_load_orders_to_trip)
        

    # When Doubleclick Selected Row
    def handle_double_click(self,item):
        row = item.row()
        trip_data = ({
            "tripCode": self.tab.tableWidgetTrips.item(row, 0).text(),
            "vehicleNumberPlate": self.tab.tableWidgetTrips.item(row, 1).text(),
            "driverName": self.tab.tableWidgetTrips.item(row, 2).text(),
            "courierName": self.tab.tableWidgetTrips.item(row, 3).text(),
            "tripLoadingProvince": self.tab.tableWidgetTrips.item(row, 4).text(),
            "tripLoadingDistrict": self.tab.tableWidgetTrips.item(row, 5).text(),
            "tripDestinationProvince": self.tab.tableWidgetTrips.item(row, 6).text(),
            "tripDestinationDistrict": self.tab.tableWidgetTrips.item(row, 7).text(),
            "tripStartTime": self.tab.tableWidgetTrips.item(row, 8).text(),
            "userName": self.tab.tableWidgetTrips.item(row, 9).text()
        })
        self.update_form = TripUpdate(controller=self, trip_data=trip_data)
        self.open_update_form()
    
    def handle_load_orders_to_trip(self):
        order_list = self.update_form.selected_order_list
        new_order_list = []
        for order in order_list:
            order_dict = {
                "orderId":order,
                "tripCode":self.update_form.lineEditTripNumber.text().strip()
            }
            new_order_list.append(order_dict)
        try:
            result = self.service.load_trip(new_order_list)
            if "Bilgi" in result:
                QMessageBox.information(self.update_form,"Bilgi","Sefer Başarıyla Oluşturuldu")
            if "Hata" in result:
                hata = result.get("Hata")
                QMessageBox.warning(self.update_form,"Hata",f"Sefer Oluşturulurken Hata Oluştu: {str(hata)}")
        except Exception as e:
            print(e)
            QMessageBox.warning(self.update_form,"Hata",f"Sefer Oluşturma Modülünde Hata, {str(e)}")



   
        
    