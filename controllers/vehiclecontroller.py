from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.vehicleservice import VehicleService
from views.form.updatevehicle import VehicleUpdate
import re

class VehicleController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = self.tab.username
        self.user_role = self.tab.user_role
        self.service = VehicleService()
        self.connect_signal()
        self.load_vehicles()
        
    # ______ Update Form _____________________________________________________________
    def handle_double_click(self, row, column):

        vehicle_data = {
            "vehicleId": self.tab.tableWidgetVehicles.item(row,0).text(),
            "vehicleNumberPlate": self.tab.tableWidgetVehicles.item(row, 1).text(),
            "vehicleBrand": self.tab.tableWidgetVehicles.item(row, 2).text(),
            "vehicleModel": self.tab.tableWidgetVehicles.item(row, 3).text(),
            "vehicleModelYear": self.tab.tableWidgetVehicles.item(row, 4).text(),
            "vehicleType": self.tab.tableWidgetVehicles.item(row, 5).text(),
            "vehicleLoadCapacity": self.tab.tableWidgetVehicles.item(row, 6).text(),
        }
        self.open_update_form(vehicle_data)


    def open_update_form(self, vehicle_data):
        self.form = VehicleUpdate(controller=self,vehicle_data=vehicle_data)
        self.form.show()  
        self.form.animation.start()  
        self.form.labelVehicleId.setText(vehicle_data["vehicleId"])
        self.form.pushButtonUpdateVehicle.clicked.connect(self.handle_update_vehicles)

    
    def handle_update_vehicles(self):
        vehicle_id = self.form.labelVehicleId.text()
        vehicle_number_plate = self.form.lineEditNumberPlate.text().upper().strip()
        vehicle_brand = self.form.lineEditBrand.text().upper().strip()
        vehicle_model = self.form.lineEditModel.text().upper().strip()
        vehicle_model_year = self.form.lineEditModelYear.text().strip()
        vehicle_type = self.form.lineEditType.text().upper().strip()
        vehicle_load_capacity = self.form.lineEditLoadCapacity.text().strip()

        # Check Lines
        if not all([vehicle_number_plate,vehicle_brand,vehicle_model,vehicle_model_year,vehicle_type,vehicle_load_capacity]):
            return QMessageBox.warning(self.tab,"Uyarı", "Plaka, Marka, Model, Model Yılı, Araç Tipi ve Max Tonaj Zorunlu Alandır")
        
        # Check Number Plate
        elif not re.match(r'^\d{2}[A-Z]{1,3}\d{2,4}$', vehicle_number_plate.upper()):
            print(vehicle_number_plate)
            return QMessageBox.warning(self.tab, "Uyarı", "Plaka Değer İçin Beklenen Format Uygun Değil")

        # Check Vehicle Model Year
        elif not vehicle_model_year.isdigit() and len(vehicle_model_year) != 4:
            return QMessageBox.warning(self.tab, "Uyarı", "Model Yılı Dört Haneli ve Rakamlardan Oluşmalıdır")
        
        # Check Load Capacity
        elif not vehicle_load_capacity.isdigit() and len(vehicle_load_capacity) > 5:
            return QMessageBox.warning(self.tab, "Uyarı", "Max Tonaj Yalnızca Rakamlardan Oluşabilir")
        
        else:
            try:
                result = self.service.update_vehicle({
                    "vehicle_id" : vehicle_id,
                    "vehicle_number_plate":vehicle_number_plate,
                    "vehicle_brand":vehicle_brand,
                    "vehicle_model":vehicle_model,
                    "vehicle_model_year":vehicle_model_year,
                    "vehicle_type":vehicle_type,
                    "vehicle_load_capacity":vehicle_load_capacity,
                    "username":self.username
                })
            
                if "Bilgi" in result:
                    print(result)
                    return QMessageBox.information(self.form,"Bilgi","Araç Güncelleme İşlemi Başarılı")
                    
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.form,"Hata", f"Araç Güncelleme İşlemi Başarısız {str(hata)}")
                
            except Exception as e:
                QMessageBox.warning(self.form,"Hata",f"Araç Güncelleme İşleminda Hata Oluştu: {str(e)}")

# _______________________________________________________________________________________________________        
    
    def connect_signal(self):
        self.tab.pushButtonAddVehicle.clicked.connect(self.handle_add_vehicle)
        self.tab.tableWidgetVehicles.cellDoubleClicked.connect(self.handle_double_click)
    
    def load_vehicles(self):
        try:
            vehicle_list = self.service.get_vehicle()
            self.tab.tableWidgetVehicles.setRowCount(len(vehicle_list))
            self.tab.tableWidgetVehicles.setColumnCount(8)
            self.tab.tableWidgetVehicles.setHorizontalHeaderLabels([
                "Araç Id",
                "Plaka",
                "Marka",
                "Model",
                "Model Yılı",
                "Tipi",
                "Max Tonaj",
                "Ekleyen Kullanıcı"
            ])

            for row_index, vehicle in enumerate(vehicle_list):
                self.tab.tableWidgetVehicles.setItem(row_index,0,QTableWidgetItem(str(vehicle["vehicleId"])))
                self.tab.tableWidgetVehicles.setItem(row_index,1,QTableWidgetItem(vehicle["vehicleNumberPlate"]))
                self.tab.tableWidgetVehicles.setItem(row_index,2,QTableWidgetItem(vehicle["vehicleBrand"]))
                self.tab.tableWidgetVehicles.setItem(row_index,3,QTableWidgetItem(vehicle["vehicleModel"]))
                self.tab.tableWidgetVehicles.setItem(row_index,4,QTableWidgetItem(vehicle["vehicleModelYear"]))
                self.tab.tableWidgetVehicles.setItem(row_index,5,QTableWidgetItem(vehicle["vehicleType"]))
                self.tab.tableWidgetVehicles.setItem(row_index,6,QTableWidgetItem(vehicle["vehicleLoadCapacity"]))
                self.tab.tableWidgetVehicles.setItem(row_index,7,QTableWidgetItem(vehicle["userName"]))
            self.tab.tableWidgetVehicles.setColumnHidden(0, True)
            
        except Exception as e:
            QMessageBox.warning(self.tab,"Hata",f"Araçlar Getirilirken Hata Oluştu: {str(e)}")
    
    

    def handle_add_vehicle(self):
        vehicle_number_plate = self.tab.lineEditNumberPlate.text().upper().strip()
        vehicle_brand = self.tab.lineEditBrand.text().upper().strip()
        vehicle_model = self.tab.lineEditModel.text().upper().strip()
        vehicle_model_year = self.tab.lineEditModelYear.text().strip()
        vehicle_type = self.tab.lineEditType.text().upper().strip()
        vehicle_load_capacity = self.tab.lineEditLoadCapacity.text().strip()

        # Check Lines
        if not all([vehicle_number_plate,vehicle_brand,vehicle_model,vehicle_model_year,vehicle_type,vehicle_load_capacity]):
            return QMessageBox.warning(self.tab,"Uyarı", "Plaka, Marka, Model, Model Yılı, Araç Tipi ve Max Tonaj Zorunlu Alandır")
        
        # Check Number Plate
        elif not re.match(r'^\d{2}[A-Z]{1,3}\d{2,4}$', vehicle_number_plate.upper()):
            print(vehicle_number_plate)
            return QMessageBox.warning(self.tab, "Uyarı", "Plaka Değer İçin Beklenen Format Uygun Değil")

        # Check Vehicle Model Year
        elif not vehicle_model_year.isdigit() and len(vehicle_model_year) != 4:
            return QMessageBox.warning(self.tab, "Uyarı", "Model Yılı Dört Haneli ve Rakamlardan Oluşmalıdır")
        
        # Check Load Capacity
        elif not vehicle_load_capacity.isdigit() and len(vehicle_load_capacity) > 5:
            return QMessageBox.warning(self.tab, "Uyarı", "Max Tonaj Yalnızca Rakamlardan Oluşabilir")

        # Add Vehicle
        else:
            try:
                result = self.service.add_vehicle({
                    "vehicle_number_plate":vehicle_number_plate,
                    "vehicle_brand":vehicle_brand,
                    "vehicle_model":vehicle_model,
                    "vehicle_model_year":vehicle_model_year,
                    "vehicle_type":vehicle_type,
                    "vehicle_load_capacity":vehicle_load_capacity,
                    "username":self.username
                })
                if "Bilgi" in result:
                    self.tab.lineEditNumberPlate.clear()
                    self.tab.lineEditBrand.clear()
                    self.tab.lineEditModel.clear()
                    self.tab.lineEditModelYear.clear()
                    self.tab.lineEditType.clear()
                    self.tab.lineEditLoadCapacity.clear()
                    return QMessageBox.information(self.tab,"Bilgi","Araç Ekleme İşlemi Başarılı")
                elif "Hata" in result:
                    hata = result.get("Hata")
                    QMessageBox.warning(self.tab,"Hata", f"Araç Ekleme İşlemi Başarısız {str(hata)}")

            except Exception as e:
                print(str(e))
                return QMessageBox.warning(self.tab,"Hata",f"Araç Ekleme İşleminde Hata Oluştu: {str(e)}")
        
        
            