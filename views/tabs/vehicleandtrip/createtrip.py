from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation
from services.driverservice import DriverService
from services.courierservice import CourierService
from services.vehicleservice import VehicleService
import json


class CreateTripTab(QWidget):
    def __init__(self, username, user_role):
        super().__init__()
        uic.loadUi("ui/templates/tabs/vehicleandtrip/createtrip.ui", self)

        # Sayfa animasyonu
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

        self.username = username
        self.user_role = user_role
        
        
        self.load_couriers()
        self.load_vehicles()
        self.load_drivers()
        self.comboBoxLoadingProvince.currentIndexChanged.connect(self.load_districts)
        self.comboBoxDestinationProvince.currentIndexChanged.connect(self.load_districts)


        # Load json files
        with open('resources/il.json', 'r', encoding='utf-8') as city_file:
            data = json.load(city_file)
            if isinstance(data, dict) and 'il' in data:
                self.city_list = data['il']
            else:
                self.city_list = data

        with open('resources/ilce.json', 'r', encoding='utf-8') as district_file:
            data = json.load(district_file)
            if isinstance(data, dict) and 'ilce' in data:
                self.district_list = data['ilce']
            else:
                self.district_list = data
        self.load_cities()

        

    
    def load_cities(self):
        self.comboBoxLoadingProvince.clear()
        sorted_cities = sorted(self.city_list, key=lambda city: int(city['id']))
        for city in sorted_cities:
            self.comboBoxLoadingProvince.addItem(city['name'], city['id'])
            self.comboBoxDestinationProvince.addItem(city['name'],city['id'])
        self.load_districts()

    def load_districts(self):
        self.comboBoxLoadingDistrict.clear()
        self.comboBoxDestinationDistrict.clear()
        selected_loding_city_id = self.comboBoxLoadingProvince.currentData()
        selected_destination_city_id = self.comboBoxDestinationProvince.currentData()
        for loading_district in self.district_list:
            if str(loading_district['il_id']) == str(selected_loding_city_id):
                self.comboBoxLoadingDistrict.addItem(loading_district['name'])
        for destination_district in self.district_list:
            if str(destination_district['il_id']) == str(selected_destination_city_id):
                self.comboBoxDestinationDistrict.addItem(destination_district['name'])

    def load_drivers(self):
        self.comboBoxDriver.clear()
        service = DriverService()
        driver_list = service.get_drivers()
        for driver in driver_list:
          fullname = f"{driver['driverName']} {driver['driverSurname']}"
          self.comboBoxDriver.addItem(fullname,driver.get('driverId'))
    
    def load_couriers(self):
        self.comboBoxCourier.clear()
        service = CourierService()
        courier_list = service.get_couriers()
        for courier in courier_list:
            fullname = f"{courier['courierName']} {courier['courierSurname']}"
            self.comboBoxCourier.addItem(fullname,courier.get('courierId'))

    def load_vehicles(self):
        self.comboBoxVehicle.clear()
        service = VehicleService()
        vehicle_list = service.get_vehicle()
        for vehicle in vehicle_list:
            number_plate = f"{vehicle['vehicleNumberPlate']}"
            self.comboBoxVehicle.addItem(number_plate, vehicle.get('vehicleId'))
        print(vehicle_list)



