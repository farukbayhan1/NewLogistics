import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
from PyQt5.QtWidgets import QMainWindow,QApplication, QVBoxLayout, QLabel, QWidget, QTabWidget
from PyQt5 import uic
from PyQt5.QtCore import Qt

from ui.icons.buttons import buttons_resources
from views.dropdowns.employee import EmployeeDropDown
from views.dropdowns.personel import PersonelDropdown
from views.dropdowns.order import OrderDropDown
from views.dropdowns.vehicleandtrip import VehicleAndTripDropDown
from views.dropdowns.report import ReportDropDown

# Employee Tabs
from views.tabs.employee.addemployee import AddEmployeeTab
from views.tabs.employee.updateemployee import UpdateEmployeeTab
from views.tabs.employee.reportemployee import ReportEmployeeTab

# Personel Tabs
from views.tabs.personel.driveroperations import DriverOperationsTab
from views.tabs.personel.courieroperations import CourierOperationsTab
from views.tabs.personel.useroperations import UserOperationsTab

# Order Tabs
from views.tabs.order.addorder import AddOrderTab
from views.tabs.order.updateorder import UpdateOrderTab
from views.tabs.order.reportorder import ReportOrderTab

# Vehicle and Trip Tabs
from views.tabs.vehicleandtrip.addvehicle import AddVehicleTab
from views.tabs.vehicleandtrip.updatevehicle import UpdateVehicleTab
from views.tabs.vehicleandtrip.createtrip import CreateTripTab
from views.tabs.vehicleandtrip.gettrip import GetTripTab
from views.tabs.vehicleandtrip.reporttrip import ReportTripTab

# Report Tabs
from views.tabs.report.reportemployee import ReportMenuEmployeeTab
from views.tabs.report.reportorder import ReportMenuOrderTab
from views.tabs.report.reporttrip import ReportMenuTripTab

# Controllers
from controllers.employeecontroller import AddEmployeeController
from controllers.usercontroller import AddUserController
from controllers.drivercontroller import DriverController
from controllers.couriercontroller import CourierController
from controllers.vehiclecontroller import VehicleController


project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))


class MainWindow(QMainWindow):
    def __init__(self,username,user_role):
        super().__init__()
        uic.loadUi("ui/templates/new_main.ui",self)
        
        
        # Window Settings
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.showMaximized()
       
        
        # Show Username
        self.labelUser.setText(username.title())
        
        # Tab Widget
        self.tabWidget = QTabWidget(self.widgetPage)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.username = username
        self.user_role = user_role

      
        if not self.widgetPage.layout():
            layout = QVBoxLayout(self.widgetPage)
            self.widgetPage.setLayout(layout)
        else:
            layout = self.widgetPage.layout()
        layout.addWidget(self.tabWidget)

        # Buttons Dropwdowns
        self.dropdownEmployee = EmployeeDropDown(self)
        self.dropdownPersonel = PersonelDropdown(self)
        self.dropdownOrder = OrderDropDown(self)
        self.dropdowneVehicleAndTrip = VehicleAndTripDropDown(self)
        self.dropdownReport = ReportDropDown(self)

        # Main Buttons
        self.pushButtonEmployee.clicked.connect(lambda: self.show_dropdown(self.pushButtonEmployee, self.dropdownEmployee))
        self.pushButtonPersonel.clicked.connect(lambda: self.show_dropdown(self.pushButtonPersonel, self.dropdownPersonel))
        self.pushButtonOrder.clicked.connect(lambda: self.show_dropdown(self.pushButtonOrder, self.dropdownOrder))
        self.pushButtonVehicleAndTrip.clicked.connect(lambda: self.show_dropdown(self.pushButtonVehicleAndTrip, self.dropdowneVehicleAndTrip))
        self.pushButtonReport.clicked.connect(lambda: self.show_dropdown(self.pushButtonReport, self.dropdownReport))
        self.pushButtonLogout.clicked.connect(self.close)

        # Controllers
              
        
    def show_dropdown(self, button, dropdown_widget):
        pos = button.mapToGlobal(button.rect().topRight())
        self_x = pos.x() + 10  # 10px Right
        self_y = pos.y()        
        dropdown_widget.move(self_x, self_y)
        dropdown_widget.show()

    def show_tab(self, widget: QWidget, title: str):
        # Eğer aynı tipte bir widget zaten açıksa, o sekmeye geç
    
        for i in range(self.tabWidget.count()):
            existing_widget = self.tabWidget.widget(i)
            if isinstance(existing_widget, type(widget)):
                self.tabWidget.setCurrentIndex(i)
                return

        # Yeni sekme oluştur
        self.tabWidget.addTab(widget, title)
        self.tabWidget.setCurrentWidget(widget)
        
    def close_tab(self, index):
        self.tabWidget.removeTab(index)

    # Employe Tabs Functions
    def show_add_employee(self):
        widget = AddEmployeeTab(self.username,self.user_role)
        AddEmployeeController(widget)
        self.employee_controller = AddEmployeeController(widget)
        self.show_tab(widget, "Müşteri Ekle")
    def show_update_employee(self):
        widget = UpdateEmployeeTab()
        self.show_tab(widget, "Müşteri Bilgileri Güncelle")
    def show_report_employee(self):
        widget = ReportEmployeeTab()
        self.show_tab(widget, "Müşteri Raporları")
    

    # Personel Tabs Functions
    def show_driver_operations(self):
        widget = DriverOperationsTab(self.username,self.user_role)
        self.driver_controller = DriverController(widget)
        self.show_tab(widget, "Sürücü İşlemleri")
    
    def show_courier_operations(self):
        widget = CourierOperationsTab(self.username,self.user_role)
        self.courier_controller = CourierController(widget)
        self.show_tab(widget, "Kurye İşlemleri")
    
    def show_user_operations(self):
        widget = UserOperationsTab(self.username,self.user_role)
        self.user_controller = AddUserController(widget)
        self.show_tab(widget, "Kullanıcı İşlemleri")

    # Order Tabs Functions
    def show_add_order(self):
        widget = AddOrderTab()
        self.show_tab(widget, "Sipariş Ekle")
    def show_update_order(self):
        widget = UpdateOrderTab()
        self.show_tab(widget, "Sipariş Bilgileri Güncelle")
    def show_report_order(self):
        widget = ReportOrderTab()
        self.show_tab(widget, "Sipariş Raporları")
    
    # Vehicle and Trip Tabs Functions
    def show_add_vehicle(self):
        widget = AddVehicleTab(self.username,self.user_role)
        self.vehicle_controller = VehicleController(widget)
        self.show_tab(widget, "Araç Ekle")
    def show_update_vehicle(self):
        widget = UpdateVehicleTab()
        self.show_tab(widget, "Araç Bilgileri Güncelle")
    def show_create_trip(self):
        widget = CreateTripTab()
        self.show_tab(widget, "Yeni Sefer Oluştur")
    def show_get_trip(self):
        widget = GetTripTab()
        self.show_tab(widget, "Sefer Bilgileri")
    def show_report_trip(self):
        widget = ReportTripTab()
        self.show_tab(widget, "Sefer Raporları")

    # Report Tabs Functions
    def show_report_employee(self):
        widget = ReportMenuEmployeeTab()
        self.show_tab(widget, "Müşteri Raporları")
    def show_report_order(self):
        widget = ReportMenuOrderTab()
        self.show_tab(widget, "Sipariş Raporları")
    def show_report_trip(self):
        widget = ReportMenuTripTab()
        self.show_tab(widget, "Sefer Raporları")
        
    
    


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
