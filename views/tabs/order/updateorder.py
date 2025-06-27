from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QGraphicsOpacityEffect, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt, QPropertyAnimation
from views.form.checkorder import CheckOrderForm
from views.form.getfilterorder import GetFilteredOrder

from services.orderservice import OrderService
from services.employeeservice import AddEmployeeService
from services.courierservice import CourierService
from services.vehicleservice import VehicleService
from services.driverservice import DriverService
from resources.dbmanager import execute_query
from resources.query.sqlitequery import GET_ALL,CHECK_BARCODE, ADD_BARCODE,COUNT_BARCODE,DELETE_BARCODES


class UpdateOrderTab(QWidget):
    def __init__(self,username,user_role):
        super().__init__()
        uic.loadUi("ui/templates/tabs/order/updateorder.ui", self)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        self.order_service = OrderService()
        self.check_form = CheckOrderForm()
        self.order_filter_form = GetFilteredOrder()
        self.username = username
        self.user_role = user_role
        self.connect_signal()
        self.count_barcode()
        self.load_barcode()
        self.check_form.lineEditSearch.textChanged.connect(self.search_barcode)

    def connect_signal(self):
        self.pushButtonGetOrders.clicked.connect(self.open_order_filter_form)
        self.pushButtonDocumentCheck.clicked.connect(self.open_check_form)
        self.check_form.pushButtonSend.clicked.connect(self.sent_data)
        self.check_form.lineEditReadBarcode.returnPressed.connect(self.insert_barcode)
        self.order_filter_form.pushButtonApply.clicked.connect(self.handle_order_filter_form)
        
     
    def open_check_form(self):
        self.check_form.show()
        self.check_form.animation.start()
    
    def open_order_filter_form(self):
        self.order_filter_form.show()
        self.order_filter_form.animation.start()
        self.load_employee()
        self.load_courier()
        self.load_vehicle()
        self.load_driver()

    def insert_barcode(self):
        barcode = self.check_form.lineEditReadBarcode.text().strip()
        result = execute_query(CHECK_BARCODE,(barcode,),fetchone=True)
        if result:
            return QMessageBox.information(self.check_form,"Bilgi","Barkod Daha Önce Okutulmuş")
        else:
            execute_query(ADD_BARCODE,(barcode,),commit=True)
            self.check_form.lineEditReadBarcode.clear()
            self.count_barcode()
            self.load_barcode()
    
    def count_barcode(self):
        get_barcode_count = execute_query(COUNT_BARCODE,fetchone=True)
        count = get_barcode_count[0]
        self.check_form.labelCount.setText(str(count))

    def load_barcode(self):
        self.check_form.tableWidgetReadedOrder.setColumnCount(3)
        self.check_form.tableWidgetReadedOrder.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.check_form.tableWidgetReadedOrder.setHorizontalHeaderLabels([
            "İrsaliye Numarası",
            "Kontrol Tarihi",
            "Kontrol Durumu"
        ])
        rows = execute_query(GET_ALL,fetchall=True)
        self.check_form.tableWidgetReadedOrder.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 0, QTableWidgetItem(str(row[0])))
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 1, QTableWidgetItem(str(row[1])))
            self.check_form.tableWidgetReadedOrder.setItem(row_index, 2, QTableWidgetItem(str(row[2])))
    
    def search_barcode(self):
        search_text = self.check_form.lineEditSearch.text().strip()
        for row in range(self.check_form.tableWidgetReadedOrder.rowCount()):
            item = self.check_form.tableWidgetReadedOrder.item(row,0)
            if item:
                item_text = item.text()
                self.check_form.tableWidgetReadedOrder.setRowHidden(row,search_text not in item_text)

    def sent_data(self):
        data = []
        try:
            rows = execute_query(GET_ALL,fetchall=True)
            for row in rows:
                data.append({
                    "order_document_no":row[0],
                    "check_date":row[1],
                    "status":row[2],
                    "username":self.username
                })
            self.order_service.update_order(data)
            execute_query(DELETE_BARCODES,commit=True)
            self.load_barcode()
            self.count_barcode()
            return QMessageBox.information(self.check_form,"Bilgi","İrsaliye Kontrol Verileri Gönderildi")
        except Exception as e:
            print(e)
            return QMessageBox.warning(self.check_form,"Hata",f"İrsaliye Kontrol Modülünde Hata: {str(e)}")

    def handle_order_filter_form(self):
        filter = {}
        order_document_no = self.order_filter_form.lineEditOrderDocumentNumber.text().strip()
        start_date = self.order_filter_form.lineEditStartDate.text().strip()
        end_date = self.order_filter_form.lineEditEndDate.text().strip()
        trip_number = self.order_filter_form.lineEditTripNumber.text().strip()
        employee_name = self.order_filter_form.comboBoxEmployee.currentText().strip()
        vehicle_id = self.order_filter_form.comboBoxVehicle.currentData()
        driver_id = self.order_filter_form.comboBoxDriver.currentData()
        courier_id = self.order_filter_form.comboBoxCourier.currentData()
        if order_document_no:
            filter["order_document_no"] = order_document_no
        if start_date:
            filter["start_date"] = start_date
        if end_date:
            filter["end_date"] = end_date
        if trip_number:
            filter["trip_code"] = trip_number
        if employee_name:
            filter["employee_name"] = employee_name
        
        order_list = self.order_service.get_orders(filters=filter)
        # Burada sonucu tabloya yerleştirl ve formu kapat
        self.tableWidgetOrder.setRowCount(len(order_list))
        self.tableWidgetOrder.setColumnCount(10)
        self.tableWidgetOrder.setHorizontalHeaderLabels([
            "Sipariş Id",
            "Sipariş Numarası",
            "İrsaliye Numarası",
            "Teslimat Adresi",
            "Sipariş Plaka",
            "Müşteri Adı",
            "Paket Ad.",
            "Sipariş Onay Tarihi",
            "Sipariş Plan Onay Tarihi",
            "Sipariş Sefer Numarası"
        ])
        for row_index, i in enumerate(order_list):
            for row_index, i in enumerate(order_list):
                self.tableWidgetOrder.setItem(row_index, 0, QTableWidgetItem(str(i[0])))  # orderId
                self.tableWidgetOrder.setItem(row_index, 1, QTableWidgetItem(str(i[1])))  # orderNo
                self.tableWidgetOrder.setItem(row_index, 2, QTableWidgetItem(str(i[2])))  # orderDocumentNo
                self.tableWidgetOrder.setItem(row_index, 3, QTableWidgetItem(str(i[3])))  # orderDeliveryAdress
                self.tableWidgetOrder.setItem(row_index, 4, QTableWidgetItem(str(i[4])))  # orderNumberPlate
                self.tableWidgetOrder.setItem(row_index, 5, QTableWidgetItem(str(i[5])))  # employeeName
                self.tableWidgetOrder.setItem(row_index, 6, QTableWidgetItem(str(i[6])))  # orderBoxCount
                self.tableWidgetOrder.setItem(row_index, 7, QTableWidgetItem(str(i[7])))  # orderConfirmationDateFormatted
                self.tableWidgetOrder.setItem(row_index, 8, QTableWidgetItem(str(i[8])))  # orderPlanConfirmationDateFormatted
                self.tableWidgetOrder.setItem(row_index, 9, QTableWidgetItem(str(i[9])))  # orderTripNu

        
       
    def load_employee(self):
        self.order_filter_form.comboBoxEmployee.clear()
        self.order_filter_form.comboBoxEmployee.addItem("Tümü","")
        service = AddEmployeeService()
        employee_list = service.get_employees()
        for employee in employee_list:
          employee_name = f"{employee['employeeName']}"
          self.order_filter_form.comboBoxEmployee.addItem(employee_name,employee.get('employeeId'))
        

    def load_courier(self):
        self.order_filter_form.comboBoxCourier.clear()
        self.order_filter_form.comboBoxCourier.addItem("Tümü","")
        service = CourierService()
        courier_list = service.get_couriers()
        for courier in courier_list:
            courier_name = f"{courier['courierName']} {courier['courierSurname']}"
            self.order_filter_form.comboBoxCourier.addItem(courier_name,courier.get('courierId'))


    def load_vehicle(self):
        self.order_filter_form.comboBoxVehicle.clear()
        self.order_filter_form.comboBoxVehicle.addItem("Tümü","")
        service = VehicleService()
        vehicle_list = service.get_vehicle()
        for vehicle in vehicle_list:
            self.order_filter_form.comboBoxVehicle.addItem(vehicle['vehicleNumberPlate'],vehicle['vehicleId'])


    def load_driver(self):
        self.order_filter_form.comboBoxDriver.clear()
        self.order_filter_form.comboBoxDriver.addItem("Tümü","")
        service = DriverService()
        driver_list = service.get_drivers()
        for driver in driver_list:
           driver_name = f"{driver['driverName']} {driver['driverSurname']}"
           self.order_filter_form.comboBoxDriver.addItem(driver_name,driver.get('driverId'))

    
        

    

     

    