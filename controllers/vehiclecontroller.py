from PyQt5.QtWidgets import QMessageBox, QWidget, QTableWidget, QTableWidgetItem
from services.vehicleservice import VehicleService
import re

class VehicleController:
    def __init__(self, tab: QWidget):
        self.tab = tab
        self.username = self.tab.username
        self.user_role = self.tab.user_role
        self.service = VehicleService()
        self.connect_signal()
        self.load_vehicles()

    def connect_signal(self):
        self.tab.pushButtonAddVehicle.clicked.connect(self.handle_add_vehicle)

    def load_vehicles(self):
        try:
            vehicle_list = self.service.get_vehicle()
            self.tab.tableWidgetVehicles.setRowCount(len(vehicle_list))
            self.tab.tableWidgetVehicles.setColumnCount(7)
            self.tab.tableWidgetVehicles.setHorizontalHeaderLabels([
                "Plaka",
                "Marka",
                "Model",
                "Model Yılı",
                "Tipi",
                "Max Tonaj",
                "Ekleyen Kullanıcı"
            ])
            for row_index, vehicle in enumerate(vehicle_list):
                self.tab.tableWidgetVehicles.setItem(row_index,0,QTableWidgetItem(vehicle["vehicleNumberPlate"]))
                self.tab.tableWidgetVehicles.setItem(row_index,1,QTableWidgetItem(vehicle["vehicleBrand"]))
                self.tab.tableWidgetVehicles.setItem(row_index,2,QTableWidgetItem(vehicle["vehicleBrand"]))
                self.tab.tableWidgetVehicles.setItem(row_index,3,QTableWidgetItem(vehicle["vehicleModelYear"]))
                self.tab.tableWidgetVehicles.setItem(row_index,4,QTableWidgetItem(vehicle["vehicleType"]))
                self.tab.tableWidgetVehicles.setItem(row_index,5,QTableWidgetItem(vehicle["vehicleLoadCapacity"]))
                self.tab.tableWidgetVehicles.setItem(row_index,6,QTableWidgetItem(vehicle["userName"]))

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
        
        
            