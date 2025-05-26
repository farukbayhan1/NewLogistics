from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QPropertyAnimation

class VehicleAndTripDropDown(QWidget):
    def __init__(self, main_window_ref):
        super().__init__()
        uic.loadUi("ui/templates/dropdown/vehicleandtrip.ui", self)
        self.mainWindowRef = main_window_ref
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.setStyleSheet("background: transparent;")
        self.setGraphicsEffect(None) # Shadow Effect
        self.opacity_effect = QGraphicsOpacityEffect(self) #Opacity Effect
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        
        #Push Buttons
        self.pushButtonAddVehicle.clicked.connect(self.open_add_vehicle_tab)
        self.pushButtonUpdateVehicle.clicked.connect(self.update_vehicle_tab)
        self.pushButtonCreateTrip.clicked.connect(self.open_create_trip_tab)
        self.pushButtonShowTrip.clicked.connect(self.open_get_trip_tab)
        self.pushButtonReportTrip.clicked.connect(self.open_report_trip_tab)

    def open_add_vehicle_tab(self):
        self.hide()
        self.mainWindowRef.show_add_vehicle()
    
    def open_create_trip_tab(self):
        self.hide()
        self.mainWindowRef.show_create_trip()
    
    def open_get_trip_tab(self):
        self.hide()
        self.mainWindowRef.show_get_trip()
    
    def open_report_trip_tab(self):
        self.hide()
        self.mainWindowRef.show_report_trip()
    
    def update_vehicle_tab(self):
        self.hide()
        self.mainWindowRef.show_update_vehicle()
